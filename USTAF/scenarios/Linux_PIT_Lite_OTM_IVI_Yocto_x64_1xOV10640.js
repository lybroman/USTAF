{
   "name": "Linux_PIT_Lite_OTM_IVI_Yocto_x64_1xOV10640",
   "test_type" : "PIT_LITE",
   "platform" : "IPU4-APL-Linux",   
   "subversion" : "IVI",
   "mail_list" : ["yubo.li@sample.com"],
   "base_share_path": "\\\\10.239.132.71\\icg_sh_share\\AUTO\\Logs\\linux_pit_lite",
   "root_artifacts_path": "\\\\10.239.132.71\\icg_sh_share\\AUTO\\Logs",
   "tools": [
	  {
         "executable": "",
         "name": "UPDATE_AUTO_TEST_PACKAGE",
         "parameters": "/usr/local/staf/sync_auto_package.sh %branch%",
         "dependency": "",
         "requires": {
            "named_req": "TARGET"
         },
         "failrerun": 1,
         "critical": true,
         "alwayspasses": false,
         "timeout": 3600,
		 "env": true,
         "type": "subprocess"
      },
      {
         "executable": "",
         "name": "SET_UP_WITH_CI_BUILD",
         "parameters": "/home/root/sw_val/scripts/tools/ci_build_set_up.sh %Build_No_Variable% EMMC TSD_Full",
         "dependency": "",
         "requires": {
            "named_req": "TARGET"
         },
         "failrerun": 1,
         "critical": true,
         "alwayspasses": false,
         "timeout": 7200,
		 "env": true,
         "type": "subprocess"
      },
      {
         "executable": "",
         "name": "REBOOT",
         "parameters": "echo `hostname` > /dev/tcp/10.239.140.27/52587",
         "dependency": "",
         "requires": {
            "named_req": "TARGET"
         },
         "failrerun": 1,
         "critical": true,
         "alwayspasses": true,
         "timeout": 300,
         "sleeptime": 100,
		 "env": true,
         "type": "subprocess"
      },

	  {
         "executable": "",
         "name": "CAMERA_FUNCTION_OV10640_AUTO_ULL_BASIC_CAPTURE_SINGLE_CAM_USERPTR_1280x1080_NV12",
         "parameters": "/home/root/sw_val/scripts/gstCaff_auto.sh CAMERA_FUNCTION_OV10640_AUTO_ULL_BASIC_CAPTURE_SINGLE_CAM_USERPTR_1280x1080_NV12",
         "dependency": "",
         "requires": {
            "named_req": "TARGET"
         },
         "failrerun": 1,
         "critical": false,
         "alwayspasses": false,
         "sleeptime": 0,
         "timeout": 120,
         "repetition": 3,
         "type": "subprocess"
      },
       {
         "executable": "",
         "name": "CAMERA_FUNCTION_OV10640_AUTO_HDR_BASIC_CAPTURE_SINGLE_CAM_USERPTR_1280x1080_NV12",
         "parameters": "/home/root/sw_val/scripts/gstCaff_auto.sh CAMERA_FUNCTION_OV10640_AUTO_HDR_BASIC_CAPTURE_SINGLE_CAM_USERPTR_1280x1080_NV12",
         "dependency": "",
         "requires": {
            "named_req": "TARGET"
         },
         "failrerun": 1,
         "critical": false,
         "alwayspasses": false,
         "sleeptime": 0,
         "timeout": 120,
         "repetition": 3,
         "type": "subprocess"
      },
      {
         "executable": "sh",
         "name": "Upload_Test_Result_Folder",
         "parameters": "/home/root/sw_val/scripts/tools/upload_test_logs.sh \"%BuildConfig_Variable%\" \"%Build_No_Variable%\" \"%TARGET.id%\" \"%UUID%\"",
         "requires": {
            "named_req": "TARGET"
         },
         "repetition": 1,
         "timeout": 300,
         "alwayspasses": true,
         "mustrun": true,
         "type": "subprocess"
      }
   ],
   "requires": [
      {
         "controller!": true,
         "named_req": "TARGET",
         "id": "UNNAMED",
         "reserve": true
      }
   ]
}
