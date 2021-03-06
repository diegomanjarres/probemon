#!/usr/bin/python
import os
import time
import datetime
import argparse
import netaddr
import sys
import logging
from scapy.all import *
from pprint import pprint
from logging.handlers import RotatingFileHandler
from datetime import datetime
import threading

NAME = 'probemon'
DESCRIPTION = "a command line tool for logging 802.11 probe request frames"

DEBUG = False
start_time = int(time.time())
count=1

def beep():
	global count
	if count > 0:
		print("info: got " + str(count) + "packets in 15 seconds\n")
		os.system("play --no-show-progress --null --channels 1 synth 1 sine 440")
		count=0
	else:
		print("info: no packets in 15 seconds\n")
		os.system("play --no-show-progress --null --channels 1 synth 15 sine 440")
	sys.stdout.flush()
	threading.Timer(15, beep).start()

def build_packet_callback(time_fmt, logger, delimiter, mac_info, ssid, rssi):
	def packet_callback(packet):
		global count
		count += 1
		#if not packet.haslayer(Dot11):
		#	return

		# we are looking for management frames with a probe subtype
		# if neither match we are done here
		#print('packet')
		if packet.type != 0 or packet.subtype != 0x04:
			return

		# list of output fields
		fields = []

		# determine preferred time format
		log_time = str(int(time.time()) - start_time)

		fields.append(log_time)

		# append the mac address itself
		fields.append(packet.addr2)

		# parse mac address and look up the organization from the vendor octets
		if mac_info:
			try:
				parsed_mac = netaddr.EUI(packet.addr2)
				fields.append(parsed_mac.oui.registration().org)
			except netaddr.core.NotRegisteredError:
				fields.append('UNKNOWN')

		# include the SSID in the probe frame
		if ssid:
			fields.append(str(packet.info))

		if rssi:
			rssi_val = -(256-ord(packet.notdecoded[-4:-3]))
			fields.append(str(rssi_val))

		logger.info(delimiter.join(fields))

	return packet_callback

def main():
	parser = argparse.ArgumentParser(description=DESCRIPTION)
	parser.add_argument('-i', '--interface', help="capture interface")
	parser.add_argument('-t', '--time', default='iso', help="output time format (unix, iso)")
	parser.add_argument('-o', '--output', default='probemon.log', help="logging output location")
	parser.add_argument('-b', '--max-bytes', default=5000000, help="maximum log size in bytes before rotating")
	parser.add_argument('-c', '--max-backups', default=99999, help="maximum number of log files to keep")
	parser.add_argument('-d', '--delimiter', default='\t', help="output field delimiter")
	parser.add_argument('-f', '--mac-info', action='store_true', help="include MAC address manufacturer")
	parser.add_argument('-s', '--ssid', action='store_true', help="include probe SSID in output")
	parser.add_argument('-r', '--rssi', action='store_true', help="include rssi in output")
	parser.add_argument('-D', '--debug', action='store_true', help="enable debug output")
	parser.add_argument('-l', '--log', action='store_true', help="enable scrolling live view of the logfile")
	args = parser.parse_args()

	if not args.interface:
		print ("error: capture interface not given, try --help")
		sys.exit(-1)

	DEBUG = args.debug

	# setup our rotating logger
	logger = logging.getLogger(NAME)
	logger.setLevel(logging.INFO)
	handler = RotatingFileHandler(args.output, maxBytes=args.max_bytes, backupCount=args.max_backups)
	logger.addHandler(handler)
	if args.log:
		logger.addHandler(logging.StreamHandler(sys.stdout))
	built_packet_cb = build_packet_callback(args.time, logger,
		args.delimiter, args.mac_info, args.ssid, args.rssi)
	print('sniffing', args.interface)
	beep()
	sniff(iface=args.interface, prn=built_packet_cb, store=0)

if __name__ == '__main__':
	main()
