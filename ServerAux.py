class user():
    
    def __init__(self, user, public, e, c, addr ):
        self.e = e
        self.public = public
        self. user = user
        self.c = c
        self.addr = addr
        
    def encrypt(self, message):
        pad = "abcdefghijklmpqrstuvwyxzABCDEFGHIJKLMNOPQRSTUVWYXYZ1234567890 !@#$%^&*()"
        for i in range(20):
            message += choice(pad)
            
        message = int(message.encode("utf-8").hex(),16)
        return pow( message, self.e, self.public)
