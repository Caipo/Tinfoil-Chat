from sympy import sieve
from secrets import SystemRandom, choice
from random import randint
from math import lcm

class RSA:
    sieve.extend_to_no(10000)
        
    def generate_key(self, bits):

        def rabin( n):
            for k in range(64):
                i  = 0
                b = n - 1

                while pow(b,1, 2) == 0:
                    i = i + 1
                    b = b // 2

                a = randint(2, n - 2)


                x = pow(a, b, n)
                if  (x  == 1 or x  == n - 1):

                    for j in range(1,  i - 1):
                        x = pow(x, 2,  n)
                        
                        if(x == 1 or  not x == n - 1):
                            return False

                else:
                    return False

            return True

        while(True):
            is_prime = True
            key = 2 * SystemRandom().randint( pow(2,bits - 1) //2  , pow(2,bits)//2  - 1)  + 1

            for i in sieve._list:
                if( pow(key, 1 , i) == 0):
                    is_prime = False
                    break
            
            if(is_prime):
                if( rabin(key) ):
                    return key
            

    def __init__(self, bits):
    

        p =  self.generate_key(bits)
        q =  self.generate_key(bits) 


        self.public  = p*q
        private = lcm(p -1, q - 1)
        
        
        self.e = pow(2,16) + 1
        self.d = pow(self.e, -1,  private)
        del p, q, private


    def encrypt(self, message):
        
        pad = "abcdefghijklmpqrstuvwyxzABCDEFGHIJKLMNOPQRSTUVWYXYZ1234567890 !@#$%^&*()"
        for i in range(20):
            message += choice(pad)
            
        message = int(message.encode("utf-8").byte(),16)
        return pow( message, self.e, self.public)
            
    def decrypt(self, cypher):
        cypher = pow( cypher, self.d, self.public)
        return bytes.fromhex( '{:x}'.format(cypher)).decode('utf-8')[:-20]

    def sign(self, message):
        message  += " \n" + "-"*10  + str( pow(  int(message.encode("utf-8").hex(),16), self.d, self.public) )
        return message

        


    








me = RSA(2048)
