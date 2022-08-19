#/bin/bash
cp -r app/* /opt/app/
apt-get install -y python3 python3-pip python3-virtualenv nginx gunicorn3 supervisor git;
pip3 install -r /opt/app/requirements.txt
# cron
sudo cp cron /etc/cron.d/cron
sudo cp chmod 0644 /etc/cron.d/cron
sudo crontab /etc/cron.d/crontab
sudo cron
# nginx
sudo rm /etc/nginx/sites-enabled/default
sudo cp nginx_sock.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/nginx_sock.conf /etc/nginx/sites-enabled/nginx_sock.conf
sudo echo "daemon off;" >> /etc/nginx/nginx.conf
# supervisor
mkdir -p /var/log/supervisor
sudo cp supervisord.conf /etc/supervisor/conf.d/supervisord.conf
sudo cp gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf
# run
cd /opt/app/ && python3 create_serve_models.py
sudo /usr/bin/supervisord