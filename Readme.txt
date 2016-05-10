Description:

The proof-of-concept methodology utlizes MPTCP adapted connection tracking information to perform accurate intrusion detection
and prevention. All MPTCP packets are logged into a dictionary and correlations are analyzed for every new packet. MPTCP subflows
are linked to their respective connections. For every data packet, the subflow data is extracted and reordered to recreate 
the original data stream which is fed into a signature matcher. 

The repo consists of a basic proxy where the security part is integrated. 


Working:

 +------+           +-----+            +----------+        
 |Client| <=MPTCP=> |Proxy| <=MPTCP=>  |TCP Server|
 +------+           +-----+            +----------+       

The above figure explains the assumed setup. All the traffic from the MPTCP client and the TCP server needs to traverse through proxy. When the proxy starts, it sets up NAT rules to be able to transparently answer to the client on the behalf of TCP server. 

Usage:

Run proxy by providing it with four arguments as follows:
  sudo python proxy.py proxy_ip proxy_port server_ip server_port 
e.g sudo python proxy.py 172.16.208.130 80 172.16.208.131 80





Note: The sha1.py file is forked from the code released at https://github.com/Neohapsis/mptcp-abuse

Dependencies:
Python-iptables https://github.com/ldx/python-iptables
Pcapy https://github.com/CoreSecurity/pcapy
DPKT https://github.com/kbandla/dpkt
SCAPY http://www.secdev.org/projects/scapy/
TEXTTABLE https://pypi.python.org/pypi/texttable
PYDOT https://code.google.com/p/pydot/

Planned updates:
-Add ability to use a text file as the signature database
-Integrate into a proxy to extend benefits to all hosts
-Update the prevention methodology from TCP RST to MPTCP specific signaling
-Other general improvements and refinements
