Description:

The proof-of-concept tool sniffs the selected interface for MPTCP packets and keeps track of all MPTCP sessions using different MPTCP options and TCP flags. It can correlate/link subflows to their respective MPTCP session. Once it sees, DATA_FIN on a connection, it assembles data from different subflows of that connection, reorders everything according to DSN and creates a single TCP data packet for that MPTCP session.

Note: The sha1.py file is forked from the code released at https://github.com/Neohapsis/mptcp-abuse

Assumption:

The tool is able to see traffic from all subflows

Dependencies (A lot currently):

Pcapy https://github.com/CoreSecurity/pcapy
DPKT https://github.com/kbandla/dpkt
SCAPY http://www.secdev.org/projects/scapy/
TEXTTABLE https://pypi.python.org/pypi/texttable
PYDOT https://code.google.com/p/pydot/


Upcoming features:

Ability to take PCAP trace as input
Create graphs
      