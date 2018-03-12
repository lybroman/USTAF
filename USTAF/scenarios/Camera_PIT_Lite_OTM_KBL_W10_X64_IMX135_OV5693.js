{
	"type" : "PIT",
	"platform" : "IPU4",
	"subversion" : "APL_RS1",
	"collateral": [
        [
            "http://SHWDEJOINTD221.sample.com:7073/api/service/content/Camera/SmartCopyTWS.exe",
            "C:/TWSTools/SmartCopyTWS.exe", 
            "", 
            ""
        ], 
        [
            "http://SHWDEJOINTD221.sample.com:7073/api/service/content/Camera/CameraTestSetEntryTWS.py",
            "C:/TWSTools/CameraTestSetEntryTWS.py", 
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
    "name": "Camera_PIT_Lite_OTM_KBL_W10_X64_IMX135_OV5693", 
    "tools": [
        {
         "executable": "cmd.exe", 
         "name": "CAMERA_SETUPENV_PIT_KBL_THX64_IMX135_OV5693",
         "parameters": "/c notepad", 
         "dependency": [], 
         "failrerun": 1,
         "critical": true,
         "timeout": 180,
          "repetition": 1
	    }
    ]
}