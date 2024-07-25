# -*- coding: utf-8 -*-

from BrowserstackLibrary.keywords import *
from BrowserstackLibrary.utils import *
from BrowserstackLibrary.version import VERSION

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword


__version__ = VERSION


class BrowserstackLibrary(
    _UpdateTestCase,
    _UploadApplication,
    _BrowserstackClient
):
    """
        BrowserstackLibrary is a library for integration with Device Farm Browserstack.

        = Application Upload and Update Test Case Status =

            With the available keywords, you will be able to easily upload your app 
            (APK, IPA, etc.) directly to Browserstack and also update the Test Cases 
            executed in Browserstack.
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self, username: str = None, access_key: str = None):
        """BrowserstackLibrary can be imported with required arguments.

        ``username`` is your username on the Browserstack platform.

        ``access_key`` is your access key on the Browserstack platform.

        This way, when you start your suite, the app will be sent directly to Browserstack

        Examples:
        | Library | BrowserstackLibrary | ${USER_NAME} | ${ACCESS_KEY} |
        """

        self.auth_user = username
        self.auth_token = access_key
        self.remote_url = f'http://{self.auth_user}:{self.auth_token}@hub.browserstack.com:80/wd/hub'

        if not self.auth_user or not self.auth_token:
            logger.warn("USERNAME and ACCESS_KEY are required")

        self.client = _BrowserstackClient(self.auth_user, self.auth_token)
        self.app_manager = _UploadApplication(self.client)
        self.status_updater = _UpdateTestCase(self.client)

        logger.info("Initialized BrowserStack client and managers.")

    @keyword('Upload Application to Browserstack')
    def uplaoad_app(self, app_name: str, app_path: str = None, app_url:str = None, custom_id: str = None):
        """Uploads an app to Browserstack, either through the PATH or app URL.

        ``app_name`` is the name of the application. Example: "ROBOT.apk"

        ``app_path`` is the relative or absolute path to get to the app. Example: "app/ROBOT.apk"
        It is only required if app_url is not populated.

        ``app_url`` is your app's remote URL. Make sure it is a publicly accessible URL 
        as BrowserStack will attempt to download the app from this location.
        It is only required if app_path is not populated.

        ``custom_id`` is your Custom ID for the application.

        Examples:
        | ${bs_url} | Upload Application to Browserstack   |
        | ...       | app_name=ROBOT.apk                   |
        | ...       | app_path=app/ROBOT.apk               |
        | ...       | custom_id=ID_123                     |
        -
        -
        | ${bs_url} | Upload Application to Browserstack         |
        | ...       | app_name=ROBOT.apk                         |
        | ...       | app_url=https://downloadurl.com/ROBOT.apk  |
        | ...       | custom_id=ID_123                           |
        """

        if not app_name:
            raise ValueError("app_name must be provided")

        if not (app_path or app_url):
            raise ValueError("Either app_path or app_url must be provided, but not both")

        if app_path and app_url:
            raise ValueError("Only one of app_path or app_url should be provided, not both")
        
        if not custom_id:
            raise ValueError("custom_id must be provided")

        if app_path:
            response = self.app_manager.upload_app_file(app_name, app_path, custom_id)
        elif app_url:
            response = self.app_manager.upload_public_url(app_name, app_url, custom_id)

        if response:
            return response.get('app_url')

    @keyword('Update Test Case Status in BrowserStack')
    def update_test_status(self):
        """This keyword must be used as 'TEARDOWN TEST'. 
        
        It will send the status of the test execution to 
        Browserstack as well as error messages that were detected.

        Examples:
        | Library | BrowserstackLibrary | ${USER_NAME} | ${ACCESS_KEY} |
        | Test Teardown | Update Test Case Status in BrowserStack | |  |
        """
        appium_lib = BuiltIn().get_library_instance('AppiumLibrary')
        appium_session_id = appium_lib.get_appium_sessionId()
        result = BuiltIn().get_variable_value("${TEST_STATUS}")
        reason = BuiltIn().get_variable_value("${TEST_MESSAGE}")

        self.status_updater.update_status(appium_session_id, result, reason)

    @keyword('Open Application In Browserstack')
    def open_application(self, capabilities: dict):
        """
        This keyword will open the application in Browserstack, sending the desired 
        capabilities that have been configured.

        Capabilities must be sent as a dictionary type (&{DICT}).

        Example:

        | *** Test Cases ***                                                    | 
        | Hello World                                                           | 
        |     | ${bs_url} |Upload Application to Browserstack                   |
        |     | ...   | app_name=ted.apk                                        |
        |     | ...   | app_path=app/app.apk                                    |
        |     | ...   | custom_id=TED_OUVINTE_123                               |
        |     |         |                                                       |
        |     | &{caps} |  Create Dictionary                                    |
        |     | ...  | automationName=uiautomator2                              |
        |     | ...  | platformName=${PLATFORM_NAME}                            |
        |     | ...  | deviceName=${DEVICE_NAME}                                |
        |     | ...  | app=${bs_url}                                            |
        |     | ...  | project=${BROWSERSTACK_PROJECT}                          |
        |     | ...  | build=TED                                                |
        |     | ...  | name=${TEST_NAME}                                        |
        |     | ...  | bstack:options=${BROWSERSTACK_OPTIONS}                   |
        |     | ...  | browserstack.networkLogs=${True}                         |
        |     | ...  | browserstack.networkLogsOptions.captureContent=${True}   |
        |     | ...  | autoGrantPermissions=${True}                             |
        |     | ...  | autoAcceptAlerts=${True}                                 |
        |     | ...  | disableIdLocatorAutocompletion=${True}                   |
        |     | ...  | browserstack.idleTimeout=60                              |
        |     | ...  | interactiveDebugging=${True}                             |
        |     |      |                                                          |
        |     | Open Application In Browserstack  |  capabilities=${caps}       |
        """
        appium_lib = BuiltIn().get_library_instance('AppiumLibrary')

        appium_lib.open_application(
            remote_url=self.remote_url,
            alias=None,
            **capabilities
        )