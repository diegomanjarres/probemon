sudo ifconfig wlan1 down
sudo iwconfig wlan1 mode managed
sudo ifconfig wlan1 up
sudo service network-manager restart
