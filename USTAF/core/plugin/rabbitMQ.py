import pika
import rabbitpy
import time, os, sys, uuid, json, traceback
from USTAF.core.logger import LOGGER
g_username = "USTAF"
g_password = "sample.123"


def queryTask(config, device_id, project_code, test_type, branch):
    try:
        with rabbitpy.Connection('amqp://{}:{}@{}:{}/%2F'.format(g_username, g_password, config["rabbitMQ_address"], config["rabbitMQ_port"])) as conn:
            with conn.channel() as channel:
                # dedicated queue would be consumed firstly
                q = rabbitpy.Queue(channel, device_id)
                q.durable = True
                q.declare()
                if q.__len__() > 0:
                    msg = q.get()
                    msg.ack()
                    return json.loads(msg.body)

                # common queue would be consumed according to priority
                for t in test_type:
                    for b in branch:
                        q = rabbitpy.Queue(channel, '{}_{}_{}'.format(project_code, b, t))
                        q.durable = True
                        q.declare()
                        if q.__len__() > 0:
                            msg = q.get()
                            msg.ack()
                            return json.loads(msg.body)
    except:
        LOGGER.critical(traceback.format_exc())
        return None


def queryTask1(config, device_id, project_code, test_type, branch):
    try:
        # check dedicated queue firstly
        credentials = pika.PlainCredentials(g_username, g_password)
        params = pika.ConnectionParameters(config["rabbitMQ_address"],
                                  config["rabbitMQ_port"], '/', credentials)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        queue = channel.queue_declare(queue=device_id,  durable=True)
        if queue.method.message_count > 0:
            method_frame, header_frame, body = channel.basic_get(device_id)
            if method_frame:
                channel.basic_ack(method_frame.delivery_tag)
                return json.loads(body)
            else:
                LOGGER.warning('No message returned')

        for t in test_type:
            for b in branch:
                q_name = '{}_{}_{}'.format(project_code, b, t)
                queue = channel.queue_declare(queue=q_name, durable=True)
                if queue.method.message_count > 0:
                    method_frame, header_frame, body = channel.basic_get(q_name)
                    if method_frame:
                        channel.basic_ack(method_frame.delivery_tag)
                        return json.loads(body)
                    else:
                        LOGGER.warning('No message returned')
    except:
        print traceback.format_exc()
        LOGGER.error(traceback.format_exc())
    return None


def getDedicatedTaskQueue(config, device_id):
    tasks = []
    try:
        with rabbitpy.Connection('amqp://{}:{}@{}:{}/%2F'.format(g_username, g_password, config["rabbitMQ_address"],
                                                                 config["rabbitMQ_port"])) as conn:
            with conn.channel() as channel:
                # dedicated queue would be consumed firstly
                q = rabbitpy.Queue(channel, device_id)
                q.durable = True
                q.declare()
                if q.__len__() == 0:
                    return []
                else:
                    for i in range(0, q.__len__()):
                        msg = q.get()
                        tasks.append(msg.body)
    except:
        LOGGER.error(traceback.format_exc())
    return tasks


def getDedicatedTaskQueue_pika(config, device_id):
    # check dedicated queue firstly
    tasks = []
    task_to_nack = []
    try:
        credentials = pika.PlainCredentials(g_username, g_password)
        params = pika.ConnectionParameters(config["rabbitMQ_address"],
                                           config["rabbitMQ_port"], '/', credentials)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        queue = channel.queue_declare(queue=device_id, durable=True)

        for m in range(queue.method.message_count):
            method_frame, header_frame, body = channel.basic_get(device_id)
            if method_frame:
                tasks.append(json.loads(body))
                task_to_nack.append(method_frame.delivery_tag)

        for t in task_to_nack:
            channel.basic_nack(t)
    except:
        for t in task_to_nack:
            channel.basic_nack(t)
        LOGGER.error(traceback.format_exc())

    return tasks

def cancelTask_pika(config, queue_id, task_id):
    task_to_nack = []
    try:
        credentials = pika.PlainCredentials(g_username, g_password)
        params = pika.ConnectionParameters(config["rabbitMQ_address"],
                                           config["rabbitMQ_port"], '/', credentials)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        queue = channel.queue_declare(queue=queue_id, durable=True)
        rc = -1
        _target_delivery_tag = ''
        for m in range(queue.method.message_count):
            method_frame, header_frame, body = channel.basic_get(queue_id)
            if method_frame:
                task = json.loads(body)
                if task.get('task_id', 'not_a_valid_id') == task_id:
                    # channel.basic_ack(method_frame.delivery_tag)
                    _target_delivery_tag = method_frame.delivery_tag
                    rc = 0
                    LOGGER.warning("cancellation op will ack: {}".format(task))
                    break
                else:
                    task_to_nack.append(method_frame.delivery_tag)
                    LOGGER.warning("cancellation op will not ack: {}".format(task))
                    #channel.basic_nack(method_frame.delivery_tag)
        else:
            rc = -1

        # task_to_nack = (_ for _ in task_to_nack)
        for t in task_to_nack:
            channel.basic_nack(t)

        channel.basic_ack(_target_delivery_tag)

    except:
        for t in task_to_nack:
            channel.basic_nack(t)
        LOGGER.error(traceback.format_exc())
        rc = -2

    return rc

