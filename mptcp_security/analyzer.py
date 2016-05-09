import dpkt
import binascii
import os
import socket
import collections
import texttable
import hashlib
import string
import pydot 
import sys
import time
from scapy.all import *
from sha1 import * 
import plotly.plotly as py
from plotly.graph_objs import *
from random import randint
from netfilterqueue import NetfilterQueue


packet=0
payloads = 0
packetsin = 0
subflows = 0
datacount = 0



os.system('clear') 
d = dict()



def write2file(data):

 #data = binascii.hexlify(str(data))
 #print "Payload written: ",data
 #temp = '|'+ data + '|'
 f2=open('payload.txt','a')
 f2.write(data)
 f2.write("\n")
 

def dictionary(sip, sport, dip, dport, recv_token):

 #print "recv_token:", recv_token, "is received by dict"
 key = recv_token
 value =  str(sip) + ":" + str(sport) +  ">" + str(dip)+  ":" + str(dport)

 #print d
 if key in d:
  if value not in d[key]: #To ensure that retransmission packets dont count as new values
   #print key, "is in dict and value is not present", "adding value:", value
   d[key].append(value)
  else:
   print key, "is in dict and value is also present"

 else:
  #print key , "is not in dict","adding value:", value
  d[key] = [value]

 #print "Updated Dict d is ", d
 #print connection_display()



def connection_display():

 index = 0
 #print "\n"
 #print "Dictionary d has:"
 #print d
 print "Total number of MPTCP sessions:", len(d)
 print "Total number of subflows: ", sum(len(v) for v in d.itervalues())
 
 for key, value in sorted(d.iteritems()):
  #for x, y in collections.Counter(value).items():
   #print x, y
  print "MPTCP session with token:", key,  "has subflows:", len([item for item in value if item])
 print "Total Data packets:", datacount


 
 t = texttable.Texttable()
 t.header(["MPTCP Session", "Unique Token (key)", "Subflows", "Details (Value)"])
 t.set_cols_dtype(['t',  # text 
                   'i',  # integer
                   'a', 'a']) # automatic

 for key, value in d.iteritems():
  index+=1
  

  if payloads>1:
   t.add_row([index, key , len([item for item in value if item]), [x[0] for x in value] ])
  else:
   t.add_row([index, key , len([item for item in value if item]), value ])
  
   

 print t.draw()



def subflow_display():
  
 t2 = texttable.Texttable()
 #t2.header(["Subflow", "Belongs to MPTCP Connection", "Data Packets (both directions)", "Data", "DSN", "Validity"])
 t2.header(["Subflow", "Belongs to MPTCP Connection", "Data", "Data Packets on subflow (<> directions)", "DSN", "Validity"
  ])
 
 t2.set_cols_dtype(['t',  # text 
                   't',  # integer
                   't', 
                    't', 
                     't', 't'
                    ]) # automatic

 for key, value in d.iteritems():
  
  print "D has   key:", key
  print "D has value:", value
  
  try:

    for element in value:
     
     datapackets = str(element).count(">|<")
     print element, "has: ",  datapackets , "data packets"  
     
     #print element, "has length:", len(element)
   
    
     if datapackets == 0:
      #print "No data packet on this subflow:", element
      t2.add_row([element, key, "-", datapackets, "-", "-"]) 
      

     if datapackets == 1:     #If a subflow only sees one or less data packet
       
      ind1 = element[1].index(' >|<')
      ind2 = element[1].index(' *|*')
      t2.add_row([element[0], key, element[1][0:ind1], len(element) - 1, element[1][ind1+4:ind2], element[1][ind2+4:]]) 
      #total packets = whatever is in value minus the original entry of subflow
  

     if datapackets > 1:      #If multiple data packets are sent over a subflow (both directions) [Needs to be generalized]
      
      #print "element[0] is ", element[0]     #('172.16.208.129:55124>172.16.208.128:82', 'Client_Hello >|<3560898898 *|*12')      
      #print "element[1] is ", element[1]     #Server_Hello >|<3235881725 *|*12 

      newelement=', '.join(element[0])      #Convert tuple to string to be able to find indexes

      ind0 = newelement.index(',')
      ind1 = newelement.index(' >|<')
      ind2 = newelement.index(' *|*')

      ind3 = element[1].index(' >|<')
      ind4 = element[1].index(' *|*')

      

      t2.add_row([newelement[0:ind0], key, newelement[ind0+2:ind1], datapackets, newelement[ind1+4:ind2], newelement[ind2+4:]]) 
      t2.add_row([newelement[0:ind0], key, element[1][0:ind3], datapackets, element[1][ind3+4:ind4], element[1][ind4+4:]])  

        



    
      #if ind1 and ind2:

      #else:
      #t2.add_row([element[0], key, "NO", "NO", "NO", "NO"])
       
       
    

