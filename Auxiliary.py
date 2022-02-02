from datetime import datetime
from RSA import PAD_LENGTH
from hashlib import sha256
from secrets import choice




class user():
    global PAD_LENGTH
    def __init__(self, name, public_key, sock ):
        self.name = name
        self.public_key = public_key
        self.sock = sock
        self.e = pow(2,16) + 1

    def __getstate__(self):
        return (self.name, self.public_key)

    def __setstate__(self, dic):
        self.name = dic[0]
        self.public_key = dic[1]

    def set_sock(self, sock):
        self.sock = sock
        
    def __eq__(self, other):
        if (isinstance(other, user)):
            return self.name == other.name and self.sock == other.sock

        return False

    def __hash__(self):
        return id(self)

    def __getitem__():
        pass

    #String -> Encypted int
    def encrypt(self, message, pad = ''):

        if isinstance(message, bytes):
            message = int.from_bytes((message) , byteorder= "little")
            return pow(message, self.e, self.public_key)


        if pad == "":
            scramble = "abcdefghijklmpqrstuvwyxzABCDEFGHIJKLMNOPQRSTUVWYXYZ1234567890 !@#$%^&*()"
            for i in range(PAD_LENGTH):
                message += choice(scramble)
        else:
            message += pad

        message = int(message.encode("utf-8").hex(), 16)
        return str(pow(message, self.e, self.public_key))

    # cypher == String encyption
    def unsign(self, signature, trim_pad = True):

        if isinstance(signature, bytes):
            signature = signature.decode()
        if not isinstance(signature, int):
            signature = int(signature)

        signature = pow( signature, self.e, self.public_key)

        try:
            if trim_pad:
                return bytes.fromhex('{:x}'.format(signature) ).decode()[:-PAD_LENGTH]
            else:
                return bytes.fromhex('{:x}'.format(signature)).decode()

        except UnicodeError:
            print("UNICODE ERROR: possibul message was to long")







class message():

        def __init__(self, content, flag , author, recipient ):
            self.content = content
            self.flag = flag
            self.author = author
            self.recipient = recipient
            self.time = datetime.timestamp(datetime.now())


#string goes in hashed string goes out
def hash_it(plain_str):
    if not isinstance(plain_str, str):
        plain_str = str(plain_str)
    plain_str = plain_str.encode()
    hash = sha256()
    hash.update(plain_str)
    hash.digest()
    return hash.hexdigest()

# String to int
def string_to_int( plain_text):
    return int(plain_text.encode().hex(), 16)

def int_to_string(num):
    return bytes.fromhex('{:x}'.format(num) ).decode()





