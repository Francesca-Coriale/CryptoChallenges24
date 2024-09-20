
otp = 'd337d7b073cc823322d373cf2ceeedd54b2984ff81c6d3d5acadd35604079cce'
instr = '0'*64

###
otp_byte = otp.encode()
print(otp_byte)


instr_byte = instr.encode()
print(instr_byte)

xor = bytes([d ^ o for d,o in zip(instr_byte, otp_byte)])
print(xor)
#####

#data = bytes.fromhex(instr.strip())
#if len(instr) != 32:
    #print("Data must be 32 bytes long")
    #exit()

data = bytes([d ^ o for d,o in zip(xor, otp_byte)])
print(data)


