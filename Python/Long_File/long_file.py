import binascii

def decode_to_hex(input_file, output_file):
    with open(input_file, "rb") as f_input, open(output_file, "wb") as f_output:
        # Read the entire content of the input file as bytes
        data = f_input.read()
        # Convert bytes to hexadecimal representation
        hex_data = binascii.hexlify(data)
        #hex_data = data.hex()
        # Write the hexadecimal representation to the output file
        f_output.write(hex_data)

# Example usage:
input_file = "file.enc"
output_file = "hex_file.enc"
decode_to_hex(input_file, output_file)