# Tinfoil-Chat
Simple chat app that uses military grade encryption (2048 bit RSA)


## Scope 

The intention of this project is to create an simple chat app that implemnts RSA purly from default python imports (no third party librarys).


## Server set up

1) Run the server file.
2) enter your ip, port and password.
3) Wait for connections.

Note that the password is unsecure on your system and is in the python shell. Use only on secure hardware



## Client set up

1) Run the Gui File.
2) Wait for your RSA keys to generate.
3) Enter in the global ip of the server your connecting to, port and password.

Note: Due to this program using pickle you should NEVER connect to a server that you dont trust.


## Security Vunrbillty 

* The client uses the pickel library "It is possible to construct malicious pickle data which will execute arbitrary code during unpickling. Never unpickle data that could have come from an untrusted source, or that could have been tampered with."
* If the client or server loses their public keys its possibul to falseify messages. 



















