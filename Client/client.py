import config
import queue
import threading
#Key Code
#config.gen_key_pair()
#Setup sockets
import os
from socket import *
import datetime

from inspect import getsourcefile
import os.path
import sys

#load utils
current_path = os.path.abspath(getsourcefile(lambda:0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

sys.path.insert(0, parent_dir)

import utils



#initialize queues
#shared_ledger = queue.PriorityQueue(0)
q1 = queue.PriorityQueue(config.Q1_MAX)
q2 = queue.PriorityQueue(config.Q2_MAX)
q3 = queue.PriorityQueue(config.Q3_MAX)
#rejects = queue.PriorityQueue(config.QR_MAX)

shared_ledger = []
rejects = []
#TODO sources DONE
fname = config.IP_FILE
mode = config.IP_MODE

def ip_switch(arg):
   switcher = {
        0: utils.sql_source(fname),
        1: utils.excel_source(fname),
        2: utils.rnd_source(fname)
    }
   func = switcher.get(arg, lambda: "Invalid Input Source Setting. Check Config file")
   return func
 #  ip_switch(config.IP_SOURCE)


config.gen_key_pair()
sk = config.get_sk()
vk = config.get_vk()

UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.sendto(vk, config.toaddr)

UDPSock.close()  

from tkinter import *
'''
master = Tk()

listbox = Listbox(master)
listbox.pack()
'''
def worker():
    while True:
        item = q1.get()
        s_item = config.sign_txn(sk,str(item).encode())
        if(config.send_txn(s_item,config.addr)):#s_item,config.addr)
            shared_ledger.push()
        else:
            rejects.push()
            
        #print(shared_ledger.qsize() , rejects.qsize())
        #q1.task_done()
'''        
for i in range(config.num_worker_threads):
     t = threading.Thread(target=worker)
     t.daemon = True
     t.start() 
'''
pt_ledger = []
pt_rejects = []
source = ip_switch(mode)
for item in source:

    q1.put(item)
    print(item)
    s_item = config.sign_txn(sk,str(item).encode())
    #print(s_item)
    if(config.send_txn(s_item,config.addr)):#s_item,config.addr)
        #shared_ledger.put(s_item)
        shared_ledger.append(s_item)
        pt_ledger.append(item)
         #listbox.insert(END,s_item )

    else:
        rejects.append(s_item)
        pt_rejects.append(item)
        #rejects.put(s_item)
        
    utils.write_wb("Verified.xlsx",pt_ledger)
    utils.write_wb("Rejected.xlsx",pt_rejects)            
#mainloop()

