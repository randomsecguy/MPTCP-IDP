#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pcapy
import dpkt
import socket
from analyzer import *
from impacket.ImpactDecoder import *
import subprocess
import time
from sys import exit
import iptc


 
# list all the network devices
#print pcapy.findalldevs()
#interface = raw_input("Please enter interface: ")
interface = 'eth0'
signatures = ['ATdIS', 'mJhFMJoBwM', 'UprUtkegWIDPswW', 'skuDtDCGhEXmoEkeAzLd', 'NztqitwGgiAnoEApjHBjSzYcI','gtZRqbUCmBsTqaAtGRDNXvJvCIqQWZ', 'zJSHIgpWldAbjbspfKdAPZHYDXKFsRuvwWL', 'eQbRbjYtQlJYmuZtSjXySdvxxaAZzDuMAxQrfVWS', 'ZpNhPisNBnaArNGrlvKdcsmjjUWDgxDexJZTjjYtQJrhr', 'QtcPEIDHoDRPndsQMqzXEEedaOjbufjdpVLwDcSCszNegEZRpm']
data_times = []
detection_times = []
detected_sigs=[]

packet= 0



def change_rules():
 rule = iptc.Rule()
 rule.target = iptc.Target(rule, "ACCEPT")
 chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "FORWARD")
 chain.insert_rule(rule)


def signature_matcher(payload):
 #sig_timer =time.time()
 
 for signature in signatures:
   if signature in payload:
    
    for key, value in d.iteritems():
     for element in value:
      print "Found", element[2], "in", element, "of ", value
      if not '.' ==  element[2]:
       if int(element[2]) > 2:
        data_times.append(element[2])
    #print "Dictionary", d
    print "Data times are:", data_times
    #print "Last Data Packet arrived at:", '%.6f' % max(times)
    maxx = max(data_times)
   
    change_rules()
    print "Maxx is", '%.6f' % maxx
    tii = time.time()
    print "Current time: ", '%.6f' % tii 
    
    diff = (tii - maxx) * 1000000
    print "SIGNATURE (", signature, ") DETECTED in", '%.6f' % diff, "(micro s)"
    detected_sigs.append(signature)
    #del d
    #exit(0)
    #time.sleep(5) 
    detection_times.append(diff)
    del d[key] 
   #else:
   # print "SIGNATURE not present"

 


def rcv_pkts(header, pkt):
 global packet
 packet= packet + 1
 

 #try:
 start  = time.time()
 payload = packet_parser(packet, pkt, start)
 try:
  if sys.argv[1] is "v":
   finish()
  else:
   pass
 except:
  pass 
 #payload = data_mapper()
 end = time.time()
   
 
 
 #print "Time from packet arrival to data mapping: (micro s)", 1000000 * (end - start)
 if payload: 
  signature_matcher(payload)
  
 else: 
  print "Not Data Packet"

# except:
 # pass


def passive_capture():
 
 
 max_bytes = 1024
 promiscuous = False
 read_timeout = 100 # in milliseconds
 
 cap = pcapy.open_live(interface, max_bytes, promiscuous, read_timeout)
 
 cap.setfilter('tcp')

 try:
  while True:
  #total_packets = cap.loop(-1, rcv_pkts)
  
   total_packets = cap.dispatch(-1, rcv_pkts) #Dispatch is more responsive to Keyboard interrupts
  
 except KeyboardInterrupt:
  print "*******************************SUMMARY**********************"
 

  #for zz in detected_sigs:
   #print "Detected signature:", zz 


  print "Detected ", len(detection_times), "signatures"  
  print "Detection times", detection_times
  summ= 0
  for i in detection_times:
   summ = summ + i
  print "Average Detection time:", summ / int(len(detection_times))
  time.sleep(5)
  #cap.breakloop()
  #createchart()
 # print "All over"

################################################MAIN###################################################

passive_capture()
