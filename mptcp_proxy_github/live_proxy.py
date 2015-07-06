#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pcapy
import dpkt
import socket
from mptcp_analyzer import *
from impacket.ImpactDecoder import *


 
# list all the network devices
print pcapy.findalldevs()
interface = raw_input("Please enter interface: ")
#interface = 'eth0'



def rcv_pkts(header, pkt):
 packet= 1
 
 try:
  packet_parser(packet, pkt)
  
  finish()


  

 except:
  pass



 
max_bytes = 1024
promiscuous = False
read_timeout = 100 # in milliseconds

cap = pcapy.open_live(interface, max_bytes, promiscuous, read_timeout)
 
cap.setfilter('tcp')

try:
 while True:
 #total_packets = cap.loop(-1, rcv_pkts)
  total_packets = cap.dispatch(-1, rcv_pkts)       #Dispatch is more responsive to Keyboard interrupts
 
except KeyboardInterrupt:
  
 print "All over"


