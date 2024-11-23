srv_name="user_srv_server"

chmod +x ./$srv_name.py
#重启，如果已经存在则关闭重启
PIDS=`ps -ef | grep ${srv_name} | grep -v grep | awk 'print $2'`
if [ "$PIDS" != "" ];
then
    echo "${srv_name} is already running."
    echo "shutting down ${srv_name}"
    if ps -aux | grep $srv_name | awk '{print $2}' | xargs kill $1
      then
        echo "${srv_name} starting"
        /root/.virtualenvs/mall_srv/bin/python3 $srv_name.py --ip=192.168.194.100
        echo "${srv_name} started successfully."
    fi
else
    echo "${srv_name} starting"
    /root/.virtualenvs/mall_srv/bin/python3 $srv_name.py --ip=192.168.194.100
    echo "${srv_name} started successfully."
fi