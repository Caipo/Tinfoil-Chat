from secrets import SystemRandom, choice
from random import randint
from math import lcm
from pickle import loads
from backend.lists import primes_list
from dotenv import load_dotenv
import os

#How long the padding should be
PAD_LENGTH = 10

class RSA:
    global primes_list, PAD_LENGTH
        
    def generate_key(self, bits):
        global p, q

        # This is the famous miller rabin test for possibul prime
        def rabin(n):
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

            # We do 2 * random + 1 sp we dont get an even number which will clearly not be prime
            key = 2 * SystemRandom().randint( pow(2,bits - 1) //2  , pow(2,bits)//2  - 1)  + 1


            # Using the fundelmental theorom of arthimatic to test if our key is prime
            for i in primes_list:
                if( pow(key, 1 , i) == 0):
                    is_prime = False
                    break

            #Lastly we do miler rabin
            if(is_prime):
                if(rabin(key)):
                    return key


    def __init__(self, bits, from_env = False ):
        
        if from_env:
            print('loading env')
            load_dotenv()
            self.d =int(os.getenv("D"))
            self.e = int(os.getenv("E"))
            self.public_key = int(os.getenv('PUBLIC_KEY'))
    
        else:
            #Basic RSA 
            p = self.generate_key(bits)
            q = self.generate_key(bits)

            self.public_key  = p*q
            private = lcm(p -1, q - 1)
            
            
            self.e = pow(2,16) + 1
            self.d = pow(self.e, -1,  private)
            del p, q, private




    # String goes in encrypted int goes out
    def encrypt(self, message, pad =''):

        if isinstance(message, bytes):
            message = int.from_bytes(message, byteorder="little")
            return pow(message, self.e, self.public_key) #Note this has no padding but we dont need it


        if pad == '':
            pad = "abcdefghijklmpqrstuvwyxzABCDEFGHIJKLMNOPQRSTUVWYXYZ1234567890 !@#$%^&*()"
            for i in range(PAD_LENGTH):
                message += choice(pad)

        else:
            message += pad

        message = int(message.encode().hex(), 16)


        return pow(message, self.e, self.public_key)

    #Encrypted int goes in String goes out
    def decrypt(self, cypher, trim_pad = True, is_object = False):
        global PAD_LENGTH
        if is_object:

            cypher = pow( int(cypher), self.d, self.public_key)
            return loads(cypher.to_bytes(   int(cypher.bit_length() / 8) + 1 , byteorder='little'))


        if isinstance(cypher, bytes):
            cypher = cypher.decode()

        if not isinstance(cypher, int):
            cypher = int(cypher)

        cypher = pow( cypher, self.d, self.public_key)


        if trim_pad:
            return bytes.fromhex('{:x}'.format(cypher)).decode('utf-8')[:-PAD_LENGTH]
        else:
            return bytes.fromhex('{:x}'.format(cypher)).decode('utf-8')


    # RSA sign a message is just encrypting with the private key
    # No one knows your private key so only you could have sign the message
    def sign(self, message, pad = ''):
        global PAD_LENGTH
        if not isinstance(message, str):
            message = str(message)

        if pad == '':
            scramble = "abcdefghijklmpqrstuvwyxzABCDEFGHIJKLMNOPQRSTUVWYXYZ1234567890 !@#$%^&*()"
            for i in range(PAD_LENGTH):
                message += choice(scramble)
        else:
            message += pad

        message = int(message.encode("utf-8").hex(), 16)
        return  pow(message, self.d, self.public_key)


    def gen_pad(self):
        global PAD_LENGTH
        scramble = "abcdefghijklmpqrstuvwyxzABCDEFGHIJKLMNOPQRSTUVWYXYZ1234567890 !@#$%^&*()"
        pad = ''
        for i in range(PAD_LENGTH):
            pad += choice(scramble)
        return pad


    
    #Decrypting a signature with the public key
    def unsign(self, signature, trim_pad = True):
        if isinstance(signature, bytes):
            signature = signature.decode()
        if not isinstance(signature, int):
            signature = int(signature)

        signature = pow( signature, self.e, self.public_key)

        try:
            if trim_pad:
                return bytes.fromhex( '{:x}'.format(signature)).decode('utf-8')
            else:
                return bytes.fromhex('{:x}'.format(signature)).decode('utf-8')[:-PAD_LENGTH]

        except UnicodeError:
            print("UNICODE ERROR: possibul message was to long")


# If you want to see how the encryption works
if __name__ == "__main__":
    import time

    start = time.time()
    me = RSA(2048)
    end = time.time()
    print(end - start)

    while True:
        print(blap := str(input("message: ")))
        print( bloop := me.encrypt(blap))
        print(me.decrypt(bloop))
