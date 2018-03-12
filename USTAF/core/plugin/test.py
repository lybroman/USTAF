import socket, time, json

class SOCK(object):
    def __init__(self, address, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print address,port
        self.sock.connect((address, port))
        time.sleep(1)

    def communicate(self, cmd):
        self.sock.send(cmd)
        try:
            self.sock.settimeout(20)
            frag = self.sock.recv(1024)
            s = frag
            while len(frag) > 0:
                frag = self.sock.recv(1024)
                s += frag
            return s
        except self.sock.timeout:
            pass

        return s

    def finish(self):
        self.sock.close()


#s = SOCK('10.239.153.126', 10001)
s = SOCK('10.239.153.119', 10001)
'''
{"scenario_name":"Camera_PIT_Lite_OTM_APL_RS1_X64_IMX135_OV2740", "task_id":"0001", "BuildConfig_Variable":"PIT", "Build_No_Variable":"39059", "TARGET.id" : "APL_TEST", "patchset": "245863"}
{"scenario_name":"Camera_PIT_Lite_OTM_APL_RS1_X64_IMX135_OV2740", "task_id":"0001", "BuildConfig_Variable":"PIT", "Build_No_Variable":"39839", "TARGET.id" : "APL_TEST", "patchset": "247604/1", "os" : "windows"}
{"scenario_name":"Camera_PIT_Lite_OTM_APL_RS1_X64_IMX135_OV2740", "task_id":"0001", "BuildConfig_Variable":"PIT", "Build_No_Variable":"47837", "TARGET.id" : "APL_TEST", "patchset": "276057", "os" : "windows"}
{"scenario_name":"Linux_PIT_Lite_OTM_IVI_Yocto_x64_1xOV10640", "task_id":"0001", "BuildConfig_Variable":"PIT", "Build_No_Variable":"43545", "TARGET.id" : "APL_TEST", "patchset": "276057", "os" : "linux", "branch":"master"}
'''
print(s.communicate('{"option" : "QUEUE", "duts":["APL_TEST"]}'))
# print(json.loads(aa))
#aa = s.communicate('{"option" : "QUEUE", "duts":["10.239.132.227"]}')
#aa = json.loads(aa)
#print(aa['queue'][0][0])
#print s.communicate('{"option" : "REORDER", "queue":"APL_002_PV_CIT", "task_id": "789396f4"}')
#print s.communicate('{"option": "REORDER", "queue":"APL_OTM_CIT", "task_id":"0001"}')
#print s.communicate('{"option" : "QUERY", "duts":["10.239.132.227"]}')
# {"option" : "CANCEL", "dut": "", "queue":"", "task_id":""}
#print s.communicate('{"option" : "CANCEL", "queue":"APL_002_PV_CIT", "task_id": "789396f4"}')
# print s.communicate('{"option" : "DETAIL", "dut":"APL_TEST", "case_name" : "CAMERA_IR_DRIVER_INSTALL_0003"}')
# print s.communicate('{"option": "LATE_LOCK", "lock": true, "dut" : "APL_TEST"}')
#print s.communicate('{"option" : "PAAS", "dut":"10.239.132.227", "cases":["CAMERA_CHECK_CAMERA_POSITION_PRIMARY_PREVIEW_NV12_STILL_MAX_NV12", "CAMERA_CHECK_CAMERA_POSITION_SECONDARY_PREVIEW_NV12_STILL_MAX_NV12"], "name" : "pit_as_a_service"}')

# print s.communicate('{"option": "UPDATE", "dut": "APL_123", "dut_name":"APL_123", "test_type":["CIT"], "branch":["OTM"]}')
# print s.communicate('{"option" : "111", "dut":"APL_TEST", "lock": false}')
s.finish()

'''
import rabbitpy, traceback

config={"rabbitMQ_address":"127.0.0.1", "rabbitMQ_port":"5672"}
try:
    with rabbitpy.Connection(
            'amqp://guest:guest@{}:{}/%2F'.format(config["rabbitMQ_address"], config["rabbitMQ_port"])) as conn:
        with conn.channel() as channel:

            # modify i & q according to true info
            i = {"scenario_name":"Camera_CIT_OTM_APL_RS1_X64_IMX135_OV2740", "task_id":"0001", "BuildConfig_Variable":"PIT", "Build_No_Variable":"39839", "TARGET.id" : "APL_TEST", "patchset": "247604/1", "os" : "windows"}
            i = str(i)
            queue = 'test queue'

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
'''