#Read the code chall.py. If you really understood it, you can correctly guess the mode. 
# If you do it with a probability higher than 2^128 you'll get the flag.
# nc 130.192.5.212 6531 

from pwn import *


def resolve(otp):
    instr = '0'*64
    otp_byte = bytes.fromhex(otp)
    instr_byte = bytes.fromhex(instr)
    #print(instr_byte)

    xor = bytes([d ^ o for d,o in zip(instr_byte, otp_byte)])
    return xor.hex()

def compare(output_str):
    midpoint = len(output_str)//2
    if output_str[:midpoint] == output_str[midpoint:]:
        return "ECB"
    else:
        return "CBC"

#conn = process(["python3","chall_1.py"])
conn = remote('130.192.5.212', 6531)
for i in range(128):
    print(f"connection #{i}")
    print(conn.recvline())
    otp_line = str(conn.recvline(), 'utf-8')
    split = otp_line.split()
    otp = split[4]
    print(f"otp: ", otp)

    data = resolve(otp) #in this way I have 32 bits all zeros i.e. two blocks of 16 bits identical (così vedo se è ECB)
    print(f"data to send: ", data)
    conn.sendline(data)

    data_output = conn.recvline()
    output_str = str(data_output, 'utf-8').strip().split()[-1]
    print(f"Output: ", output_str)
    print(conn.recvline())
    mode = compare(output_str)
    conn.sendline(mode)
    print(conn.recvline())

print(conn.recvline())
conn.close()


##CRYPTO24{773c8a04-9485-4d54-a166-1e9c079809a4}

