# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 17:12:18 2018

@author: Reshma
"""


from inspect import getsourcefile
import os.path
import sys
from threading import Thread
from time import sleep
import config
import os
from socket import *
host = ""#"10.60.1.175"
port = 13000
buf = 200
addr = (host, port)

UDPSock = socket(AF_INET, SOCK_DGRAM)
#UDPSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
UDPSock.bind(addr)
#UDPSock.listen()

#   c, addr = UDPSock.accept()
config.gen_key_pair()
vk = UDPSock.recv(100)
#print("Waiting to receive messages...")
while True:
  
    (data, addr) = UDPSock.recvfrom(buf)
    #print("Received message: " + data)
    msg = config.sign_txn(config.get_sk(),data)
    UDPSock.sendto(msg , addr)
   
UDPSock.close()
os._exit(0)
'''
# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread): 
 
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        print("[+] New server socket thread started for " + ip + ":" + str(port) )
 
    def run(self): 
        while True : 
            data = conn.recv(64) 
            print("Server received data:", data)
            msg = config.sign_txn(config.get_sk(),data)
            conn.send(msg)  # echo 

# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0' 
TCP_PORT = 2004 
BUFFER_SIZE = 100  # Usually 1024, but we need quick response 

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT)) 
threads = [] 
 
while True: 
    tcpServer.listen(4) 
    (conn, (ip,port)) = tcpServer.accept() 
    newthread = ClientThread(ip,port) 
    newthread.start() 
    threads.append(newthread) 
 '''