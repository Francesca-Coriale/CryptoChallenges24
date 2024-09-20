// NONCENSE protocol:
// 1. generate random 256bit number r1
// 2. generate random 256bit number r2
// 3. obtain a key by XOR-ing the two rands, name it key_symm
// 4. generate the RSA keypair of at least 2048 bit modulus
// 5. encrypt the generated RSA keypair using AES-256 with key_symm and obtain the payload

#include <stdio.h>
#include <stdlib.h>
#include <openssl/bn.h>
#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <openssl/err.h>

#include <openssl/evp.h>
#include <string.h>

#define BITS 256
#define ENCRYPT 1
#define DECRYPT 0

void handle_errors(){
    ERR_print_errors_fp(stderr);
    abort();
}


int main(){
    unsigned char r1[BITS/8];
    unsigned char r2[BITS/8];
    unsigned char key_symm[BITS/8];

    if(RAND_load_file("/dev/random", 64) != 64) //optional on Linux
        handle_errors();

    if(!RAND_bytes(r1,(BITS/8)))
        handle_errors();
    if(!RAND_bytes(r2,(BITS/8)))
        handle_errors();

	for (int i = 0; i<BITS/8 ; i++) {
		key_symm[i] = r1[i]^r2[i];
	}

    RSA *rsa_keypair = RSA_new();
    BIGNUM *bne = BN_new();
    
	if(!BN_set_word(bne,RSA_F4))
        handle_errors();
	
	if(!RSA_generate_key_ex(rsa_keypair, 2048, bne, NULL)) /* callback not needed for our purposes */
        handle_errors();
		
	if(!PEM_write_RSAPrivateKey(stdout, rsa_keypair, EVP_aes_256_cbc(), key_symm, strlen(key_symm), NULL, NULL))
        handle_errors();
	
	RSA_free(rsa_keypair);
    BN_free(bne);
	
    CRYPTO_cleanup_all_ex_data();
    ERR_free_strings();
    return 0;
}

