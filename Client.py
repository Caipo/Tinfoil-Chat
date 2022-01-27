import socket
from pickle import dumps, loads
from Auxiliary import *
from RSA import *


sock = socket.socket()
clients = set()
current_user = ""
server = ""


def logout(author):
    sock.send( dumps( message( "", "<Close>" , author)))

def secure_login(ip, port, server_password):
    global sock, clients, current_user, my_RSA

    # Create a socket object
    sock = socket.socket()

    my_RSA = RSA(1024)

    # Define the port on which you want to connect
    port = int(port)
    ip = str(ip)

    # Connect to the server
    sock.connect((ip, port))

    current_user = user("bloop",   my_RSA.public_key, sock)

    #Phase 1 (key echange)
    server_public_key = int(sock.recv(2048).decode())#Getting server public key
    server = user("Server", server_public_key, sock) #Loding our info into object
    server.sock.sendall( str(my_RSA.public_key).encode()) #Sending our public key

    #Phase 2 (Client Verifycation)



    server.sock.sendall( str(server.encrypt( server_password + hash_it(my_RSA.public_key) ) ).encode())  #Sending the password with key hash
    ser_response = my_RSA.decrypt(  int(server.sock.recv(2048).decode('utf-8')) )


    if not "Welcome To Tinfoil Chat" in  ser_response:
        return False




    if my_RSA.decrypt( int(server.sock.recv(2048).decode('utf-8'))) ==server_password + hash_it(str(server_public_key)):
        current_user = user(name=ser_response.split(" ")[-1], public_key=my_RSA.public_key, sock=sock)
        return True


def send_to(recipient, content):
    global sock, current_user
    print("sending")
    try:
        if not isinstance(current_user, str):
            to_send = message(content,   "<Encrypted>",  current_user.name, recipient )
            sock.sendall(dumps(to_send))  # TO DO FIX USER

    except AttributeError:
        print("Failed to make user")



def receive_data():
    global sock, clients

    while True:
        data = loads(sock.recv(2048))

        if isinstance(data, message):
            return data

        if isinstance(data, set):
            return data

def get_users():
    global current_user
    try:

        sock.sendall(dumps(message("", "<Get Users>", current_user.name,  "")) )
    except AttributeError:
        print("Failed to make user")



if __name__ == "__main__":
    secure_login("192.168.1.68", int(str(1234) + input("port ")), input( "Password: ") )