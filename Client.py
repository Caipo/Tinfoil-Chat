# Import socket module
import socket            
 
# Create a socket object
sock = socket.socket()        
 
# Define the port on which you want to connect
port = 12345               
 
# connect to the server on local computer
sock.connect(('127.0.0.1', port))
user = input("name")
public =1
e = 1
sock.sendall( (user + "-" + str(public) + "-" + str(e) ).encode('UTF-8') )

 
# receive data from the server and decoding to get the string.

# close the connection




