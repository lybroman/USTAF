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
    "name": "error_log_analysis", 
	"test_type" : "PIT_LITE",
	"platform" : "TestPlatform",
    "tools": [
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_IR_DRIVER_INSTALL_0003", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/abc.py CAMERA_IR_DRIVER_INSTALL_0003", 
            "failrerun": 0, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
			"failrerun":3,
            "mustrun": false
        },
		{
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "CAMERA_IR_DRIVER_INSTALL_0011", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/abc.py CAMERA_IR_DRIVER_INSTALL_0011", 
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
            "name": "CAMERA_IR_DRIVER_INSTALL_0018", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/abc.py CAMERA_IR_DRIVER_INSTALL_0018", 
            "failrerun": 0, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
			"sleeptime":0,
            "mustrun": false
        }
	]
}