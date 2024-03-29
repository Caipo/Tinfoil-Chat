import socket
import pickle
from threading import Thread, Lock
from time import sleep
from backend.auxiliary import *
from backend.rsa import *
from secrets import randbelow, choice
from backend.lists import name_list

server_RSA = RSA(1024)
server_hash = ""
clients = set()
server_password = ""

def main():
    global server_RSA, server_hash, server_password

    # Opening connections
    sock = socket.socket()
    print("Generating rsa")

    #host_name = socket.getfqdn()
    host_name = socket.gethostname()
    ip = socket.gethostbyname_ex(host_name)[2][0]
    port = int(input("Port: "))
    server_password = input("Server Password: ")
    server_hash = hash_it(server_password)

    sock.bind((ip, port))
    print(f"{ip} : {port}")

    # Threading for new connections
    print_lock = Lock()
    new_con = Thread(target=get_secure_connection, args=(sock,))
    new_con.start()

    # Main Loop
    while True:
        if not new_con.is_alive():
            new_con = Thread(target=get_secure_connection, args=(sock,))
            new_con.start()
        sleep(1)


def get_secure_connection(sock):
    global clients, server_password, server_hash

    # Get New Connection
    sock.listen(1)
    print("Socket Is Listening")
    client_sock, addr = sock.accept()
    print('Got connection from', addr)

    # Phase 1 (key exchange)
    client_sock.sendall(str(server_RSA.public_key).encode('utf-8'))  # Sending client RSA infromation
    client_public_key = int(client_sock.recv(2048).decode('utf-8'))  # Getting his public key
    client_key_hash = hash_it(client_public_key)

    test_client = user("bloop", client_public_key, client_sock)  # Creating a User

    # Phase 2 (Password exchange) in format (PasswordHash) all one string with no buffer
    client_authentication = server_RSA.decrypt(int(client_sock.recv(2048).decode('utf-8')))  # Get the data
    client_password = client_authentication[:-len(client_key_hash)]

    # Compares the passwords and compares the public key hashes
    if hash_it(client_password) == server_hash and client_authentication[len(client_password):] == hash_it(
            test_client.public_key):

        client_name = choice(["Doctor ", "Agent ", "Mr ", "Lord ", "General "]) + name_list.pop(
            randbelow(len(name_list))).capitalize()
        client_sock.sendall(str(test_client.encrypt(str("Welcome To Tinfoil Chat " + client_name))).encode())

        clients.add(new_client := user(client_name, client_public_key, client_sock))

        # del client_name, client_public_key, client_password, client_key_hash,
        Thread(target=get_message, args=(new_client,)).start()

    else:
        client_sock.sendall(str(test_client.encrypt("Password Not Accepted")).encode())
        client_sock.close()

    # Phase 3 showing the client that your legit
    client_sock.sendall(str(test_client.encrypt(server_password + hash_it(str(server_RSA.public_key)))).encode())


def get_message(client):
    global clients
    print("get message running for ", client.name)

    while client in clients:
        try:
            client_message = client.sock.recv(2048).decode().split(":")

            # If a message wasn't encrypted we disconnect
            try:
                decrypted_message = server_RSA.decrypt(client_message[0])

            except ValueError:
                print(client.name, " Has Disconnecte")
                client.sock.close()
                clients.remove(client)
                print(clients)
                return

            try:
                if client.unsign(client_message[1]) != hash_it(decrypted_message):
                    print("Signature didnt check out")
                    return

            except IndexError:
                print("NO signature found with ", client.name)
                return

                # These are flags that we handel the message

            # The client wants users
            if "<users>" in decrypted_message:
                encrypted_message = str(client.encrypt(pickle.dumps(set([x.name for x in clients]))))
                client.sock.sendall(
                    (encrypted_message + ":" + str(server_RSA.sign(hash_it(encrypted_message)))).encode())

            # The client closed
            elif "<close>" in decrypted_message:
                print(client.name, " Has Disconnecte")
                client.sock.close()
                clients.remove(client)
                return

            # The client sent a message
            elif "<message>" in decrypted_message:
                for user in clients:
                    encrypted_message = str(client.encrypt(pickle.dumps(
                        message(content=decrypted_message[9:], flag="<message>", recipient="", author=client.name))))
                    user.sock.sendall(
                        (encrypted_message + ":" + str(server_RSA.sign(hash_it(encrypted_message)))).encode())

        except Exception as e:
            print(e)
            print(client.name, " Has Disconnecte")
            client.sock.close()
            clients.remove(client)
            print(clients)
            return


if __name__ == "__main__":
    main()
