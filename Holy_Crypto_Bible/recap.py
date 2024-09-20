# Considering that the first 16 bytes are guessed as IV
# ciphertext[16:32] is the first block of the encrypted data

from Crypto.Cipher import AES
from pwn import *


from myconfig import HOST,PORT


from mysniffeddata import ciphertext
from mydata import correct_server_answer
from mydata import wrong_server_answer


def num_blocks(ciphertext, block_size):
    return math.ceil(len(ciphertext)/block_size)

#first block is 0
def get_nth_block(ciphertext, n, block_size):
    return ciphertext[(n)*block_size:(n+1)*block_size]

def get_n_blocks_from_m(ciphertext, n, m, block_size):
    return ciphertext[(m)*block_size:(m+n)*block_size]


def guess_byte_first_block(p,c,ciphertext,iv,block_size):
    # p and c must have the same length
    padding_value = len(p)+1
    current_byte_index= block_size - len(p)-1
    
    for i in range(0,256):
        iv_ca = bytearray()
        iv_ca += iv[:current_byte_index]
        iv_ca += i.to_bytes(1,byteorder='big')

        for x in p:
            iv_ca += (x ^ padding_value).to_bytes(1,byteorder='big')

        server = remote(HOST, PORT)
        server.send(iv_ca)
        server.send(ciphertext)
        response = server.recv(1024)
        server.close()

        if response == correct_server_answer:
            print("found",end=' ')
            print(i)

            p_prime = padding_value ^ i
            c.insert(0,i)
            p.insert(0,p_prime)
            break

    return bytes([p_prime ^ iv[current_byte_index]])



if __name__ == '__main__':
    
    iv = ciphertext[:16]
    cipherdata = ciphertext[16:]
    n = num_blocks(cipherdata,AES.block_size)
    plaintext = bytearray()
    
    print(len(ciphertext))
    c = []
    p = []
    for i in range(0,AES.block_size):
        plaintext[0:0] = guess_byte_first_block(p,c,cipherdata,iv,AES.block_size)
    print(plaintext)