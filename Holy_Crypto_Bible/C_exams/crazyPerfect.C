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
#define MAX_ENC_LEN 128
#define MAX_BUFFER 1024

void handle_errors(){
    ERR_print_errors_fp(stderr);
    abort();
}



int main(){
    
    ERR_load_crypto_strings();
    OpenSSL_add_all_algorithms();

    BIGNUM *rand1=BN_new();
    BIGNUM *rand2=BN_new();

    /* init the random engine: */
    int rc = RAND_load_file("/dev/random", 64);
    if(rc != 64) {
        handle_errors();
    }

    // generate a 128 bit prime
    // BN_generate_prime_ex is deprecated in OpenSSL 3.0 use the one below instead (also has a context for more generic generation) 
    // int BN_generate_prime_ex2(BIGNUM *ret, int bits, int safe, const BIGNUM *add, const BIGNUM *rem, BN_GENCB *cb, BN_CTX *ctx);
    if (!BN_generate_prime_ex(rand1, 128, 0, NULL, NULL, NULL)) 
        handle_errors();

    if (!BN_generate_prime_ex(rand2, 128, 0, NULL, NULL, NULL)) 
        handle_errors();

    BIGNUM *k1=BN_new();
    BIGNUM *sum=BN_new();
    BIGNUM *sub=BN_new();
    BN_add(sum,rand1,rand2);
    BN_sub(sub,rand1,rand2);

    BN_CTX *ctx=BN_CTX_new();
    BIGNUM *base=BN_new();
    BIGNUM *exp=BN_new();
    BIGNUM *mod=BN_new();
    BN_set_word(base, 2);
    BN_set_word(exp, 128);
    BN_exp(mod, base, exp, ctx);
    BN_mod_mul(k1,rand1,rand2,mod,ctx);

    BIGNUM *k2=BN_new();
    BIGNUM *tmp=BN_new();
    BIGNUM *mul=BN_new();
    BN_mul(mul,rand1,rand2,ctx);
    BN_div(tmp, NULL, mul, sub, ctx);
    BN_mod(k2, tmp, mod, ctx);

//Encrypt k2 using k1 using a stron encryption algorithm (and mode) of your choice call it enc_k2.
// Algorithm = AES-128-CBC
    char *k1_hex = BN_bn2hex(k1);
    char *k2_hex = BN_bn2hex(k2);

// pedantic mode: check NULL
    EVP_CIPHER_CTX *EVPctx = EVP_CIPHER_CTX_new();

    if(!EVP_CipherInit(EVPctx,EVP_aes_128_cbc(), k1_hex, NULL, ENCRYPT))
        handle_errors();
    
    unsigned char enc_k2[MAX_ENC_LEN];

    int update_len, final_len;
    int enck2_len=0;
    int n_read;
    unsigned char buffer[MAX_BUFFER];


    while((n_read = fread(buffer,1,MAX_BUFFER,k2_hex)) > 0){
        if(enck2_len > MAX_ENC_LEN - n_read - EVP_CIPHER_CTX_block_size(EVPctx)){ //use EVP_CIPHER_get_block_size with OpenSSL 3.0+ instead
            fprintf(stderr,"The file to cipher is larger than I can manage\n");
            abort();
        }
    
        if(!EVP_CipherUpdate(EVPctx,enc_k2+enck2_len,&update_len,buffer,n_read))
            handle_errors();
        enck2_len+=update_len;
    }

    if(!EVP_CipherFinal_ex(EVPctx,enc_k2+enck2_len,&final_len))
        handle_errors();

    enck2_len+=final_len;

//Generate an RSA keypair with a 2048 bit modulus.
    RSA *keypair = NULL;
    BIGNUM *bne = NULL;

    int bits = 2048;
    unsigned long e = RSA_F4;

    // 1. generate the RSA key
    bne = BN_new();
    if(!BN_set_word(bne,e))
        handle_errors();

    keypair = RSA_new();
    if(!RSA_generate_key_ex(keypair, bits, bne, NULL)) /* callback not needed for our purposes */
        handle_errors();
    
// Encrypt enc_k2 using the just generated RSA key.
    int encrypted_data_len;
    unsigned char encrypted_data[RSA_size(keypair)];


    if((encrypted_data_len = RSA_public_encrypt(strlen(enc_k2)+1, enc_k2, encrypted_data, keypair, RSA_PKCS1_OAEP_PADDING)) == -1) 
            handle_errors();



    EVP_CIPHER_CTX_free(EVPctx);
    CRYPTO_cleanup_all_ex_data(); // deprecated since version 1.1.0
    /* Remove error strings */
    ERR_free_strings(); // deprecated since version 1.1.0



    
    



    return 0;
}