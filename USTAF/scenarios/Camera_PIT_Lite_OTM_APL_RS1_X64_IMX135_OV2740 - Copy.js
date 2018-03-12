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
    "name": "Camera_PIT_Lite_OTM_APL_RS1_X64_IMX135_OV2740", 
	"test_type" : "PIT",
	"platform" : "APL",
    "tools": [
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_SETUPENV_CLEANAPPLOG", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/CleanUpMetroResult.py CLEANAPPLOG {BUILD_NUM}", 
            "failrerun": 0, 
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
            "timeout": 900, 			
            "mustrun": false
        },
		{
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_SETUPENV_CLEANAPPLOG", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/CleanUpMetroResult.py CLEANAPPLOG", 
            "failrerun": 0, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": true
        }
	]
}