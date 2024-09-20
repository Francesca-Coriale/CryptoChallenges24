/**
 * The specification of the CRAZY protocol includes the following operations:
 * 
 * 1. Generate two strong random 128-bit integers, name them rand1 and rand2
 * 
 * 2. Obtain the first key as
 * k1 = (rand1 + rand2) * (rand1 - rand2) mod 2^128
 * 
 * 3. Obtain the second key as
 * k2 = (rand1 * rand2) / (rand1 - rand2) mod 2^128
 * 
 * 4. Encrypt k2 using k1 using a stron encryption algorithm (and mode) of your choice
 * call it enc_k2.
 * 
 * 5. Generate an RSA keypair with a 2048 bit modulus.
 * 
 * 6. Encrypt enc_k2 using the just generated RSA key.
 * 
 * Implement in C the protocol steps described above, make the proper decisions when
 * the protocol omits information.
 * 
 **/

#include <stdio.h>
#include <openssl/bn.h>
#include <openssl/evp.h>
#include <openssl/rand.h>
#include <openssl/err.h>
#include <openssl/rsa.h>
#include <openssl/pem.h>

#define ENCRYPT 1
#define DECRYPT 0
#define KEY_LENGTH  2048

void handle_errors(){
    ERR_print_errors_fp(stderr);
    abort();
}

int main(){

    /* Load the human readable error strings for libcrypto */
    ERR_load_crypto_strings();
    /* Load all digest and cipher algorithms */
    OpenSSL_add_all_algorithms();
    
    BIGNUM *rand1 = BN_new();
    BIGNUM *rand2 = BN_new();
    BN_rand(rand1,128,0,1);
    BN_rand(rand2,128,0,1);

    BIGNUM *sum = BN_new();
    BIGNUM *sub = BN_new();
    BN_add(sum,rand1,rand2);
    BN_sub(sub, rand1, rand2);

    BN_CTX *ctx = BN_new();
    BIGNUM *key1 = BN_new();
    BIGNUM *base = BN_new();
    BIGNUM *exp = BN_new();
    BIGNUM *m = BN_new();
    BN_set_word(base, 2);
    BN_set_word(exp, 128);
    BN_exp(m,base,exp,ctx);
    BN_mod_mul(key1, sum, sub, m, ctx);

    BIGNUM *key2 = BN_new();
    BIGNUM *mult = BN_new();
    BN_mul(mult,rand1,rand2,ctx);
    
    BIGNUM *div=BN_new();
    BIGNUM *rem=BN_new();
    BN_div(div,rem,mult,sub,ctx);
    BN_mod(key2, div, m, ctx);

//Encrypt k2 with k1 and a strong encryption algorithm and mode (AES-128-CBC) and output enc_k2
    char key1_hex[128] = BN_bn2hex(key1);
    char key2_hex[128] = BN_bn2hex(key2); 

    EVP_CIPHER_CTX *ctx2 = EVP_CIPHER_CTX_new();

    if(!EVP_CipherInit(ctx2,EVP_aes_128_cbc(), key1_hex, NULL, ENCRYPT))
        handle_errors();

    unsigned char enc_k2[128];
    int update_len, final_len;
    int ciphertext_len=0;

    if(!EVP_CipherUpdate(ctx2,enc_k2,&update_len, key2_hex, strlen(key2_hex)))
        handle_errors();

    ciphertext_len+=update_len;
    printf("update size: %d\n",ciphertext_len);

    if(!EVP_CipherFinal_ex(ctx2,enc_k2+ciphertext_len,&final_len))
        handle_errors();
    ciphertext_len+=final_len;

//Generate an RSA keypair with a 2048 bit modulus.
    EVP_PKEY *rsa_keypair = NULL;
    int bits = 2048;
    if((rsa_keypair = EVP_RSA_gen(bits)) == NULL ) 
        handle_errors();

//Encrypt enc_k2 using the just generated RSA key.
    // Generate key pair
    RSA  *keypair; //RSA data structure
    printf("Generating a fresh RSA (%d bits) keypair...\n", KEY_LENGTH);
    BIGNUM *bn_pub_exp = BN_new();
    BN_set_word(bn_pub_exp,RSA_F4);
    
    keypair = RSA_new();
    if(!RSA_generate_key_ex(keypair, KEY_LENGTH, bn_pub_exp, NULL))
        handle_errors();


    // Encrypt the message
    int encrypted_data_len;
    unsigned char encrypted_data[RSA_size(keypair)];


    if((encrypted_data_len = RSA_public_encrypt(strlen(enc_k2)+1, enc_k2, encrypted_data, keypair, RSA_PKCS1_OAEP_PADDING)) == -1) 
            handle_errors();


    BN_CTX_free(ctx);
    BN_free(rand1);
    BN_free(rand2);
    BN_free(sum);
    BN_free(sub);
    BN_free(m);
    BN_free(mult);
    BN_free(div);
    BN_free(key1);
    BN_free(key2);

    EVP_CIPHER_CTX_free(ctx2);
    return 0;
}
