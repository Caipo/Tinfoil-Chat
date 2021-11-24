import socket,pickle
from threading import Thread, Lock
from time import sleep
from ServerAux import *
from random import randint



def get_connection():
    global clients

    #Get New Connection
    sock.listen(1)  
    print ("Socket Is Listening")
    client_sock, addr = sock.accept()    
    print ('Got connection from', addr )

    data = pickle.loads(client_sock.recv(2048))
    data.set_sock(client_sock)

    for client in clients:
      if client == data:
        client_sock.sendall(b"Username Already Taken")
        client_sock.close()
        return
      


    #Welcom Waggon
    client_sock.sendall(b"Welcom To Tinfoil Chat" )
    clients.add(data)
    print(clients)
    Thread(target = get_message, args = (data,)).start()
    print(data.name+ " has connected")


def get_message(client):
    global clients
    print("get message running")

    while client in clients:

      try:
          data = pickle.loads(client.sock.recv(2048))
          print(data.flag)

          if data.flag == "<Get Users>":
            print("gibing clinets")
            client.sock.sendall(   pickle.dumps(clients )    )

          elif data.flag == "<Close>":
              print(client.name, " Has Disconnecte")
              client.sock.close()
              clients.remove(client)
              print(clients)
              return

          elif data.flag == "<Encrypted>":
            

            for user in clients:


                user.sock.sendall( pickle.dumps(data) )





      
      except:
          print(client.name , " Has Disconnecte")
          client.sock.close()
          clients.remove(client)
          print(clients)
          return



if __name__ == "__main__":
  #Opening connections
  sock = socket.socket()
  port = 12340 + randint(0, 9)
  ip = '192.168.1.68'
  sock.bind((ip, port))
  print(f"{ip} : {port}")

  
  clients = set()

  #Threading for new connections
  print_lock = Lock()
  new_con = Thread(target = get_connection, args = ())
  new_con.start()


  #Main Loop
  while True:
      if not new_con.is_alive():
          new_con = Thread(target = get_connection, args = ())
          new_con.start()
      sleep(1)

