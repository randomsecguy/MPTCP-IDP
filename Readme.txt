Description:

The proof-of-concept tool utlizes MPTCP adapted connection tracking to perform accurate intrusion detection and prevention. All MPTCP packets are logged into a dictionary and correlations are being analyzed for every new packet. MPTCP subflows are linked to their respective connections. For every data packet, the subflow data is extracted and ordered to recreate the original data stream which is fed into a signature matcher. 

First, the IDPS needs to be runnning in order to grab MPTCP packets and perform processing accordingly. The list of signatures 
is currently embedded inside the code. 

Note: The sha1.py file is forked from the code released at https://github.com/Neohapsis/mptcp-abuse

Assumption:

The tool is able to see traffic from all subflows

Dependencies:

Pcapy https://github.com/CoreSecurity/pcapy
DPKT https://github.com/kbandla/dpkt
SCAPY http://www.secdev.org/projects/scapy/
TEXTTABLE https://pypi.python.org/pypi/texttable
PYDOT https://code.google.com/p/pydot/

Planned updates:
-Ability to use a text file as the signature database
-Update the prevention methodology from TCP RST to MPTCP specific signaling
-Other general improvements and refinements
