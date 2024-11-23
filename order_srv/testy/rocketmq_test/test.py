from rocketmq.client import Producer, Message, SendStatus

def create_message():
    msg = Message("hellormq")
    msg.set_property("name", "micro services")
    msg.set_keys("mall")
    msg.set_tags("python")
    msg.set_delay_time_level(2)  # 1s 5s 10s 30s 1m 2m 3m 4m 5m 6m 7m 8m 9m 10m 20m 30m 1h 2h
    msg.set_body("This is a test message".encode('utf-8'))  # Replace with your message content in bytes format
    return msg
def send_message(count):
    producer = Producer('test')
    producer.set_name_server_address('192.168.194.100:9886')  # Replace with your name server address
    producer.start()
    for i in range(count):  # Send 10 messages
        message = create_message()
        ret = producer.send_sync(message)
        print(f"发送消息状态:{ret.status},消息id：{ret.msg_id}")
    print("消息发送完成")
    producer.shutdown()

if __name__ == "__main__":
    send_message(2)