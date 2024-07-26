Browserstack library for RobotFramework
==================================================

Introduction
------------

`BrowserstackLibrary`_ is a keyword library for integration with Browserstack for mobile testing using `Robot Framework`_ and **AppiumLibrary**. Library can be downloaded from **PyPI**.

Before installing the library in your project, ensure that you or your project have access credentials to Browserstack.

If you don't have one, go to https://www.browserstack.com to register.

It is supporting Python 3.8+


Appium Library Dependency
------------
Some BrowserstackLibrary keywords use AppiumLibrary instances so they can be executed. Therefore, your project needs to have the Appium Library installed. 

Later, support for WEB testing will be added.


Keyword Documentation
---------------------

Access `Keyword Documentation`_  to see available keywords.


Installation
------------

**Option 1** :: With Pip

    pip install robotframework-browserstacklibrary


**Option 2** :: With Poetry

    poetry add robotframework-browserstacklibrary


Usage
-----

Below is an example of using the Browserstack Library together with the Robot Framework and Appium Library:

.. code:: robotframework

    *** Settings ***
    Library    AppiumLibrary
    Library    BrowserstackLibrary  username=${BS_USERNAME}  access_key=${BS_ACCESS_KEY}
    Test Teardown    Run Keywords
    ...    Update Test Case Status in BrowserStack
    ...    Close Application
    Resource    base.resource

    *** Test Cases ***
    Olá Mundo
        ${bs_url}  Upload Application to Browserstack
        ...    app_name=ted.apk
        ...    app_path=app/app.apk
        ...    custom_id=TED_OUVINTE_123

        Open Application In Browserstack
        ...  automationName=uiautomator2
        ...  platformName=${PLATFORM_NAME}
        ...  deviceName=${DEVICE_NAME}
        ...  app=${bs_url}
        ...  project=${BROWSERSTACK_PROJECT}
        ...  build=TED
        ...  name=${TEST_NAME}
        ...  bstack:options=${BROWSERSTACK_OPTIONS}
        ...  browserstack.networkLogs=${True}
        ...  browserstack.networkLogsOptions.captureContent=${True}
        ...  autoGrantPermissions=${True}
        ...  autoAcceptAlerts=${True}
        ...  disableIdLocatorAutocompletion=${True}
        ...  browserstack.idleTimeout=60
        ...  interactiveDebugging=${True}

        Wait Until Element Is Visible    Next
        Click Element    Next

Create a file with the content above (name it: ``test_file.robot``) and execute:

    robot -d log test_file.robot

Another example, containing the keywords from the Browserstack Library, in a more structured way is in https://github.com/robotcourses/RF_Appium


.. _BrowserstackLibrary: https://github.com/robotcourses/robotframework-browserstack
.. _Robot Framework: https://robotframework.org
.. _PyPI: https://pypi.org/project/robotframework-appiumlibrary/
.. _Keyword Documentation: https://robotcourses.github.io/robotframework-browserstack/BrowserstackLibrary.html