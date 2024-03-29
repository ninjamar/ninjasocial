apt update
apt upgrade -y
apt install -y lsb-release
curl -fsSL https://packages.redis.io/gpg | gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/redis.list
apt update
apt install -y redis

redis-server --daemonize yes &

touch /etc/cron.daily/api-token
echo "python3 /app/api_action.py" > /etc/cron.daily/api-token
chmod u+x /etc/cron.daily/api-token

python3 api_action.py

pip3 install uvicorn[standard]
uvicorn --host 0.0.0.0 --port 8080 --workers 2 social.asgi:application