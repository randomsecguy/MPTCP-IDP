Description:

The proof-of-concept tool performs MPTCP adapted connection tracking and intrusion detection. The tool can be integrated into any proxy
to extend the benefits to all hosts. It requires, access to MPTCP packets. 

Note: The sha1.py file is forked from the code released at https://github.com/Neohapsis/mptcp-abuse

Assumption:

The tool is able to see traffic from all subflows

Dependencies:

Pcapy https://github.com/CoreSecurity/pcapy
DPKT https://github.com/kbandla/dpkt
SCAPY http://www.secdev.org/projects/scapy/
TEXTTABLE https://pypi.python.org/pypi/texttable
PYDOT https://code.google.com/p/pydot/

