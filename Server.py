import socket,sys, threading, pickle
from ServerAux import *
from _thread import *
from random import *

from time import *


sock, port = socket.socket(), 12340 + randint(0, 9)
sock.bind(('', port))        
print ("socket binded to %s" %(port))
 
# put the socket into listening mode

clients = list()
clients_for_user = list()

print_lock = threading.Lock()

        
 
def get_connection():
  global clients, new_con

  sock.listen(5)  
  print ("Socket Is Listening")
  connection, addr = sock.accept()    
  print ('Got connection from', addr )
  identy = connection.recv(2048).decode().split("-")

  for client in clients:
    if client.name == identy[0]:
      connection.sendall(b"Username Already Taken")
      connection.close()
      return

  connection.sendall(b"Welcom To Tinfoil Chat " + identy[0].encode() )
  new_client = user( identy[0], int(identy[1]), connection, addr)
  threading.Thread(target = get_message, args = (new_client,)).start()
  clients.append(new_client)
  print(identy[0] + " has connected")



def get_message(client):
  global clients
  print("get message running")
  reciver = ""
  while client in clients:
    try:
        data = pickle.loads(client.c.recv(2048))
        print(data)
    
    
        if data[0] == "<Get Users>":
          print(client.get_array() )
          client.c.sendall(pickle.dumps(client.get_array() ))
        
        if data[0] == "<Encrypted>":
          print("got message")
          flag = False
          for i in clients:
              if str(data[1]) == str(i.name):
                  print("forwarding")
                  i.c.sendall( pickle.dumps(data) )
                  #i.c.sendall(b"blap")
                  flag = True
              if not flag:
                  client.c.sendall(  pickle.dumps([ "<Server>", "Could Not Find User"]))
                  
    except:
        print(client.name , " Has Disconnecte")
        client.c.close()
        clients.remove(client)
        print(clients)
    
        return


  

new_con = threading.Thread(target = get_connection, args = ())
new_con.start()





while True:
    
    if not new_con.is_alive():
        new_con = threading.Thread(target = get_connection, args = ())
        new_con.start()


    sleep(1)

