sudo ifconfig ${ANTENNA} down
sudo service network-manager stop
sudo iwconfig ${ANTENNA} mode monitor
sudo ifconfig ${ANTENNA} up
