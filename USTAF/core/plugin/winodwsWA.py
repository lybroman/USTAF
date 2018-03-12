'''
This file is for some Windows Hardcode stuff
'''

from USTAF.core.case import Case

WIN_PREFIX = "C:/AutoBat/Bat/"
CASE_DETAIL_URL = 'http://sample.com/rest/query_parent_category/'
WIN_CI_BUILD_PATH_LIST = [r'\\sample_dir\OSimages\Artifacts\Gerrit CI\Patchset Created (Common)',
                     r'\\sample_dir\OSimages\Artifacts\Gerrit CI\FW Patchset Created (Common)']
WIN_FULL_BUILD_PATH = ''

WIN_LOG_ROOT_PATH = r'\\sample_dir\AUTO_TEST\TWSResult'


def generateSetupEnvCases(scenario):

    CAMERA_SETUPENV_CAMERA_COPY_DRIVER = Case(scenario)
    CAMERA_SETUPENV_CAMERA_COPY_DRIVER.name = 'CAMERA_SETUPENV_CAMERA_COPY_DRIVER'
    CAMERA_SETUPENV_CAMERA_COPY_DRIVER.cmd = r'C:/AutoBat/bat/Desktop/Scripts/DriverManagement/CopyBuildInfoDriver.py CAMERA_COPY_DRIVER {Build_No_Variable}'
    CAMERA_SETUPENV_CAMERA_COPY_DRIVER.critical = True
    CAMERA_SETUPENV_CAMERA_COPY_DRIVER.failrerun = 1
    scenario.addTestCaseObject(CAMERA_SETUPENV_CAMERA_COPY_DRIVER)

    CAMERA_SETUPENV_CAMERA_INSTALL_CAMERA = Case(scenario)
    CAMERA_SETUPENV_CAMERA_INSTALL_CAMERA.name = 'CAMERA_SETUPENV_CAMERA_INSTALL_CAMERA'
    CAMERA_SETUPENV_CAMERA_INSTALL_CAMERA.cmd = r'C:/AutoBat/bat/Desktop/Scripts/DriverManagement/InstallCameraDriver.py CAMERA_INSTALL_CAMERA'
    CAMERA_SETUPENV_CAMERA_INSTALL_CAMERA.critical = True
    CAMERA_SETUPENV_CAMERA_INSTALL_CAMERA.failrerun = 1
    scenario.addTestCaseObject(CAMERA_SETUPENV_CAMERA_INSTALL_CAMERA)

    CAMERA_SETUPENV_CLEANAPPLOG = Case(scenario)
    CAMERA_SETUPENV_CLEANAPPLOG.name = 'CAMERA_SETUPENV_CLEANAPPLOG'
    CAMERA_SETUPENV_CLEANAPPLOG.cmd = r'C:/AutoBat/bat/Desktop/Scripts/CleanUpMetroResult.py CLEANAPPLOG'
    CAMERA_SETUPENV_CLEANAPPLOG.critical = True
    CAMERA_SETUPENV_CLEANAPPLOG.failRerun = 1
    scenario.addTestCaseObject(CAMERA_SETUPENV_CLEANAPPLOG)

    CAMERA_SETUPENV_REBOOT_DUT_NOW = Case(scenario)
    CAMERA_SETUPENV_REBOOT_DUT_NOW.name = 'CAMERA_SETUPENV_REBOOT_DUT_NOW'
    CAMERA_SETUPENV_REBOOT_DUT_NOW.cmd = r'cmd.exe /c shutdown /r /f /t 0'
    CAMERA_SETUPENV_REBOOT_DUT_NOW.alwaysPass = True
    scenario.addTestCaseObject(CAMERA_SETUPENV_REBOOT_DUT_NOW)

    CAMERA_SETUPENV_CAMERA_CHECK_DEVICE = Case(scenario)
    CAMERA_SETUPENV_CAMERA_CHECK_DEVICE.name = 'CAMERA_SETUPENV_CAMERA_CHECK_DEVICE'
    CAMERA_SETUPENV_CAMERA_CHECK_DEVICE.cmd = r'C:/AutoBat/bat/Desktop/Scripts/DriverManagement/CheckCameraDriver.py CAMERA_CHECK_DEVICE'
    CAMERA_SETUPENV_CAMERA_CHECK_DEVICE.critical = True
    CAMERA_SETUPENV_CAMERA_CHECK_DEVICE.failRerun = 0
    scenario.addTestCaseObject(CAMERA_SETUPENV_CAMERA_CHECK_DEVICE)


def generateCopyCases(scenario):
    MapLogTWS = Case(scenario)
    MapLogTWS.name = 'MapLogTWS'
    MapLogTWS.cmd = r'C:/TWSTools/MapLogTWS.exe'
    scenario.addTestCaseObject(MapLogTWS)

    Copy_BATResults = Case(scenario)
    Copy_BATResults.name = 'Copy_BATResults'
    Copy_BATResults.cmd = '"C:/TWSTools/CopyTWSResultsFolder.py \"C:/AutoBAT_Results\" \"L:\" \"{BuildConfig_Variable}\" \"{Build_No_Variable}\" \"{TARGET.id}\" {UUID}"'
    scenario.addTestCaseObject(Copy_BATResults)

