python shell 生成proto文件命令

`python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I . user.proto`

user_pb2_grpc.py里面的`import user_pb2 as user__pb2`要改成 `from . import user_pb2 as user__pb2` 要不然识别不了


安装rocketmq-client-python时要确保rocketmq-client-cpp版本要为最新版本，当前版本2.2.0：
wget https://github.com/apache/rocketmq-client-cpp/releases/download/2.2.0/rocketmq-client-cpp-2.2.0-centos7.x86_64.rpm
sudo rpm -ivh rocketmq-client-cpp-2.2.0-centos7.x86_64.rpm