# else:
#      t2.add_row([element[0], key, "NO", len(element) - 1, element[1][ind1+4:ind2], element[1][ind2+4:]        #total packets = whatever is in value minus the original entry of subflow
#      ])

   
  except:
   pass
 print t2.draw()



def createchart():

 x = []
 y = []

 for key, value in d.iteritems():

  x.append(int(key))
  t = len([item for item in value if item])
  y.append(int(t))

 print "X-axis", x
 print "Y-axis", y
 
 data = Data([
        Bar(
           x= x, y =y)
])


 layout = Layout(
    xaxis=XAxis(
        title = 'MPTCP Connections',
        exponentformat='e',
        showexponent='first'
        
    ),
    yaxis=YAxis(title = 'Number of Subflows')
)

 fig = Figure(data=data, layout=layout)
 plot_url = py.plot(fig, filename='basic-bar')



def data_mapper():


 mapping = []
 mapped_payload = []
 
	
 try:
  for key in d.keys():
   
   print "MPTCP Connection:", key  
      
   for temp in d[key]:
    
    if ' >|<' in temp[1]:          #If the subflow actually had a data packet

     ind1 = temp[1].index(' >|<')
     ind2 = temp[1].index(' *|*')
     mapping.append(temp[1][ind1+4:ind2])          #Find DSN and append to mapping



##########Now we reconstruct the data stream according to the sorted order########

     for x in sorted(mapping):
      if x == temp[1][ind1+4:ind2]:
       #print "x" , x, "is equal to", temp[1][ind1+4:ind2]
       #print "Data is ", temp[1][0:ind1]
       mapped_payload.append(temp[1][0:ind1])
      
     ttime= temp[2]	

     #print "Original Sequence of DSN's :",  mapping 
     #print "Sorted Sequence of DSN's   :" , sorted(mapping)
     #print "Reconstructed data stream  :", ''.join(mapped_payload), "\n"

    else:
     #mapped_payload.append(' ')    	
     break

   print "Current Datastream is", ''.join(mapped_payload)
   return ''.join(mapped_payload) 
   #packet_generator(sip, dip, int(sport), int(dport), ''.join(mapped_payload))
   
  
   #mapped_payload = []
   #mapping = []

   #del d[key]         #Delete the connection entry once a packet is created (to avoid duplicates)

 except: 
  pass




def packet_generator(src, dst, sport, dport, pay):

 #print "Dictionary d has:" , d

 #for keys in d.keys():
  #values 

 dst = "216.58.209.110"     #Assume server is of google. so we create a 3 way handshake with it and send the reordered data
 
 print "Packet gen calledXXXXXXXXXXXXXXXXXXXXXXXXXx" 

 ip  = IP(src=src, dst=dst)
 TCP_SYN=TCP(sport=sport, dport=dport, flags="S", seq=100)
 TCP_SYNACK=sr1(ip/TCP_SYN)

 my_ack = TCP_SYNACK.seq + 1
 TCP_ACK=TCP(sport=sport, dport=dport, flags="A", seq=101, ack=my_ack)
 send(ip/TCP_ACK)

 my_payload= pay
 TCP_PUSH=TCP(sport=sport, dport=dport, flags="PA", seq=102, ack=my_ack)
 send(ip/TCP_PUSH/my_payload)
 



