from datetime import datetime 

class user():
    
    def __init__(self, name, public, c, addr ):
        self.name = name
        self.public = public
        self.c = c
        self.addr = addr

    def get_array(self):
        return [ self.name, self.public]
        

    def __getitem__():
        pass

'''
class message():

        def __init__(self, content, flag ,author, recipient ):
        self.content = content
        self.flag = flag
        self.author = author
        self.recipient = recipient
        self.time = datetime.now()
'''