def cancelTask(config, queue, task_id):
    import threading
    lock = threading.Lock()
    lock.acquire()
    rc = 0
    try:
        with rabbitpy.Connection('amqp://{}:{}@{}:{}/%2F'.format(g_username, g_password, config["rabbitMQ_address"],
                                                                 config["rabbitMQ_port"])) as conn:
            with conn.channel() as channel:
                # dedicated queue would be consumed firstly
                q = rabbitpy.Queue(channel, queue)
                q.durable = True
                q.declare()
                channel.enable_publisher_confirms()
                _t = []
                for i in range(0, q.__len__()):
                    msg = q.get()
                    task = json.loads(msg.body)
                    if task["task_id"] == task_id:
                        msg.ack()
                        break
                else:
                    rc = -1
    except:
        LOGGER.error(traceback.format_exc())
        rc = -1
    finally:
        lock.release()
    return rc


def moveToTop_pika(config, queue_id, task_id):
    task_to_requeue = []
    try:
        credentials = pika.PlainCredentials(g_username, g_password)
        params = pika.ConnectionParameters(config["rabbitMQ_address"],
                                           config["rabbitMQ_port"], '/', credentials)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        queue = channel.queue_declare(queue=queue_id, durable=True)
        rc = -1
        _target = ''
        for m in range(queue.method.message_count):
            method_frame, header_frame, body = channel.basic_get(queue_id)
            data = json.loads(body)
            if data.get('task_id', 'not_a_valid_id') == task_id:
                _target = body
            else:
                task_to_requeue.append(body)

            channel.basic_ack(method_frame.delivery_tag)

        if _target:
            rc = 0
            task_to_requeue.insert(0, _target)

        for t in task_to_requeue:
            channel.basic_publish(body=t, exchange='', routing_key=queue_id)
    except:
        LOGGER.error(traceback.format_exc())
        rc = -2

    return rc

def moveToTop(config, queue, task_id):
    import threading
    lock = threading.Lock()
    lock.acquire()
    rc = 0
    try:
        with rabbitpy.Connection('amqp://{}:{}@{}:{}/%2F'.format(g_username, g_password, config["rabbitMQ_address"],
                                                                 config["rabbitMQ_port"])) as conn:
            with conn.channel() as channel:
                # dedicated queue would be consumed firstly
                q = rabbitpy.Queue(channel, queue)
                q.durable = True
                q.declare()
                channel.enable_publisher_confirms()
                _t = []
                _r = ''
                for i in range(0, q.__len__()):
                    msg = q.get()
                    msg.ack()
                    task = json.loads(msg.body)
                    if task["task_id"] == task_id:
                        _r = msg.body
                    else:
                        _t.append(msg.body)
                _t.insert(0,_r)

                for i in _t:
                    msg = rabbitpy.Message(channel, i)
                    # Publish the message, looking for the return value to be a bool True/False
                    if msg.publish("", queue, mandatory=True):
                        LOGGER.debug('Message {} publish confirmed by RabbitMQ'.format(msg.body))
                    else:
                        LOGGER.error('Message {} publish not confirmed by RabbitMQ'.format(msg.body))
                        rc = -1
    except:
        LOGGER.error(traceback.format_exc())
        rc = -1
    finally:
        lock.release()
    return rc

#print queryTask({"rabbitMQ_address":'127.0.0.1', 'rabbitMQ_port':5672}, '127.0.0.1', 'APL', ['PIT', 'CIT'], ['OTM', 'PV'])
#print queryTask1({"rabbitMQ_address":'10.239.111.152', 'rabbitMQ_port':5672},"10.239.132.227", "APL",["CIT", "PIT"], ["OTM", "PV"])
#a = getDedicatedTaskQueue({"rabbitMQ_address":'10.239.153.126', 'rabbitMQ_port':5672},"10.239.132.227")
#b = getDedicatedTaskQueue_pika({"rabbitMQ_address":'10.239.153.126', 'rabbitMQ_port':5672},"APL_OTM_CIT")
#print(type(b[0]), b)