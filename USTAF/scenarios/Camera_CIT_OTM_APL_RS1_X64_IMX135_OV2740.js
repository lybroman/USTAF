{
    "collateral": [
        [
            "http://SHWDEJOINTD221.sample.com:7073/api/service/content/Camera/SmartCopyTWS.exe",
            "C:/TWSTools/SmartCopyTWS.exe", 
            "", 
            ""
        ], 
        [
            "http://SHWDEJOINTD221.sample.com:7073/api/service/content/Camera/CameraTestSetEntryRS1.py",
            "C:/TWSTools/CameraTestSetEntryRS1.py", 
            "", 
            ""
        ], 
        [
            "http://SHWDEJOINTD221.sample.com:7073/api/service/content/Copyfolder/CopyTWSResultsFolder.py",
            "C:/TWSTools/CopyTWSResultsFolder.py", 
            "", 
            ""
        ], 
        [
            "http://SHWDEJOINTD221.sample.com:7073/api/service/content/Copyfolder/MapLogTWS.exe",
            "C:/TWSTools/MapLogTWS.exe", 
            "", 
            ""
        ]
    ], 
    "name": "Camera_CIT_OTM_APL_RS1_X64_IMX135_OV2740", 
	"test_type" : "CIT",
	"platform" : "APL", 
    "tools": [
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
			"env": true, 
            "name": "CAMERA_SETUPENV_PIT_APL_RSx64_IMX135_OV2740", 
			"parameters": "C:/TWSTools/CameraTestSetEntryRS1.py CAMERA_SETUPENV_PIT_APL_RSx64_IMX135_OV2740 -DUTOS x64 -TestType PIT -Mode 030 -Primary IMX135 -Secondary OV2740 -App x64 -ProjectCode BXT-APL-RS1 -BuildTarget GerritCI -DriverPackage BXT_Threshold_b0",
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": true, 
			"env": true, 
            "name": "CAMERA_SETUPENV_CAMERA_COPY_DRIVER", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/DriverManagement/CopyBuildInfoDriver.py CAMERA_COPY_DRIVER %Build_No_Variable%", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": true, 
			"env": true, 
            "name": "CAMERA_SETUPENV_CAMERA_INSTALL_CAMERA", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/DriverManagement/InstallCameraDriver.py CAMERA_INSTALL_CAMERA", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
			"env": true, 
            "name": "CAMERA_SETUPENV_CLEANAPPLOG", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/CleanUpMetroResult.py CLEANAPPLOG", 
            "failrerun": 0, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "executable": "C:/python27/python.exe", 
            "name": "CAMERA_SETUPENV_RESET_VERIFIER", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/DriverManagement/enableDriverVerify.py RESET_VERIFIER Reset", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "alwayspasses": true, 
			"env": true, 
            "dependency": "", 
            "critical": false, 
            "timeout": 900, 
            "repetition": 5, 
            "type": "subprocess", 
            "mustrun": false
        }, 
        {
            "executable": "cmd.exe", 
            "name": "CAMERA_SETUPENV_REBOOT_DUT_NOW", 
            "parameters": "/c shutdown /r /f /t 0", 
            "type": "subprocess", 
            "alwayspasses": true, 
			"env": true, 
            "timeout": 600, 
            "requires": {
                "named_req": "TARGET"
            }
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
			"env": true, 
            "name": "CAMERA_SETUPENV_CHECK_VERIFIER_DISABLED", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/DriverManagement/enableDriverVerify.py CHECK_VERIFIER_DISABLED VerifyDisabled", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": true, 
            "name": "CAMERA_SETUPENV_CAMERA_CHECK_DEVICE", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/DriverManagement/CheckCameraDriver.py CAMERA_CHECK_DEVICE", 
            "repetition": 5, 
			"env": true, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_CHECK_CAMERA_POSITION_PRIMARY_PREVIEW_NV12_STILL_MAX_NV12", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestSingleCamDualPin.py CAMERA_CHECK_CAMERA_POSITION_PRIMARY_PREVIEW_NV12_STILL_MAX_NV12", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_CHECK_CAMERA_POSITION_SECONDARY_PREVIEW_NV12_STILL_MAX_NV12", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestSingleCamDualPin.py CAMERA_CHECK_CAMERA_POSITION_SECONDARY_PREVIEW_NV12_STILL_MAX_NV12", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_CHECK_CAMERA_POSITION_PRIMARY_PREVIEW_NV12_VIDEO_MAX_NV12", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestSingleCamDualPin.py CAMERA_CHECK_CAMERA_POSITION_PRIMARY_PREVIEW_NV12_VIDEO_MAX_NV12", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_CHECK_CAMERA_POSITION_SECONDARY_PREVIEW_NV12_VIDEO_MAX_NV12", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestSingleCamDualPin.py CAMERA_CHECK_CAMERA_POSITION_SECONDARY_PREVIEW_NV12_VIDEO_MAX_NV12", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_HDR_AUTO_PRIMARY_STILL_3264x1836_JPEG", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestHDR.py CAMERA_HDR_AUTO_PRIMARY_STILL_3264x1836_JPEG", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_HDR_AUTO_SECONDARY_STILL_1920x1080_NV12", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestHDR.py  CAMERA_HDR_AUTO_SECONDARY_STILL_1920x1080_NV12", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_HDR_AUTO_PRIMARY_STILL_2560x1920_NV12", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestHDR.py CAMERA_HDR_AUTO_PRIMARY_STILL_2560x1920_NV12", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_SWITCHRESOLUTION_SECONDARY_STILL_ALL_ORDER_REVERSE_PREVIEW_MINSAMEAR", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_SWITCHRESOLUTION_SECONDARY_STILL_ALL_ORDER_REVERSE_PREVIEW_MINSAMEAR Camera_SwitchResolution_Secondary_Still_All_Order_Reverse_Preview_MinSameAR", 
            "repetition": 5,
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_SWITCHRESOLUTION_SECONDARY_VIDEO_ALL_ORDER_DEFAULT_PREVIEW_MAXSAMEAR", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_SWITCHRESOLUTION_SECONDARY_VIDEO_ALL_ORDER_DEFAULT_PREVIEW_MAXSAMEAR Camera_SwitchResolution_Secondary_Video_All_Order_Default_Preview_MaxSameAR", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_SWITCHRESOLUTION_PRIMARY_STILL_ALL_ORDER_REVERSE_PREVIEW_MAXSAMEAR", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_SWITCHRESOLUTION_PRIMARY_STILL_ALL_ORDER_REVERSE_PREVIEW_MAXSAMEAR Camera_SwitchResolution_Primary_Still_All_Order_Reverse_Preview_MaxSameAR", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_SWITCHRESOLUTION_PRIMARY_PREVIEW_ALL_ORDER_DEFAULT", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_SWITCHRESOLUTION_PRIMARY_PREVIEW_ALL_ORDER_DEFAULT Camera_SwitchResolution_Primary_Preview_All_Order_Default", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_WIN8UI_AUTO_PHOTOSEQ_ALLRESOLUTIONS_SECONDARY_1920x1080_NV12", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_WIN8UI_AUTO_PHOTOSEQ_ALLRESOLUTIONS_SECONDARY_1920x1080_NV12 Camera_PhotoSeq_AllResolutions_Secondary_History08_All16_1920x1080_NV12", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_WIN8UI_AUTO_PHOTOSEQ_ALLRESOLUTIONS_PRIMARY_4096X2304_JPEG", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_WIN8UI_AUTO_PHOTOSEQ_ALLRESOLUTIONS_PRIMARY_4096X2304_JPEG Camera_PhotoSeq_AllResolutions_Primary_History08_All16_4096x2304_JPEG", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_WIN8UI_AUTO_PHOTOCONFIRMATION_NV12_VPS_PRIMARY_PREVIEW_640X360_NV12", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_WIN8UI_AUTO_PHOTOCONFIRMATION_NV12_VPS_PRIMARY_PREVIEW_640X360_NV12 Camera_PhotoConfirmation_Nv12_VPS_Primary_Preview_640x360_NV12", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_API_KSPROPERTY_0156", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/APITest/CameraKSPropertyAPI.py CAMERA_API_KSPROPERTY_0156 PROPSETID_VIDCAP_CAMERACONTROL KSPROPERTY_CAMERACONTROL_ZOOM SET", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_BASIC_DESKTOP_SWITCHMODE_PRIMARY_IMAGE_3264x1836_JPEG_VIDEO", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestSingleCamSwitchMode.py CAMERA_BASIC_DESKTOP_SWITCHMODE_PRIMARY_IMAGE_3264x1836_JPEG_VIDEO Primary still jpeg 3264 1836 1000 video 1000 0", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_WIN8UI_AUTO_SWITCHMODE_SECONDARY_VIDEO_1280x720_NV12_IMAGE", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_WIN8UI_AUTO_SWITCHMODE_SECONDARY_VIDEO_1280x720_NV12_IMAGE Camera_SwitchMode_Secondary_Video_1280x720_NV12_Image", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_BASIC_SWITCH_CAMERA_PRIMARY_PREVIEW_STILL_SECONDARY_PREVIEW_STILL", 
            "parameters": "c:/AutoBAT/BAT//Desktop/Scripts/FeatureTestSwitchCamera.py CAMERA_BASIC_SWITCH_CAMERA_PRIMARY_PREVIEW_STILL_SECONDARY_PREVIEW_STILL", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_WIN8UI_AUTO_TEST_SWITCHCAMERA_PRIMARY_VIDEO_60FPS_SECONDARY_VIDEO", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_WIN8UI_AUTO_TEST_SWITCHCAMERA_PRIMARY_VIDEO_60FPS_SECONDARY_VIDEO Camera_SwitchCamera_Primary_Video_60FPS_Secondary_Video", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_WIN8UI_AUTO_VPS_FOCUS_WITHOUTCONFIRMATION_18_PRIMARY_IMAGE_1920X1080_JPEG", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_WIN8UI_AUTO_VPS_FOCUS_WITHOUTCONFIRMATION_18_PRIMARY_IMAGE_1920X1080_JPEG Camera_VPS_FOCUS_WITHOUTCONFIRMATION_18_Primary_Image_1920x1080_JPEG", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_WIN8UI_AUTO_VPS_EXPOSURE_WITHCONFIRMATION_18_SECONDARY_IMAGE_1920X1080_JPEG", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_WIN8UI_AUTO_VPS_EXPOSURE_WITHCONFIRMATION_18_SECONDARY_IMAGE_1920X1080_JPEG Camera_VPS_EXPOSURE_WITHCONFIRMATION_18_Secondary_Image_1920x1080_JPEG", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_WIN8UI_AUTO_VPS_INTERLEAVED_MINMIDMAX_12_SECONDARY_IMAGE_1920X1080_JPEG", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_WIN8UI_AUTO_VPS_INTERLEAVED_MINMIDMAX_12_SECONDARY_IMAGE_1920X1080_JPEG Camera_VPS_INTERLEAVED_MINMIDMAX_12_Secondary_Image_1920x1080_JPEG", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_WIN8UI_AUTO_VPS_COMBINED_ALLSAMEMID_18_PRIMARY_IMAGE_1920X1080_JPEG", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_WIN8UI_AUTO_VPS_COMBINED_ALLSAMEMID_18_PRIMARY_IMAGE_1920X1080_JPEG Camera_VPS_COMBINED_ALLSAMEMID_18_Primary_Image_1920x1080_JPEG", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_IMAGEEFFECT_SECONDARY_PREVIEW_MONOCHROME", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestColorEffect.py  CAMERA_IMAGEEFFECT_SECONDARY_PREVIEW_MONOCHROME", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_BASIC_PRIMARY_PREVIEW_ALL_NV12_VIDEO_640X360_NV12", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestSingleCamDualPin.py CAMERA_BASIC_PRIMARY_PREVIEW_ALL_NV12_VIDEO_640X360_NV12", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_BASIC_PRIMARY_PREVIEW_ALL_NV12_VIDEO_1280x720_YUY2", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestSingleCamDualPin.py CAMERA_BASIC_PRIMARY_PREVIEW_ALL_NV12_VIDEO_1280x720_YUY2", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_BASIC_SECONDARY_PREVIEW_ALL_NV12_VIDEO_1920x1080_NV12", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestSingleCamDualPin.py CAMERA_BASIC_SECONDARY_PREVIEW_ALL_NV12_VIDEO_1920x1080_NV12", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_WIN8UI_AUTO_ENUMFORMAT_PRIMARY_VIDEO_NV12", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_WIN8UI_AUTO_ENUMFORMAT_PRIMARY_VIDEO_NV12 Camera_EnumFormat_Primary_Video_NV12", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_BASIC_PRIMARY_PREVIEW_ALL_NV12_VIDEO_640x480_NV12", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestSingleCamDualPin.py CAMERA_BASIC_PRIMARY_PREVIEW_ALL_NV12_VIDEO_640x480_NV12", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_WIN8UI_AUTO_FILEFORMAT_PRIMARY_VIDEO_NV12_WMV", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_WIN8UI_AUTO_FILEFORMAT_PRIMARY_VIDEO_NV12_WMV Camera_FileFormat_Primary_Video_NV12_WMV", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_INTEXTEND_API_SECONDARY_WHITEBALANCEMODE", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_INTEXTEND_API_SECONDARY_WHITEBALANCEMODE Secondary IntExtWhiteBalanceMode", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_INTEXTEND_API_PRIMARY_EXPOSUREPRIORITY", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_INTEXTEND_API_PRIMARY_EXPOSUREPRIORITY Primary IntExtExposurePriority", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_PRIMARY_API_WINRT_METHOD_001", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_PRIMARY_API_WINRT_METHOD_001 Primary MediaCapture_CapturePhotoToStorageFileAsync", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_SECONDARY_API_BASIC_PROPERTY_004", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_SECONDARY_API_BASIC_PROPERTY_004 Secondary VideoDeviceController_Exposure", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_PRIMARY_API_BASIC_PROPERTY_010", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_PRIMARY_API_BASIC_PROPERTY_010 Primary VideoDeviceController_WhiteBalance", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_BASIC_PRIMARY_PREVIEW_ALL_NV12_STILL_3264X1836_JPEG", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestSingleCamDualPin.py CAMERA_BASIC_PRIMARY_PREVIEW_ALL_NV12_STILL_3264X1836_JPEG", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_BASIC_SECONDARY_STILL_1920X1080_NV12", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestSingleCamSiglePin.py CAMERA_BASIC_SECONDARY_STILL_1920X1080_NV12 Secondary still still nv12 1920 1080 0 0", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_BASIC_PRIMARY_STILL_2560X1920_JPEG", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestSingleCamSiglePin.py CAMERA_BASIC_PRIMARY_STILL_2560X1920_JPEG Primary still still jpeg 2560 1920 0 0", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_WIN8UI_AUTO_ENUMFORMAT_PRIMARY_IMAGE_NV12", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_WIN8UI_AUTO_ENUMFORMAT_PRIMARY_IMAGE_NV12 Camera_EnumFormat_Primary_Image_NV12", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_WIN8UI_AUTO_ENUMFORMAT_SECONDARY_IMAGE_JPEG", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_WIN8UI_AUTO_ENUMFORMAT_SECONDARY_IMAGE_JPEG Camera_EnumFormat_Secondary_Image_JPEG", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_DESKTOP_AUTO_ULL_PRIMARY_STILL", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestULL.py CAMERA_DESKTOP_AUTO_ULL_PRIMARY_STILL", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_WIN8UI_AUTO_LOWLAG_PHOTOLATENCY_PRIMARY_2560x1440_NV12", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_WIN8UI_AUTO_LOWLAG_PHOTOLATENCY_PRIMARY_2560x1440_NV12 Camera_LowLag_PhotoLatency_Primary_2560x1440_NV12", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_LOWLAG_SWITCHCAMERA_023", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_LOWLAG_SWITCHCAMERA_023 Camera_LowLag_SwitchCamera_Secondary_LowLagRecord_Primary_LowLagPhoto", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_LOWLAG_SWITCHMODE_001", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_LOWLAG_SWITCHMODE_001 Camera_LowLag_SwitchMode_Primary_NormalPhoto_LowLagPhoto", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_WIN8UI_AUTO_LOWLAG_PHOTOLATENCY_PRIMARY_1920x1080_JPEG", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_WIN8UI_AUTO_LOWLAG_PHOTOLATENCY_PRIMARY_1920x1080_JPEG Camera_LowLag_PhotoLatency_Primary_1920x1080_JPEG", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_WIN8UI_AUTO_TEST_DUALCAMERA_DUALPIN_SECONDARY_VIDEO_MAX_YUY2_PRIMARY_PHOTO_MAX_JPEG", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_WIN8UI_AUTO_TEST_DUALCAMERA_DUALPIN_SECONDARY_VIDEO_MAX_YUY2_PRIMARY_PHOTO_MAX_JPEG Camera_DualCamera_InOrder_DualPin_Secondary_Video_Max_YUY2_Primary_Photo_Max_JPEG", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_BASIC_PRIMARY_VIDEO_MAX_NV12_SECONDARY_VIDEO_MAX_NV12", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestDualCamSiglePin.py CAMERA_BASIC_PRIMARY_VIDEO_MAX_NV12_SECONDARY_VIDEO_MAX_NV12", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_WIN8UI_AUTO_TEST_DUALCAMERA_SAMETIME_PRIMARY_VIDEO_MIN_NV12_SECONDARY_VIDEO_MIN_YUY2", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_WIN8UI_AUTO_TEST_DUALCAMERA_SAMETIME_PRIMARY_VIDEO_MIN_NV12_SECONDARY_VIDEO_MIN_YUY2 Camera_DualCamera_SameTime_Primary_Video_Min_NV12_Secondary_Video_Min_YUY2", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_3A_DESKTOP_TORCH_PRIMARY_VIDEO_INDEPENDENT_FLASH_SEQUENTIAL", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTest3AMisc.py CAMERA_3A_DESKTOP_TORCH_PRIMARY_VIDEO_INDEPENDENT_FLASH_SEQUENTIAL", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_3A_DESKTOP_SHUTTER_SPEED_PRIMARY_PREVIEW", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTest3AMisc.py CAMERA_3A_DESKTOP_SHUTTER_SPEED_PRIMARY_PREVIEW", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_PRIMARY_API_NEW_0011", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_PRIMARY_API_NEW_0011 Primary TorchControl", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_SECONDARY_API_NEW_0005", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_SECONDARY_API_NEW_0005 Secondary IsoSpeedControl", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_MUTE_PRIMARY_STILL_MUTE_MODE", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestMuteMode.py CAMERA_MUTE_PRIMARY_STILL_MUTE_MODE", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_PERFORMANCE_PRIMARY_PREVIEW_NV12_VIDEO_1280x720_NV12", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestSingleCamDualPin.py CAMERA_PERFORMANCE_PRIMARY_PREVIEW_NV12_VIDEO_1280X720_NV12 Primary nv12 12000 video nv12 1280 720 12000 1", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_PERFORMANCE_SECONDARY_PREVIEW_NV12_VIDEO_640X360_NV12", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestSingleCamDualPin.py CAMERA_PERFORMANCE_SECONDARY_PREVIEW_NV12_VIDEO_640X360_NV12 Secondary nv12 12000 video nv12 640 360 12000 1", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_BASIC_DESKTOP_SECONDARY_RAW_1932X1092_GR10_1FPS", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestRawPin.py CAMERA_BASIC_DESKTOP_SECONDARY_RAW_1932X1092_GR10_1FPS", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_BASIC_DESKTOP_PRIMARY_RAW_4208X3120_GR10_1FPS", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestRawPin.py CAMERA_BASIC_DESKTOP_PRIMARY_RAW_4208X3120_GR10_1FPS", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_BASIC_DESKTOP_ZOOM_SECONDARY_VIDEO_NV12_640x480_DUALPIN", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestBasicControl.py CAMERA_BASIC_DESKTOP_ZOOM_SECONDARY_VIDEO_NV12_640x480_DUALPIN", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_BASIC_DESKTOP_EXPOSURE_PRIMARY_STILL_DUALPIN", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestBasicControl.py CAMERA_BASIC_DESKTOP_EXPOSURE_PRIMARY_STILL_DUALPIN", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_BASIC_DESKTOP_BRIGHTNESS_PRIMARY_STILL_DUALPIN", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestBasicControl.py CAMERA_BASIC_DESKTOP_BRIGHTNESS_PRIMARY_STILL_DUALPIN", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_BASIC_DESKTOP_ZOOM_PRIMARY_VIDEO_YUY2_1920x1080_DUALPIN", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestBasicControl.py CAMERA_BASIC_DESKTOP_ZOOM_PRIMARY_VIDEO_YUY2_1920x1080_DUALPIN", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_BASIC_DESKTOP_AWBMODE_MANUAL_PRIMARY_PREVIEW", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestBasicControl.py CAMERA_BASIC_DESKTOP_AWBMODE_MANUAL_PRIMARY_PREVIEW", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_MATEDATA_Auto_184", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/ImageMetadataCheck.py CAMERA_MATEDATA_Auto_184 Camera_Primary_Image_Metadata_Brightness_-1", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_WIN8UI_AUTO_PROFILE_CHECK_RESOLUTION_SECONDARY_VIDEOCONFERENCING", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_WIN8UI_AUTO_PROFILE_CHECK_RESOLUTION_SECONDARY_VIDEOCONFERENCING Camera_Profile_Check_Resolution_Secondary_VideoConferencing", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_WIN8UI_AUTO_SDV_BASIC_SECONDARY_VIDEO_1920X1080_YUY2_30FPS", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_WIN8UI_AUTO_SDV_BASIC_SECONDARY_VIDEO_1920X1080_YUY2_30FPS Camera_SDV_Basic_Secondary_Video_1920x1080_YUY2_30FPS", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_BASIC_SECONDARY_PREVIEW_1920X1080_NV12", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestSingleCamSiglePin.py CAMERA_BASIC_SECONDARY_PREVIEW_1920X1080_NV12", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_WIN8UI_AUTO_ENUMFORMAT_PRIMARY_PREVIEW_NV12", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_WIN8UI_AUTO_ENUMFORMAT_PRIMARY_PREVIEW_NV12 Camera_EnumFormat_Primary_Preview_NV12", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_SECONDARY_API_DSHOW_003", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/APITest/CameraDShowAPI.py CAMERA_SECONDARY_API_DSHOW_003 Secondary CAPTUREGRAPHBUILDER2 CopyCaptureFile", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_PRIMARY_API_DSHOW_003", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/APITest/CameraDShowAPI.py CAMERA_PRIMARY_API_DSHOW_003 Primary CAPTUREGRAPHBUILDER2 CopyCaptureFile", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_WIN10_Metadata_Secondary_Still_WhiteBalance", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/FeatureTestWin10Metadata.py Camera_Win10_Metadata_Secondary_Still_WhiteBalance", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_EPAC_AUTO_0009", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/ePac/ePac_Unicode_Check.py Camera_EPAC_AUTO_0009", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_EPAC_AUTO_0008", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/ePac/ePac_Binscope.py Camera_EPAC_AUTO_0008 checkinf", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_EPAC_AUTO_0003", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/ePac/ePac_Binscope.py Camera_EPAC_AUTO_0003 GSFriendlyInitCheck", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_EPAC_AUTO_0007", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/ePac/SymChkTest.py Camera_EPAC_AUTO_0007 dll", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
		  {
			 "executable": "C:/AutoBat/bat/Desktop/Scripts/ePac/ePAC_Check_Unnecessary_driver_file.bat", 
			 "name": "CAMERA_EPAC_AUTO_0010",
			 "parameters": "", 
			 "dependency": "CAMERA_SETUPENV_CAMERA_CHECK_DEVICE", 
			 "requires": {
				"named_req": "TARGET"
			 }, 
			 "repetition": 5,
			 "critical": false,
			 "timeout": 900,
			 "type": "subprocess",
			 "disabled": false
		  }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_EPAC_AUTO_0011", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/ePac/ePac_Binscope.py Camera_EPAC_AUTO_0011 GSCheck", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_PRIMARY_API_MF_025", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/APITest/CameraMFAPI.py CAMERA_PRIMARY_API_MF_025 Primary AdvExtControl ColorFX", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "executable": "C:/python27/python.exe", 
            "name": "CAMERA_SETUPENV_ENABLE_CAMERA_DRIVER_VERIFIER", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/DriverManagement/enableDriverVerify.py ENABLE_CAMERA_DRIVER_VERIFIER Camera", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "alwayspasses": true, 
            "dependency": "", 
            "critical": false, 
            "timeout": 900, 
            "repetition": 5, 
            "type": "subprocess", 
            "mustrun": false
        }, 
        {
            "executable": "cmd.exe", 
            "name": "CAMERA_SETUPENV_REBOOT_DUT_NOW", 
            "parameters": "/c shutdown /r /f /t 0", 
            "type": "subprocess", 
            "alwayspasses": true, 
            "timeout": 600, 
            "requires": {
                "named_req": "TARGET"
            }
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_SETUPENV_CHECK_VERIFIER_ENABLED", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/DriverManagement/enableDriverVerify.py CHECK_VERIFIER_ENABLED VerifyEnabled", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_DRIVER_INSTALL_0007", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/DriverManagement/TestCameraDriver.py CAMERA_DRIVER_INSTALL_0007 install Flash test", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_DRIVER_INSTALL_0017", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/DriverManagement/TestCameraDriver.py CAMERA_DRIVER_INSTALL_0017 disable ISP test", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_DRIVER_INSTALL_0039", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/DriverManagement/TestCameraDriver.py CAMERA_DRIVER_INSTALL_0039 disable Camera test", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_DRIVER_INSTALL_0018", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/DriverManagement/TestCameraDriver.py CAMERA_DRIVER_INSTALL_0018 disable Primary test", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_DRIVER_INSTALL_0020", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/DriverManagement/TestCameraDriver.py CAMERA_DRIVER_INSTALL_0020 disable Secondary test", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_DRIVER_INSTALL_0022", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/DriverManagement/TestCameraDriver.py CAMERA_DRIVER_INSTALL_0022 disable Flash test", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_DRIVER_INSTALL_0024", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/DriverManagement/TestCameraDriver.py CAMERA_DRIVER_INSTALL_0024 enable ISP test", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_DRIVER_INSTALL_0038", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/DriverManagement/TestCameraDriver.py CAMERA_DRIVER_INSTALL_0038 enable Camera test", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_DRIVER_INSTALL_0026", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/DriverManagement/TestCameraDriver.py CAMERA_DRIVER_INSTALL_0026 enable Primary test", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_DRIVER_INSTALL_0028", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/DriverManagement/TestCameraDriver.py CAMERA_DRIVER_INSTALL_0028 enable Secondary test", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_DRIVER_INSTALL_0030", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/DriverManagement/TestCameraDriver.py CAMERA_DRIVER_INSTALL_0030 enable Flash test", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "executable": "C:/python27/python.exe", 
            "name": "CAMERA_TUNIT_FW_DUMP_ISYS", 
            "parameters": "c:/AutoBAT/BAT/Desktop/scripts/CameraFWDump.py CAMERA_TUNIT_FW_DUMP_ISYS", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "alwayspasses": false, 
            "dependency": "", 
            "critical": false, 
            "timeout": 900, 
            "repetition": 5, 
            "type": "subprocess", 
            "mustrun": false
        }, 
        {
            "executable": "C:/python27/python.exe", 
            "name": "CAMERA_TUNIT_FW_DUMP_PSYS", 
            "parameters": "c:/AutoBAT/BAT/Desktop/scripts/CameraFWDump.py CAMERA_TUNIT_FW_DUMP_PSYS", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "alwayspasses": false, 
            "dependency": "", 
            "critical": false, 
            "timeout": 900, 
            "repetition": 5, 
            "type": "subprocess", 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_WIN8UI_AUTO_TEST_DUALCAMERA_SAMETIME_PRIMARY_VIDEO_MAX_YUY2_SECONDARY_VIDEO_MAX_YUY2", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_WIN8UI_AUTO_TEST_DUALCAMERA_SAMETIME_PRIMARY_VIDEO_MAX_YUY2_SECONDARY_VIDEO_MAX_YUY2 Camera_DualCamera_SameTime_Primary_Video_Max_YUY2_Secondary_Video_Max_YUY2", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_WIN8UI_AUTO_TEST_SWITCHCAMERA_SECONDARY_IMAGE_PRIMARY_VIDEO", 
            "parameters": "c:/AutoBAT/BAT/Metro/Scripts/RunStoreAppAutoTest.py CAMERA_WIN8UI_AUTO_TEST_SWITCHCAMERA_SECONDARY_IMAGE_PRIMARY_VIDEO Camera_SwitchCamera_Secondary_Image_Primary_Video", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_DRIVER_INSTALL_0033", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/DriverManagement/TestCameraDriver.py CAMERA_DRIVER_INSTALL_0033 uninstall Camera test", 
            "repetition": 5, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }, 
        {
            "executable": "C:/python27/python.exe", 
            "name": "CAMERA_SETUPENV_RESET_VERIFIER", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/DriverManagement/enableDriverVerify.py RESET_VERIFIER Reset", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "alwayspasses": true, 
            "dependency": "", 
            "critical": false, 
			"env": true, 
            "timeout": 900, 
            "repetition": 5, 
            "type": "subprocess", 
            "mustrun": false
        }, 
        {
            "executable": "C:/TWSTools/MapLogTWS.exe", 
            "name": "MapLogTWS", 
            "parameters": "", 
            "type": "subprocess", 
			"mustrun": true, 
            "timeout": 600, 
            "repetition": 1, 
            "requires": {
                "named_req": "TARGET"
            }
        }, 
        {
            "executable": "C:/python27/python.exe", 
            "name": "Copy_BATResults", 
            "parameters": "C:/TWSTools/CopyTWSResultsFolder.py \"C:/AutoBAT_Results\" \"L:\" \"%BuildConfig_Variable%\" \"%Build_No_Variable%\" \"%TARGET.id%\" {UUID}", 
            "type": "subprocess", 
            "timeout": 1800, 
			"mustrun": true, 
            "repetition": 1, 
            "requires": {
                "named_req": "TARGET"
            }
        }
    ], 
    "variables": {}, 
    "repetitions": 1, 
    "type": "TWS", 
    "requires": [
        {
            "controller!": "true", 
            "named_req": "TARGET", 
            "id": "UNNAMED", 
            "reserve": "true"
        }
    ]
}