from rocketmq.client import Producer, Message, TransactionMQProducer, TransactionStatus

import time
import threading

topic = 'TopicTest'
gid = 'test'
name_srv = '192.168.194.100:9886'
MUTEX = threading.Lock()

def create_message():
    msg = Message(topic)
    msg.set_keys('mall')
    msg.set_tags('python')
    msg.set_property('name', 'micro services')
    msg.set_body('微服务开发')
    return msg


def send_message_sync(count):
    producer = Producer(gid)
    producer.set_name_server_address(name_srv)
    producer.start()
    for n in range(count):
        msg = create_message()
        ret = producer.send_sync(msg)
        print ('发送消息状态: ' + str(ret.status) + ' msgId: ' + ret.msg_id)
    print ('发送消息成功')
    producer.shutdown()


def send_message_multi_threaded(retry_time):
    producer = Producer(gid)
    producer.set_name_server_address(name_srv)
    msg = create_message()

    global MUTEX
    MUTEX.acquire()
    try:
        producer.start()
    except Exception as e:
        print('ProducerStartFailed:', e)
        MUTEX.release()
        return

    try:
        for i in range(retry_time):
            ret = producer.send_sync(msg)
            if ret.status == 0:
                print('发送消息状态: ' + str(ret.status) + ' msgId: ' + ret.msg_id)
                break
            else:
                print('send message to MQ failed.')
            if i == (retry_time - 1):
                print('send message to MQ failed after retries.')
    except Exception as e:
        print('ProducerSendSyncFailed:', e)
    finally:
        producer.shutdown()
        MUTEX.release()
        return


def send_orderly_with_sharding_key(count):
    producer = Producer(gid, True)
    producer.set_name_server_address(name_srv)
    producer.start()
    for n in range(count):
        msg = create_message()
        ret = producer.send_orderly_with_sharding_key(msg, 'orderId')
        print ('send message status: ' + str(ret.status) + ' msgId: ' + ret.msg_id)
    print ('send sync order message done')
    producer.shutdown()


def check_callback(msg):
    print ('事务消息回查: ' + msg.body.decode('utf-8'))
    return TransactionStatus.COMMIT


def local_execute(msg, user_args):
    print ('本地执行:   ' + msg.body.decode('utf-8'))
    return TransactionStatus.UNKNOWN


def send_transaction_message(count):
    producer = TransactionMQProducer(gid, check_callback)
    producer.set_name_server_address(name_srv)
    producer.start()
    for n in range(count):
        msg = create_message()
        ret = producer.send_message_in_transaction(msg, local_execute, None)
        print ('发送消息状态: ' + str(ret.status) + ' 消息id: ' + ret.msg_id)
    print ('发送消息成功')

    while True:
        time.sleep(3600)


if __name__ == '__main__':
    send_transaction_message(1)