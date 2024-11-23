from rocketmq.client import PushConsumer, ConsumeStatus
import time

def callback(msg):
    print(msg.id, msg.body,  msg.get_property('property'))
    return ConsumeStatus.CONSUME_SUCCESS

def start_consume_message():
    consumer = PushConsumer('consumer_group')
    consumer.set_name_server_address('192.168.194.100:9886')
    consumer.subscribe('TopicTest', callback)
    print ('开始消费消息')
    consumer.start()

    while True:
        time.sleep(3600)

if __name__ == '__main__':
    start_consume_message()