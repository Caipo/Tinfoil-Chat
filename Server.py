import socket,sys, threading
from ServerAux import *
from _thread import *

from time import *


sock, port = socket.socket(),12345
sock.bind(('', port))        
print ("socket binded to %s" %(port))
 
# put the socket into listening mode

clients = list()


print_lock = threading.Lock()

        
 
def get_connection():
  global clients, new_con

  sock.listen(5)  
  print ("socket is listening")
  connection, addr = sock.accept()    
  print ('Got connection from', addr )
  identy = connection.recv(2048).decode().split("-")

 for client in clients:
     if client.name == identy[0]:
         connection.close()
         
     
  
  clients.append( user( identy[0], identy[1], identy[2], connection, addr) )
  print(identy[0] + " has connected")


def get_message():
    global clients
    
    for client in clients:
        message = client.c.recv(2048).decode()
        if message != "":
            print(message )
        sleep(1)


new_con = threading.Thread(target = get_connection, args = ())
new_con.start()

get_mess =  threading.Thread(target = get_message, args = ())
get_mess.start()
    
while True:
    
    if not new_con.is_alive():
        new_con = threading.Thread(target = get_connection, args = ())
        new_con.start()

    if not get_mess.is_alive():
        get_mess =  threading.Thread(target = get_message, args = ())
        get_mess.start()
    sleep(1)
    
