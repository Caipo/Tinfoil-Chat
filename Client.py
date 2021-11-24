import socket, pickle, sys
from ServerAux import *


sock = socket.socket()
clients = set()
current_user = ""

def logout(author):
    sock.send( pickle.dumps( message( "", "<Close>" , author) ))

def login(port, name, ip):
    global sock, clients, current_user
    
     
    # Create a socket object
    sock = socket.socket()        
     
    # Define the port on which you want to connect
    port = int(port)
    ip = str(ip)
     
    # Connect to the server
    sock.connect((ip, port))
    public = 1

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
    global sock, current_user

    try:
        if not isinstance(current_user, str):
            to_send = message(content,   "<Encrypted>",  current_user.name, recipient )
            sock.sendall(pickle.dumps(to_send))  # TO DO FIX USER
    except AttributeError:
        print("Failed to make user")



def receive_data():
    global sock, clients



    while True:
        data = pickle.loads(sock.recv(2048))

        if isinstance(data, message):
            return data

        if isinstance(data, set):
            return data

def get_users():
    global current_user
    try:

        sock.sendall(pickle.dumps(message("", "<Get Users>", current_user.name,  "")) )
    except AttributeError:
        print("Failed to make user")



