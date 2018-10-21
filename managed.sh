sudo ifconfig ${ANTENNA} down
sudo iwconfig ${ANTENNA} mode managed
sudo ifconfig ${ANTENNA} up
sudo service network-manager restart
