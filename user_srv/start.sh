srv_name="user_srv_server"

chmod +x ./$srv_name.py
#重启，如果已经存在则关闭重启
PIDS=`ps -ef | grep ${srv_name} | grep -v grep | awk '{print $2}'`
if [ "$PIDS" != "" ];
then
    echo "${srv_name} is already running."
    echo "shutting down ${srv_name}"
    ps -aux | grep $srv_name | awk '{print $2}' | xargs kill $1
    echo "${srv_name} starting"
    /root/.virtualenvs/mall_srv/bin/python3 $srv_name.py --ip=121.43.157.170 > /dev/null 2>&1 &
    echo "${srv_name} started successfully."
else
    echo "${srv_name} starting"
    /root/.virtualenvs/mall_srv/bin/python3 $srv_name.py --ip=121.43.157.170 > /dev/null 2>&1 &
    echo "${srv_name} started successfully."
fi