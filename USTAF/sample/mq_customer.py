# -*- coding: utf-8 -*-
"""
@Created mq_customer.py on 17-8-1 下午5:27
@Author: Gaobo.Xiao
@Version: ??
@license: Intel-ICG
"""
import pika
import traceback
import json

# from environment import Env
# from api import RestApi
# from config import *
import pdb

if __name__ == "__main__":
    credentials = pika.PlainCredentials('USTAF', 'Intel.123')
    QUEUE_NAME = 'APL_PV_PIT'
    parameters = pika.ConnectionParameters(host='10.239.111.152', port=5672, virtual_host='/',
                                           credentials=credentials, heartbeat_interval=600)  # ,connection_attempts =1440*15,retry_delay=60
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    print ' [*] Waiting for Rest API messages. To exit press CTRL+C'

    def callback(ch, method, properties, body):
        # env = Env.getInstance()
        try:
            print '111'
            mq_args = json.loads(body)
            print mq_args
            # status_code, result = RestApi().run('calc-cases', mq_args)
        except Exception as e:
            # env.log.error(str(traceback.format_exc()))
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return False
        ch.basic_ack(delivery_tag=method.delivery_tag)
        # env.log.info(" [x] Done")

    channel.basic_qos(prefetch_count=1000)
    channel.basic_consume(callback, queue=QUEUE_NAME)
    channel.start_consuming()