def visualize():

 subflow_num = 1
 graph = pydot.Dot(graph_type='graph')
 conns = len(d)
 subfs=  sum(len(v) for v in d.itervalues())

 for key, value in sorted(d.iteritems()):
 
  edge = pydot.Edge("Root", "MPTCP Connection: %s" % key)
  graph.add_edge(edge)
  subs = len([item for item in value if item])
  for i in range (0, subs):
   edge = pydot.Edge("MPTCP Connection: %s" % key, "Subflow%d" % subflow_num)
   graph.add_edge(edge)
   subflow_num += 1


 graph.write_png('mptcp.png')





def get_sender_key(options):                  #Extract key from SYN packet and the response SYN/ACK packet 
 options_list = dpkt.tcp.parse_opts(options) 
 try:
  for option in options_list: 
   if option[0] == 30:
    data = binascii.hexlify(str(option[1]))
              
    return data[4:]    #Sender's key is always after mp_capable option (0-2) + mptcp flags(2-4) 

 except:
  pass



def get_recv_token(options):             #extract recv's token from the mp_join message
 options_list = dpkt.tcp.parse_opts(options) 
 try:
  for option in options_list: 
   if option[0] == 30:
    data = binascii.hexlify(str(option[1]))
    return data[4:12]            #Recv's token is always after mp_join option (0-2) + mptcp flags(2-4) and before sender's random number (13 onwards)
     
 except:
  pass




def get_dsn_n_length(options):

 options_list = dpkt.tcp.parse_opts(options)
 #print "Options list: ", options_list
 try:
  for option in options_list:
   if option[0]==30:  #Go to MPTCP Option (agar option ka first part 30 ha to send second part to hexlify function coz options are returned by parse as option no:option value
    data = binascii.hexlify(str(option[1]))
    return data[12:20], data[28:32]            
     
 except:
  pass


def check_mptcp(options):   
 options_list = dpkt.tcp.parse_opts(options) 
 for option in options_list: 
  if option[0] == 30:
   return "MPTCP"  


def check_mpjoin(options):
 options_list = dpkt.tcp.parse_opts(options) 
 try:
  for option in options_list: 
   if option[0] == 30:

    data = binascii.hexlify(str(option[1]))
    data = data[0:2]                      #MP_JOIN option is always at the start of options
    #write2file(data)  
   
    if data == "10":  
     #print "SUBFLOW ADDITION REQUEST"
     return "True"      

 except:
  pass 
  #return options_list


def check_datafin(options):
 options_list = dpkt.tcp.parse_opts(options) 
 try:
  for option in options_list: 
   if option[0] == 30:
    data = binascii.hexlify(str(option[1]))
    data = data[2:4]                      
    #write2file(data)  
   
    if data == "15":        #TCP flags==0x15 means its a DATA_FIN
     #print "DATA_FIN"
     return "True"      

 except:
  pass 
  #return options_list






