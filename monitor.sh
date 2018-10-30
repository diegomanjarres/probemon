sudo ifconfig wlan0 down
sudo service network-manager stop || echo "no network manager"
sudo iwconfig wlan0 mode monitor
sudo ifconfig wlan0 up
