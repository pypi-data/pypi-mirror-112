#!/bin/sh
echo "AIS release script starting for 2021.5.3 on chanel 3" 
pip install python-miio==0.5.5 -U  

echo "21.04.08" > /data/data/pl.sviete.dom/files/home/AIS/.ais_apt  
apt update 

apt upgrade  -y 

curl -k -o "/data/data/pl.sviete.dom/files/home/.bash_profile" -L  https://raw.githubusercontent.com/sviete/AIS-utils/master/patches/scripts/.bash_profile 

curl -k -o "/sdcard/AisClient.apk" -L https://powiedz.co/ota/android/AisPanelApp-gate-release.apk && su -c "pm install -r /sdcard/AisClient.apk" 

echo "21.02.03" > /data/data/pl.sviete.dom/files/home/AIS/.ais_apt  
apt update 

apt upgrade  -y 

apt reinstall python 

curl -o "/sdcard/AisLauncher.apk" -L https://powiedz.co/ota/android/AisLauncher.apk 

su -c "pm install -r /sdcard/AisLauncher.apk" 

echo "# AIS Config file for mosquitto" > "/data/data/pl.sviete.dom/files/usr/etc/mosquitto/mosquitto.conf"  

echo "listener 1883 0.0.0.0" >> "/data/data/pl.sviete.dom/files/usr/etc/mosquitto/mosquitto.conf"  

echo "allow_anonymous true" >> "/data/data/pl.sviete.dom/files/usr/etc/mosquitto/mosquitto.conf"  

echo "21.03.24" > /data/data/pl.sviete.dom/files/home/AIS/.ais_apt  
echo "21.02.19" > /data/data/pl.sviete.dom/files/home/AIS/.ais_apt  
echo "AIS Linux update START" 

echo "AIS save config file for mosquitto" 

cp /data/data/pl.sviete.dom/files/usr/etc/mosquitto/mosquitto.conf /sdcard/mosquitto.conf 

echo "AIS apt update" 

apt update 

DEBIAN_FRONTEND=noninteractive apt -y upgrade 

echo "AIS back config file for mosquitto" 

cp /sdcard/mosquitto.conf /data/data/pl.sviete.dom/files/usr/etc/mosquitto/mosquitto.conf 

echo "AIS reinstall python" 

apt reinstall python 

pip install python-miio==0.5.5 -U  

echo "AIS Linux update END" 

echo "21.05.25" > /data/data/pl.sviete.dom/files/home/AIS/.ais_apt  
echo "21.06.02" > /data/data/pl.sviete.dom/files/home/AIS/.ais_apt  

