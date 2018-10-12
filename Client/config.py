# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 18:02:27 2018

@author: Reshma
"""


#SLEEP TIME
from time import sleep
SLEEP_TIME = 1
from socket import *


from ecdsa import SigningKey, VerifyingKey, NIST384p

IP_MODE = 2 # 0 : SQLite , 1 : Excel , 2 : RND_GEN
IP_FILE = "source1.db"
DOWN_DEF = 0 # 0 : Accept by default , 2 : Reject , 3 : Pending
OP_MODE = 0 # 0 : GUI, 1 : Excel 
T1 = 5 # First timeout in minutes
T2 = 10 # Second timeout in minutes
T3 = 30 # Rejection timeout in minutes
Q1_MAX = 100 # Main Incoming Queue Size
Q2_MAX = 100 # First timeout Queue Size
Q3_MAX = 100 # Second timeout Queue Size
QR_MAX = 100 # Reject Queue Size

target = "127.0.0.1"
#target = "10.60.1.175" # set to IP address of target computer
port = 13000
toaddr = (target,port+1)
addr = (target, port)
BUFFER_SIZE = 200
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.connect(addr)
target_vk = ""
num_worker_threads = 1


def gen_key_pair():
    
    sk = SigningKey.generate(curve=NIST384p)
    vk = sk.get_verifying_key()
    open("private.txt","wb").write(sk.to_string())
    open("public.txt","wb").write(vk.to_string())
    
def get_sk():
    sk_pem = open("private.txt","rb").read()
    sk = SigningKey.from_string(sk_pem, curve=NIST384p)
    return sk
    
def get_vk():
    vk_pem = open("public.txt","rb").read()
    vk = VerifyingKey.from_string(vk_pem, curve=NIST384p)
    return vk.to_string()

def set_vk(vstring):
    target_vk = VerifyingKey.from_string(vstring)
    open("target.txt","wb").write(target_vk.to_string())
    
def verify(s_item,item):
    vk_pem = open("target.txt","rb").read()
    target_vk = VerifyingKey.from_string(vk_pem, curve=NIST384p)
    if(target_vk==""):
        print("Please initialize Target Verification Key")
    else:
        assert target_vk.verify(s_item, item)

if __name__ == '__main__':
    print ('Setup Client Environment Variables')
    
    IP_MODE = input("Enter Input Mode :  0 : SQLite , 1 : Excel , 2 : RND_GEN ")
    IP_FILE = input("Enter Input File Name : ") #"source1.db"
    DOWN_DEF = input("Enter Downtime Behaviour :  0 : Accept by default , 2 : Reject , 3 : Pending")
    OP_MODE = input("Enter Output Mode :  0 : GUI, 1 : Excel ")
    T1 = input("Enter Main Queue timeout :") # First timeout in minutes
    T2 = input("Enter 2nd queue timeout :")  # Second timeout in minutes
    T3 = input(" Enter Rejection timeout :") #in minutes
    Q1_MAX = input(" Main Incoming Queue Size :")
    Q2_MAX = input(" First timeout Queue Size :")
    Q3_MAX = input(" Second timeout Queue Size :")
    QR_MAX = input("  Reject Queue Size :")
    
    target = input("Enter Target IP Address : eg, 127.0.0.1")
    #target = "10.60.1.175" # set to IP address of target computer
    port = input("Enter port number : ")#13000
    BUFFER_SIZE = input("Enter buffer size (Recommended 100) : ")#200
    num_worker_threads = input("Enter number of parallel threads : ")#1

def sign_txn(sk,item):
    return sk.sign(item)


def ver_txn(vk,s_item,txn):
    assert vk.verify(s_item,txn)


    
def send_txn(s_item,addr):
    
    UDPSock.send(s_item)
    reply = UDPSock.recv(BUFFER_SIZE) # Size of signature NIST384p = 64bytes
    if not reply:
        return 0
    else:
        return reply
    