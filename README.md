
----------

## 1. Introduction ##

USTAF(**U**ltra **S**oftware **T**est **A**utomation **F**ramework) is a **XOS** test automation framework which supports both **centralized** and **decentralized** working mode. It has a all-round testcase level control which guarantees the stability and accuracy of testcase execution. Also it provides a high level management for testsuite.

USTAF is designed for Validation teams that are willing to implement 7*24 automation test for validation or integration. USTAF has extreme flexibility on the execution process control. You could easily collaborate it with your build system, code review system, and CI system.

USTAF is written in Python(2.7) and the GUI is  built with QT. To deploy it, you also need to install STAF(IBM open source project which provided the basic service apis), RabbitMQ， MySQL as well as some other 3rd party packages.

## 2. Design Overview ##

For centralized mode, the engineer does not need to touch the GUI, instead some high-level web server framework could communicate with the USTAF interfaces (you need to build the source code based on your platform, e.g. using py2exe to build an executable on Windows and enable the server for socket communication) or just integrate it into your web framework! And thus the end users could directly work on the dashboard.
For decentralized mode, the engineer could directly use it as a GUI tool(you need to build the source code based on your platform, e.g. using py2exe to build an executable on Windows)
![Usage Model for USTAF](http://upload-images.jianshu.io/upload_images/9304106-19953ad735e2c881.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

As you could see in the above figure, the engineer could directly logon to a host with USTAF to execute tasks, also the end users could execute the same operation from the Web UI as long as it is connected to the USTAF server. On the right side of the figure, it has listed(but not limited to) some typical devices that could be tested with the framework.

Since you should already have a brief idea of what USTAF is, let's have a more deep dive into the architecture of  USTAF itself.
![USTAF Architecture](http://upload-images.jianshu.io/upload_images/9304106-9596c574f85f44ab.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
As in the above figure,  when the engineer push a patch to code review system(e.g.,  gerrit), once this patch is approved, it should trigger a build(or in other words, some release to be tested in a certain device/platform). When the build is ready to be tested, the build system could schedule a task in the queue system of USTAF(implemented with RabbitMQ, you need to define the payload of the task which could be further used in the execution, perhaps some environment variables).
Here we have a concept of device pools which group the devices of same platforms and test purpose. When any device in the pool is idle, USTAF will fetch a task from the matched queue for that device to execute the test task. The benefit of pool is to balance the workload. However if you want to trigger some test on a certain device, just make the queue  only have that device. You could have multiple device pools.
The task is testsuite based.  A testsuite could contain any numbers of testcases. And a testcase could be executed more than once based on the run-time conditions and configuration parameters.
Also there could be some post-processing after each cases, such as device reboot , test log analysis  and even bug isolation based on bug systems.
There are lots of sockets interfaces which could support same functionalities on GUI on WEB UI. Also you could call these apis to extract run-time data about the executions. By design, a email report would be sent if task has finished.
Moreover, you could adjust the order of scheduled tasks as well as cancel some tasks.  
## 3. Testsuite/Scenario Definitions ##
The testsuite is a very important part of the framework though it is a standalone JSON File. The structure looks like below:
```
{
    "name": "TESTSUITE_NAME", 
    "test_type" : "PIT_LITE",
    "platform" : "TEST_PLATFORM",
    "subversion" : "SUBVERSION",
    "mail_list" : ["Joe.Doe@example.com"],
    "tools": [
        {
            "executable": "C:/python27/python.exe", 
            "name": "TESTCASE_NAME_0", 
			"parameters": "TEST_PARAMETERS",
        },
      {
            "executable": "C:/python27/python.exe", 
            "name": "TESTCASE_NAME_1", 
			"parameters": "TEST_PARAMETERS",
        }
    ]
}
```
As shown above, that's the very simple structure of a testsuite(tc)/scenario. Actually you could modify the code easily to enable more configuration parameters as well. But based on the original design(business process when I develop this framework), it does look like this way. All the testcase(ts) items are listed in the "tools". For supported configuration parameters and the corresponding definitions, please refer to below tables:

|Tag|Hierarchy|Definitions|Type|Comments|
| - | - | - | - | - |
|name|ts|name of the ts|str||
|test_type|ts|test type for the ts|str|define it base on your biz|
|platform|ts|platform for the ts|str|define it base on your biz|
|subversion|ts|subversion for the ts|str|define it base on your biz|
|mail_list|ts|list of receivers of the report|list||
| gating_fail_rate | ts | test would be cancelled if fail rate larger than the threshold | int | default is 1.1 so if not set, no side effect |
| collateral | ts | before the execution of the first cases, the files of list[i][0] would be copied to list[i][1]|list[list[]] | these file syncs would help copy some test environment related files or executables |
| root_artifacts_path| ts | a base shared path used for biz purpose | str | default value is hard-coded, please redefine it base on your biz |
| executable | tc | executable + parameters  = case cmdline | str | e.g., C:/python27/python.exe or cmd.exe on Windows platforms |
| name | tc | name of the tc | str | supposed to be all uppercases |
| parameters | tc | executable + parameters  = case cmdline | str | e.g., C:/Test/test-sanity.py -a 5 -b 6 on Windows platforms|
| dependencies | tc | a list of tc name, if any of them failed, this tc would not be executed | list[tc_name] | |
| critical | tc | if True and tc failed, following tcs would be cancelled | bool | except for mustrun tc |
| failrerun | tc | if first run failed, tc would rerun until pass or larger than set value| int | default is 0, namely no rerun |
| repetition | tc | if first run failed, tc would rerun until larger than set value and between each rerun, a reboot would be triggered| int | reboot is a good way to clean the test environment. Repetition is designed for majority vote strategy.|
| mustrun | tc | even critical tc failed, tc with mustrun is True would be executed | bool | some environment cleanup or log copy tc should be marked as True |
| alwayspasses | tc | whatever the result is, tc would be shown as pass | bool |  |
| env | tc | any environment setup tc should mark this tag as True | bool |  |
| sleeptime | tc | sleep set value before execute next tc | int | in second |
| pass_bypass | tc | if any tc in the list passed, this tc would not be executed| list[tc_name] | |
## 4. Basic Usages ##
Once you have all things ready(refer to section 7 for how to setup), you could launch USTAF on your platform, the following example is based on the executable built for Windows.
1. Double Click the executable to launch USTAF:
![main-window](http://upload-images.jianshu.io/upload_images/9304106-315223f9e80c179e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

|Button|Behavior|Comments|
| - | - | - |
|Group Editor| Add a device group/pool|Note: the pool is not defined here, it is in device configuration page instead|
|Refresh DUT status|Not implemented yet| you could refresh the device in the menu for each dut, DUT is Device Under Test, just a terminology in our biz|
|Load Workspace| Load a configuration from file| Load all the devices and scenarios configurations|
|Save Workspace| Save a configuration to file| Save all the devices and scenarios configurations|
|Start Listener| Start the socket server listener| Start socket listener server with the port specified in server configuration|
|Configure Server| Configure some basic parameters| RabbitMQ server IP & Port, Socket Port, log configuration and etc.|

2. Add your device group and add scenarios for each device you have added. 
3. Click the Start Listener Button on main window. This would enable communication with your web server framework.
4. Click the start button for EACH device in the device window. This would enable the communication with RabbitMQ to fetch a task when it is idle. This step could be done via socket interface.
5. The device pool is determined by `[project_code]_[branch]_[test_type]`, thus a device could belong to multiple pools. And each pool is connected to a queue with same name`[project_code]_[branch]_[test_type]`. Thus when any device is idle, it would search the queue with order to fetch next task.
![pool.PNG](http://upload-images.jianshu.io/upload_images/9304106-86c9941820bec89c.PNG?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

6. The task is in JSON format and looks like below:
```
{"scenario_name":"Linux_PIT_Lite_Some_Test_Scenario", "task_id":"0001", 
"BuildConfig_Variable":"PIT", "Build_No_Variable":"43545",
 "TARGET.id" : "APL_TEST", "patchset": "276057", "os" : "linux", "branch":"master"}
```
Note that all the parameters could be customized depends on your own biz and thus you need to change the code accordingly. The default behavior is that before each case, the framework would set the (key, value) pairs as environment variables. What's more, the "scenario_name" is critical as it defines which testsuite to be triggered.
A script to schedule such task to a certain queue could be:
```
import rabbitpy, traceback

config={"rabbitMQ_address":"127.0.0.1", "rabbitMQ_port":"5672"}
try:
    with rabbitpy.Connection(
            'amqp://guest:guest@{}:{}/%2F'.format(config["rabbitMQ_address"], config["rabbitMQ_port"])) as conn:
        with conn.channel() as channel:

            # modify i & q according to true info
            
            i =  "scenario_name":"Linux_PIT_Lite_Some_Test_Scenario", "task_id":"0001", 
                  "BuildConfig_Variable":"PIT", "Build_No_Variable":"43545",
                  "TARGET.id" : "APL_TEST", "patchset": "276057", "os" : "linux", "branch":"master"}
          
            queue = 'Project_PIT_OTM'

            q = rabbitpy.Queue(channel, queue)
            q.durable = True
            q.declare()
            channel.enable_publisher_confirms()

            msg = rabbitpy.Message(channel, i)

            if msg.publish("", queue, mandatory=True):
                print 'Message: "{}" publish confirmed by RabbitMQ'.format(msg.body)
            else:
                print 'Message: "{}" publish not confirmed by RabbitMQ'.format(msg.body)
                # TODO. should resend it...
except:
    print traceback.format_exc()
```
The RabbitMQ view via web UI is as below:
![queue-view](http://upload-images.jianshu.io/upload_images/9304106-e11e3c721d73b660.PNG?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

7. More
There are lots of features on the UI(there are corresponding interfaces as well) and you could try left click/right click/double click to explore them~
![main-window-with-devices](http://upload-images.jianshu.io/upload_images/9304106-4fa5bf029dab246b.PNG?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![device-window](http://upload-images.jianshu.io/upload_images/9304106-1aa4f04c09a05920.PNG?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![run-time-logs-and-status](http://upload-images.jianshu.io/upload_images/9304106-c93dbf9a41f3f14d.PNG?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 5. Report Definitions ##
The Email report looks like as below:
![Sample Email Report](http://upload-images.jianshu.io/upload_images/9304106-354c70307313dfb5.PNG?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
There are are some basic information in the first table whose meaning are quite clear. In the second table, there are would be some additional information regarding to the integration, testing and DUT.  A typical table with detailed information is as below:
![Report with additional Data](http://upload-images.jianshu.io/upload_images/9304106-f78bf5799c0bc847.PNG?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
Definitely, you need and have to customize the definitions of this table so as to show whatever you want.
In the third table, it contains the test results of each case. Some definitions in this tables are as below(you could find them in the source code as well):

    NotRun =     0b00000000
    TBD =        0b00000001
    Fail =       0b00000010 
    Pass =       0b00000100
    ReRunPass =  0b00001000
    ReAddPass =  0b00010000
    RepeatPass = 0b00100000
    Bypass =     0b01000000
    AlwaysPass = 0b10000000

    NORMAL =            0b000000000000000
    WARM_REBOOT =       0b000000000000001
    COLD_REBOOT =       0b000000000000010
    REBOOT_RECOVERY =   0b000000000000100
    INITIAL_REBOOT =    0b000000000001000
    MANUAL_CANCEL =     0b000000000010000
    ERROR =             0b000000000100000
    DEPENDENCY_FAIL =   0b000000001000000
    CRITICAL_FAIL =     0b000000010000000
    TBD =               0b000000100000000
    HANG_TO =           0b000001000000000
    PASS_BYPASS =       0b000010000000000
    CONNECTION_LOSS =   0b000100000000000
    ENV_FAILURE =       0b001000000000000
    BSOD =              0b010000000000000
    ReRun =             0b100000000000000

|Case Result|Definitions|
| - | - |
|NotRun| The case is not executed|
| TBD | case not passed in the first time but do have rerun |
| Fail | The case failed |
| Pass | The case passed without any rerun |
| ReRunPass | The case passed with rerun |
|ReAddPass| Reserved status, not implemented |
|RepeatPass| The case passed with fail-repetition |
|Bypass| The case is bypassed due to pass-bypass |
|AlwaysPass| The case is marked as always pass |

Below are some events that might happen during the executions (some are reserved but not implemented).
|Event|Definitions|
| - | - |
| NORMAL | Nothing unexpected happened |
| WARM_REBOOT | warm reboot is triggered |
| COLD_REBOOT | cold reboot is triggered |
|  REBOOT_RECOVERY | DUT recovered from cold reboot |
| INITIAL_REBOOT | Framework triggered a reboot for DUT |
| MANUAL_CANCEL | case/scenario is cancelled |
| ERROR | Something unexpected happened |
| DEPENDENCY_FAIL | The case's dependency cases failed |
| CRITICAL_FAIL | The case is critical and it failed |
| TBD | The case could be marked as pass, but this tag would appear if the case finished in very short time and has little logs |
| HANG_TO | The DUT is hang or case timeout|
| PASS_BYPASS | The case is bypassed as expected |
| CONNECTION_LOSS | Unstable network |
|ENV_FAILURE | The case is environment-setup case and it failed|
| BSOD | Blue Screen of Death |
| ReRun | The case was rerun |

Definitely, you need and have to customize the definitions of this table so as to show whatever you want.
What's more there would be one excel and log file attached in the email. In the excel there would be extra error logs parsed from the log analysis modules. In the log file, it documented the stdout/stderr for all the cases. With these two files, it would be easy for you to debug.
## 6. Socket Interface Definitions ##
As mentioned above, the framework provide several socket api for communications. The definitions are as below:
![Socket APIs Check List](http://upload-images.jianshu.io/upload_images/9304106-5257aac0b74872c3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
You might need to go through the code if you want to fully understand the apis.
## 7. Requirements and Setup ##
1. You need to install the STAF and select the right Python version both on server and DUT.
2. Add the USTAF path to the python installation folder with a .pth file.
3. It is good to go now, just click the main.py!
4. Alternatively you could build it as an executable for you platform.
## 8. Useful Links ##
· **IBM Wiki**: [http://www.ibm.com/developerworks/library/os-test-stafstax/](http://www.ibm.com/developerworks/library/os-test-stafstax/)
· **Source**: [http://staf.sourceforge.net/](http://staf.sourceforge.net/)
