ssh 0.0.0.0 
cd griffy-dev2
nano launcher.sh

#!/bin/sh
cd /
cd home/pi/bbt
sudo python bbt.py
cd /

: '
after that, type:
chmod 755 launcher.sh
sh launcher.sh
cd
mkdir logs
sudo crontab -e
@reboot sh /home/.../launcher.sh >/home/pi/logs/cronlog 2>&1
sudo reboot
cd logs
cat cronlog

'
