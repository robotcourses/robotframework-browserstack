# -*- coding: utf-8 -*-

from BrowserstackLibrary.keywords import *
from BrowserstackLibrary.utils import *
from BrowserstackLibrary.version import VERSION

from robot.api import logger
from robot.api.deco import keyword


__version__ = VERSION


class BrowserstackLibrary(
    _UpdateTestCase,
    _UploadApplication,
    _BrowserstackClient
):
    """
    docstring

    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self, username, access_key):
        """
        docstring
        """

        self.auth_user = username
        self.auth_token = access_key

        if not self.auth_user or not self.auth_token:
            raise ValueError("USERNAME and ACCESS_KEY are required")

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
    def update_test_status(self, appium_session_id, result, reason):
        self.status_updater.update_status(appium_session_id, result, reason)