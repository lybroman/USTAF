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
	"test_type" : "PIT",
	"platform" : "APL",
    "tools": [
        {
            "dependency": "", 
            "executable": "C:/python27/python.exe", 
            "critical": false, 
            "name": "TEST_ERROR_LOG", 
            "parameters": "c:/AutoBAT/BAT/Desktop/Scripts/XXX.py TEST_ERROR_LOG", 
            "failrerun": 0, 
            "type": "subprocess", 
            "requires": {
                "named_req": "TARGET"
            }, 
            "timeout": 900, 
            "mustrun": false
        }
	]
}