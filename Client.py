import socket, pickle
from ServerAux import *


sock = socket.socket()
clients = list()

def login(port, name):
    global sock, clients
    
     
    # Create a socket object
    sock = socket.socket()        
     
    # Define the port on which you want to connect
    port = 12340 + int(port)
     
    # Connect to the server 
    sock.connect(('127.0.0.1', port))
    public =1

    #Sending our info
    current_user = user( name =  name.strip(), public_key = public,  sock = sock ) 
    sock.sendall( pickle.dumps(current_user) )

    #Seeing if it accepts us
    ser_response = sock.recv(32).decode()
    if ser_response == "Welcom To Tinfoil Chat":
        print(ser_response)
        return True
    else:
        return False


def send_to( recipient, content):
    global sock

    to_send = message(content,   "<Encrypted>",  "nick", recipient )
    sock.sendall(pickle.dumps(to_send))  # TO DO FIX USER

def receive_data():
    global sock, clients

    while True:
        data = pickle.loads(sock.recv(2048))

        if isinstance(data, message):
            if data.flag == "<Encrypted>":
                return data

        if isinstance(data, list):
            return data

            
        

        
def get_users():
    sock.sendall(pickle.dumps(message("", "<Get Users>", "nick",  "")) )
    #return pickle.loads(sock.recv(2048))


