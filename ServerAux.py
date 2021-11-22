from datetime import datetime


class user():
    def __init__(self, name, public_key, sock ):
        self.name = name
        self.public_key = public_key
        self.sock = sock

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
        return false

    def __getitem__():
        pass


class message():

        def __init__(self, content, flag , author, recipient ):
            self.content = content
            self.flag = flag
            self.author = author
            self.recipient = recipient
            self.time = datetime.timestamp(datetime.now())



