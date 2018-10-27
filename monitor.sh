sudo ifconfig wlan1 down
sudo service network-manager stop || echo "no network manager"
sudo iwconfig wlan1 mode monitor
sudo ifconfig wlan1 up
