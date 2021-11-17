# Import socket module
import socket, ServerAux, pickle
import tkinter as tk
from time import *


sock = socket.socket()
def login(port, name):
    global sock
    clients = list()
     
    # Create a socket object
    sock = socket.socket()        
     
    # Define the port on which you want to connect
    port = 12340 + int(port)
     
    # connect to the server on local computer
    sock.connect(('127.0.0.1', port))
    user = name.strip()
    public =1
    sock.sendall( (user + "-" + str(public) ).encode('UTF-8') )
    print(sock.recv(32).decode())

def send_to( name, message):
    global sock
    
    sock.sendall(pickle.dumps([ "<Encrypted>", name, message]))
    print("sent")
    #data  = sock.recv(2048)

    #print(pickle.loads(data))
    
def recive():
    global sock
    while True:

       # try:
            #msg = sock.recv(20).decode()
            #print(msg)
            #if msg != "":
                
                #return msg
                
            
        data = pickle.loads(sock.recv(2048))
        
        print(data)
        if data[0] == "<Encrypted>":
          return data[2]
        #except:
            #pass
            #print("whooops")



def get_users():
    sock.sendall(pickle.dumps(["<Get Users>"]) )
    clients = pickle.loads(sock.recv(2048))
    print(clients)

