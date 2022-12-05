import socket
from backend.auxiliary import *
from backend.rsa import *

# THIS FILE CONTAINS ALL THE NETWORK AND ENCRYPTION CODE TO WORK IN THE BACKGROUND OF THE CLINET

my_RSA = ""
sock = socket.socket()
clients = set()
current_user = ""
server = ""

def generate_RSA():
    global my_RSA

    if os.path.exists('.env'):
        print('generating key')
        my_RSA = RSA(2048, True)

    else:
        print('Loading keys')
        my_RSA = RSA(2048)

        with  open('.env', 'w') as file:
            file.write(f'D = "{my_RSA.d}"\n') 
            file.write(f'E = "{my_RSA.e}"\n') 
            file.write(f'PUBLIC_KEY = "{my_RSA.public_key}"') 
        file.close()

    return my_RSA


def secure_login(ip, port, server_password):
    global sock, clients, current_user, my_RSA, server

    # See Read me for the theory

    # Create a socket object
    sock = socket.socket()

    if my_RSA == "":
        raise Exception("You didn't generate client RSA")

    print("Generating RSA")

    # Define the port on which you want to connect
    port = int(port)
    ip = str(ip)

    # Connect to the server
    sock.connect((ip, port))

    current_user = user("bloop", my_RSA.public_key, sock)

    # Phase 1 (key echange)
    print("Exchanging Keys")

    server_public_key = int(sock.recv(2048).decode())  # Getting server public key
    server = user("Server", server_public_key, sock)  # Loding our info into object
    server.sock.sendall(str(my_RSA.public_key).encode())  # Sending our public key

    # Phase 2 (Client Verifycation)
    print("Verifying to server")

    server.sock.sendall(str(server.encrypt(
        server_password + hash_it(my_RSA.public_key))).encode())  # Sending the password with key hash
    ser_response = my_RSA.decrypt(int(server.sock.recv(2048).decode('utf-8')))

    if not "Welcome To Tinfoil Chat" in ser_response:
        return False

    print("Sever verifing back")
    if my_RSA.decrypt(int(server.sock.recv(2048).decode('utf-8'))) == server_password + hash_it(str(server_public_key)):
        current_user = user(name=ser_response.split(" ")[-1], public_key=my_RSA.public_key, sock=sock)
        return True


def send_to(content):
    global sock, current_user
    print("sending")

    # Reciving the encrypted data
    encrpted_message = str(server.encrypt("<message>" + content))
    sock.sendall((encrpted_message + ":" + str(my_RSA.sign(hash_it("<message>" + content)))).encode())


def receive_data():
    global sock, clients, server
    while True:
        data = (sock.recv(2048)).decode().split(":")

        try:
            if hash_it(data[0]) == server.unsign(data[1]):

                data = my_RSA.decrypt(data[0], is_object=True)
                if isinstance(data, message):
                    return data

                if isinstance(data, set):
                    return data
            else:
                print("Message Authentication Failed")

        # If there is no message, we don't do antyhing even though this line of code is pretty scarry.
        except IndexError:
            pass
# We just send a message telling the server to give us an updated server log.
# Come to think of it we could just have the server do it without asking which i may implement later
def get_users():
    global current_user
    encrpted_message = str(server.encrypt("<users>"))
    sock.sendall((encrpted_message + ":" + str(my_RSA.sign(hash_it("<users>")))).encode())


# Used to test logging in without a gui with my local ip
if __name__ == "__main__":
    secure_login("192.168.1.68", int(str(1234) + input("port ")), input("Password: "))