def packet_parser(packet, pkt, start):
                        

   	    print "-----------------------------------------------------------------"
	    eth=dpkt.ethernet.Ethernet(pkt)
	    ip=eth.data      

	    try:
	     if ip.p == dpkt.ip.IP_PROTO_TCP:       
	      tcp = ip.data          #IP has TCP segmet (header plus tcp payload) encapsulated in its payload. Extract it and save to tcp
	    

	      syn_flag = (tcp.flags & dpkt.tcp.TH_SYN)  != 0
	      psh_flag = (tcp.flags & dpkt.tcp.TH_PUSH) != 0
	      ack_flag = (tcp.flags & dpkt.tcp.TH_ACK ) != 0

	      dip = socket.inet_ntoa(ip.dst)
	      sip = socket.inet_ntoa(ip.src)
	      dport = tcp.dport
	      sport = tcp.sport

	    
	      if check_mptcp(tcp.opts) == "MPTCP":
               #print "MPTCP so accepted"
               
               
 
	       if syn_flag and not ack_flag and not check_mpjoin(tcp.opts):              # First MP_CAPABLE SYN request


		sender_key = get_sender_key(tcp.opts)
		sender_key = int(sender_key, 16)
		print "Packet:", packet, "is a SYN req for a new MPTCP connection from ", sip, ":", sport, "to", dip,":",dport, "with client's key:", sender_key
                



	       elif syn_flag and ack_flag and not check_mpjoin(tcp.opts):                # SERVER's RESPONSE TO THE FIRST MP_CAPABLE SYN 

		sender_key = get_sender_key(tcp.opts)
		sender_key = int(sender_key, 16)
		   
		key_sha, garbage = token(sender_key)
		print "Packet:", packet, "is a SYN/ACK response for MPTCP connection with server's key:", sender_key, "or", key_sha , "(SHA1)"
	       
		dictionary(dip, dport, sip, sport, key_sha)    #need to invert because we are extracting details from the response packet of server
                

	       
	       elif syn_flag and not ack_flag and check_mpjoin(tcp.opts):                # MP_JOIN Req from client to server (req to add new subflow to existing MPTCP connection)

		recv_token = get_recv_token(tcp.opts)
		recv_token = int(recv_token, 16)
		print "Packet:", packet, "is a SYN req for a new subflow to an old MPTCP connection with token: ", recv_token
		dictionary(sip, sport, dip,  dport, recv_token)
                

	      

	       #elif syn_flag and ack_flag and check_mpjoin(tcp.opts):                # SERVER's RESPONSE TO MP_JOIN request

		#sender_key = get_sender_key(tcp.opts)
		#sender_key = int(sender_key, 16)
		#print "Packet:", packet, "is a SYN/ACK response to MP_JOIN request"
                

	  
	       if psh_flag and ack_flag:  #Data packet
                

                datatimer= time.time()
                global datacount
		datacount+=1 
		dsn, length = get_dsn_n_length(tcp.opts)
		dsn = int(dsn, 16)              #Convert hex to int with base 16	       

		length = int(length, 16)        #length of bytes for which the mapping is valid    
		      
				       
		print "Packet:", packet, "has PSH+ACK", "from", str(sport), "to", str(dport), "DSN:", dsn, ", Valid for" , length, "hex digits (or /2 bytes)"
	       
		data = tcp.data       #extract tcp payload from the overall segment         
                print "Packet has data:", data, "arriving at ", '%.6f' % datatimer
	       
		 
		#data = str(data) + ' >|<' + str(dsn) + ' *|*' + str(length)
	  
		test =   str(sip) + ":" + str(sport) +  ">" + str(dip) +  ":" + str(dport)
		test2 =  str(dip)+  ":" + str(dport) +  ">" + str(sip) +  ":" + str(sport)        #To accommodate data packets from opposite direction
	
		for key, value in d.iteritems(): 
			      
		 if any(test in s or test2 in s for s in value):  #Payload is from a flow that we know and are tracking. Tests ensure that we account for data packets in both directions client--><--server
		  for place, item in enumerate(value): #Go through all values, find the value which matches the data packet and update that value by adding data and other info 
		   if test in item or test2 in item:
		    item = item ,  str(data) + ' >|<' + str(dsn) + ' *|*' + str(length), datatimer      
		    value[place] = item
                   
                 else:
                  print "Not adding dataXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX1 coz ", test ,"or", test2, "is not in", value
	 
                #print "Dict d is ", d
                               
                retur = data_mapper()
                return retur
	   
		 # write2file(data)
		  #payloads+=1 

               if ack_flag and check_datafin(tcp.opts):   #Data Fin packet
                   
                test = str(sip) + ":" + str(sport) +  ">" + str(dip) +  ":" + str(dport) 
                print "Packet with", test, "has a Data_FIN"  
                
                

                #for key, value in d.iteritems():
                 #for x in value:
                  #if test == x[0]:                    
                   #data_mapper(str(sip), str(sport), str(dip), str(dport))              #Currently we assume that DATA_FIN on any subflow of an MPTCP session means the whole connection is terminating
                  

                
	    except:
	     pass

            



        
 



def finish():
  
 connection_display()
 #subflow_display()
 #data_mapper()
 #visualize()











