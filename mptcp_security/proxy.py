#!/usr/bin/python

import socket
import select
import time
import sys
import subprocess

class Forward:
    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        print "Actual Destination is:", host , "Port:", port ,"(according to class Forward)" 
        try:
            self.forward.connect((host, port))
            return self.forward
        except Exception, e:
            print e
            return False

class TheFunctionalityModule:
    input_list = []
    channel = {}

    def __init__(self, host, port):

        socket.MPTCP_ENABLED = 26
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        
        self.server.setsockopt(socket.IPPROTO_TCP, socket.MPTCP_ENABLED, 1)
        self.server.bind((host, port))
        self.server.listen(150)
        print "Listening to connections on IP:", host, "port:", port


    def main(self):
                      
        self.input_list.append(self.server)
        while 1:
            #time.sleep(1)
            ss = select.select
            inputready, outputready, exceptready = ss(self.input_list, [], [])
            for self.s in inputready:
               
                if self.s == self.server:
                    self.on_accept()
                    
                    break

                self.data = self.s.recv(4096)
                if len(self.data) == 0:
                    self.on_close()
                    break
                else:
                    self.on_recv()

    def on_accept(self):
        clientsock, clientaddr = self.server.accept()
        add_SNAT_rule(clientaddr[0]) 
        print "_______________________________________________"
        print clientaddr, "has connected"
             

        forward = Forward().start(forward_to[0], forward_to[1])
        print "Started a conn. to ACTUAL dest. ", forward_to[0] , ":", forward_to[1]        
        if forward:
            self.input_list.append(clientsock)
            self.input_list.append(forward)
            self.channel[clientsock] = forward  #Associate the server with the client
            self.channel[forward] = clientsock

            
        else:
            print "Can't establish connection with remote server.",
            print "Closing connection with client side", clientaddr
            clientsock.close()

    def on_close(self):
        print self.s.getpeername(), "has disconnected"
        
        self.input_list.remove(self.s)
        self.input_list.remove(self.channel[self.s])
        out = self.channel[self.s]
        self.channel[out].close() 
        print "closed the connection with remote server"
        print "_____________________________________________"
        print "\n"
        self.channel[self.s].close()
        del self.channel[out]
        del self.channel[self.s]

    def on_recv(self):  #Relay the data received from one party to the other party
        data = self.data
        self.channel[self.s].send(data)
        #print "Forwarding..." 

def TheSecurityModule():
 pid = subprocess.Popen(args=['gnome-terminal', '-e', 'python idps.py'])


def flush_iptables():
 p = subprocess.Popen(["iptables", "-t", "nat", "-F"],      stdout=subprocess.PIPE)
 output , err = p.communicate()
 print output



def add_DNAT_rule(proxy_ip, server_ip):
 p2 = subprocess.Popen(["iptables", "-t", "nat", "-A", "PREROUTING", "-p", "tcp", "-d", server_ip, "-j", "DNAT", "--to-destination", proxy_ip], stdout=subprocess.PIPE)
 output2 , err = p2.communicate()
 print output2

def add_SNAT_rule(client_ip):
 p1 = subprocess.Popen(["iptables", "-t", "nat", "-A", "POSTROUTING", "-p", "tcp", "-j", "SNAT", "--to-source", client_ip], stdout=subprocess.PIPE)
 output1 , err = p1.communicate()
 print output1



if __name__ == '__main__':
        
        proxy_ip = sys.argv[1]
        proxy_port = int(sys.argv[2])
        server_ip = sys.argv[3]
        server_port = int(sys.argv[4])
        forward_to = (server_ip, server_port)


        flush_iptables()
        add_DNAT_rule(proxy_ip, server_ip) #SNAT rule is added once client IP is known
        
        server = TheFunctionalityModule(proxy_ip, proxy_port)
        TheSecurityModule()
               


        try:
            server.main()
        except KeyboardInterrupt:
            sys.exit(1)


l
