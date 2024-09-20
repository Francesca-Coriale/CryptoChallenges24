# A and B want to exchange messages encrypted with AES-128-CBC
# they've agreed on a padding method: 
# if the last block contains RESIDUE_BYTES, it fills the block with
# RESIDUE_BYTES||len_RESIDUE_BYTES (1B)||last_16-1-lenght_RESIDUE_BYTES_of_IV


# B sets up a server that receives IV and ciphertext and stores the dec msg
# if padding is incorrect, server returns b'wrongPAD'.

# we sniff a ciphertext from A to B, 
# we want to GUESS the last 3 bytes of the last block of the ciphertext
# Note: we have access to the ciphertext and the IV

# IDEA: to guess bytes in CBC we use the padding oracle attack
# cosa fa? per ogni byte itera tutte le possibili combinazioni 
# finchè non restituisce OKPAD

# COSA USO? CBCPaddingOracle_client.py 
# (va bene anche CBC_PaddingOracle_Attack, da vedere)


from mysecrets import exam_july21_iv as iv
from mysecrets import exam_july21_ciphertext as ciphertext
from mysecrets import exam_july21_HOST as HOST
from mysecrets import exam_july21_PORT as PORT
import math
from Crypto.Cipher import AES
from pwn import *



def num_blocks(ciphertext, block_size):
    return math.ceil(len(ciphertext)/block_size)

def get_nth_block(ciphertext, n, block_size):
    return ciphertext[(n)*block_size:(n+1)*block_size]

def guess_byte(p,c,ciphertext,block_size):
    # p and c must have the same length
    padding_value = iv[block_size-len(p)-1]
    print("pad="+str(padding_value))
    n = num_blocks(ciphertext,block_size)
    print("n="+str(n))
    current_byte_index= len(ciphertext)-1 -block_size - len(p)
    print("current="+str(current_byte_index))

    # print(p)
    # print(c)
    plain = b'\x00'
    for i in range(0,256):
        # print(i)
        ca = bytearray()
        ca += ciphertext[:current_byte_index]
        ca += i.to_bytes(1,byteorder='big')

        # print(ca)
        for x in p:
            ca += (x ^ padding_value).to_bytes(1,byteorder='big')
        # print(ca)
        ca += get_nth_block(ciphertext,n-1,block_size)
        # print(ca)
        # print("          "+str(ciphertext))

        server = remote(HOST, PORT)
        server.send(iv)
        server.send(ca)
        response = server.recv(1024)

        # print(response)

        if response == b'OKPAD':
            print("found",end=' ')
            print(i)

            p_prime = padding_value ^ i
            plain = bytes([p_prime ^ ciphertext[current_byte_index]])
            if plain == padding_value: #this is not sufficient in the general case, onyl wokrs for the last byte and not always
                continue
            # print(p_prime)
            # print(ciphertext[current_byte_index])
            # print(p_prime ^ ciphertext[current_byte_index])
            c.insert(0,i)
            p.insert(0,p_prime)
            # print(p)
            # print(type(p_prime))
            # x= bytes([p_prime ^ ciphertext[current_byte_index]])
            # break


    return plain

    


if __name__ == '__main__':
    n = num_blocks(ciphertext,AES.block_size)
    plaintext = bytearray()
    
    for i in range(1,n):
        c = []
        p = []

        for j in range(AES.block_size-2,AES.block_size):
            plaintext[0:0] = guess_byte(p,c,ciphertext,AES.block_size)
            print(plaintext)


