Description:

The proof-of-concept tool performs MPTCP adapted connection tracking and intrusion detection. First the IDPS module needs to be run to grab MPTCP packets and perform processing accordingly. The list of signatures is currently embedded inside the code. 

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
