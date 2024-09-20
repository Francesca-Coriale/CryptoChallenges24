// How DH works:
// choose p and q
// S chooses a and generates X = q^a mod p
// C chooses b and generates Y = q^b mod p
// S and C exchange X and Y and then 
// S computes Y^a mod p
// C computes X^b mod p
// at the end the key is q^(ab) mod p

#include <stdio.h>
#include <openssl/bn.h>
#include <openssl/evp.h>
#include <openssl/rand.h>
#include <openssl/err.h>

void handle_errors(){
    ERR_print_errors_fp(stderr);
    abort();
}

//client side
int main(){
    /* Load the human readable error strings for libcrypto */
    ERR_load_crypto_strings();
    /* Load all digest and cipher algorithms */
    OpenSSL_add_all_algorithms();

    /*
    int BN_generate_prime_ex(BIGNUM *ret,int bits,int safe, const BIGNUM *add,
        const BIGNUM *rem, BN_GENCB *cb);
    */
    BIGNUM *p=BN_new();
    BIGNUM *q=BN_new();

    BIGNUM *b = BN_new();

    /* init the random engine: */
    int rc = RAND_load_file("/dev/random", 64);
    if(rc != 64) {
        handle_errors();
    }

    if (!BN_generate_prime_ex(p, 64*8, 0, NULL, NULL, NULL)) 
        handle_errors();

    if (!BN_generate_prime_ex(q, 64*8, 0, NULL, NULL, NULL)) 
        handle_errors();

    // b has to be max p-2 so i use 63 bytes numbers 
	BN_rand(b,63*8,0,1);

    //generate q^b mod p
    BN_CTX *ctx = BN_CTX_new();
    BIGNUM *res = BN_new();
    if (!BN_mod_exp(res,q,b,p,ctx)) {
        ERR_print_errors_fp(stdout);
        exit(1);
    }
    
    send_to_sara(p);
    send_to_sara(q);
    send_to_sara(res);
    //receive from S res2 = q^a mod p
    BIGNUM *res2 = receive_from_sara();

    //compute res2^b mod p
    BIGNUM *key = BN_new();
    if (!BN_mod_exp(key,res2,b,p,ctx)) {
        ERR_print_errors_fp(stdout);
        exit(1);
    }

    BN_free(p);
    BN_free(q);
    BN_free(b);
    BN_free(res);
    BN_free(res2);
    BN_free(key);
    BN_CTX_free(ctx);

    return 0;
}

// Finally answer the following question: what CARL and SARA have to do if they want
// to generate an AES-256 key?

// One of the two has to generate the AES-256 key using PRNG
// and then it will be encrypted using the key K obtained from DH as
// AES*K mod p = AES_KEY
// The other side will decrypt it with AES_KEY*K^-1 mod p
// And both will have the AES-256 key.