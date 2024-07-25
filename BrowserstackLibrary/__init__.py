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

    def __init__(self, username=None, access_key=None):
        """BrowserstackLibrary can be imported with required arguments.

        ``username`` is your username on the Browserstack platform.

        ``access_key`` is your access key on the Browserstack platform.

        This way, when you start your suite, the app will be sent directly to Browserstack

        Examples:
        | Library | BrowserstackLibrary | ${USER_NAME} | ${ACCESS_KEY} |
        """

        self.auth_user = username
        self.auth_token = access_key

        if not self.auth_user or not self.auth_token:
            logger.warn("USERNAME and ACCESS_KEY are required")

        self.client = _BrowserstackClient(self.auth_user, self.auth_token)
        self.app_manager = _UploadApplication(self.client)
        self.status_updater = _UpdateTestCase(self.client)

        logger.info("Initialized BrowserStack client and managers.")

    @keyword('Upload Application to Browserstack')
    def uplaoad_app(self, app_name, app_path=None, app_url=None, custom_id=None):

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
        appiumlib = BuiltIn().get_library_instance('AppiumLibrary')
        appium_session_id = appiumlib.get_appium_sessionId()
        result = BuiltIn().get_variable_value("${TEST_STATUS}")
        reason = BuiltIn().get_variable_value("${TEST_MESSAGE}")

        self.status_updater.update_status(appium_session_id, result, reason)
