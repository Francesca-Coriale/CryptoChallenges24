#include <stdio.h>
#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <openssl/err.h>

#include <openssl/evp.h>
#include <string.h>
#define ENCRYPT 1
#define DECRYPT 0
#define MAX_BUFFER 1024
#define MAX_FILE_LEN 1000000 //1MB


void handle_errors(){
    ERR_print_errors_fp(stderr);
    abort();
}

int main(int argc, char **argv){

    if(argc != 3){
        fprintf(stderr,"Invalid parameters. Usage: %s file_in file_out\n",argv[0]);
        exit(1);
    }

    FILE *f_in;
    if((f_in = fopen(argv[1],"r")) == NULL) {
            fprintf(stderr,"Couldn't open the input file, try again\n");
            abort();
    }

    FILE *f_out;
    if((f_out = fopen(argv[2],"wb")) == NULL) {
            fprintf(stderr,"Couldn't open the output file, try again\n");
            abort();
    }

    /* Load the human readable error strings for libcrypto */
    ERR_load_crypto_strings();
    /* Load all digest and cipher algorithms */
    OpenSSL_add_all_algorithms();

// I cannot encrypt too much data with asymmetric encryption,
// then I need to create a new key (symmetric) to encrypt the message
// and then encrypt this key with the public key of Bob (asymmetric)
    unsigned char key[16];
    unsigned char iv[16];

    /* Generate key and IV random of 128 bytes */
    if(RAND_load_file("/dev/random", 64) != 64)
        handle_errors();
    
    if(!RAND_bytes(key,16))
        handle_errors();
        
    if(!RAND_bytes(iv,16))
        handle_errors();
    
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();

    if(!EVP_CipherInit(ctx,EVP_aes_128_cbc(), key, iv, ENCRYPT))
        handle_errors();

    int length;
    unsigned char ciphertext[MAX_FILE_LEN];

    int n_read;
    unsigned char buffer[MAX_BUFFER];
    int ciphertext_len=0;

    while((n_read = fread(buffer,1,MAX_BUFFER,f_in)) > 0){
        printf("n_Read=%d-",n_read);

        if(ciphertext_len > MAX_FILE_LEN - n_read - EVP_CIPHER_CTX_block_size(ctx)){ //use EVP_CIPHER_get_block_size with OpenSSL 3.0+
            fprintf(stderr,"The file to cipher is larger than I can\n");
            abort();
        }

        if(!EVP_CipherUpdate(ctx,ciphertext,&length,buffer,n_read))
            handle_errors();
        printf("length=%d\n",length);
        if(fwrite(ciphertext, 1, length,f_out) < length){
            fprintf(stderr,"Error writing the output file\n");
            abort();
        }
    }
            
    if(!EVP_CipherFinal_ex(ctx,ciphertext,&length))
        handle_errors();

    printf("lenght=%d\n",length);

    if(fwrite(ciphertext,1, length, f_out) < length){
        fprintf(stderr,"Error writing in the output file\n");
        abort();
    }

// Now I encrypt the symmetric key with the Bob's public key
    EVP_PKEY *pkB;
    EVP_PKEY_CTX* enc_ctx = EVP_PKEY_CTX_new(pkB, NULL);
    if (EVP_PKEY_encrypt_init(enc_ctx) <= 0) {
        handle_errors();
    }
    // Specific configurations can be performed through the initialized context
    if (EVP_PKEY_CTX_set_rsa_padding(enc_ctx, RSA_PKCS1_OAEP_PADDING) <= 0) {
        handle_errors();
    }
    // Determine the size of the output
    size_t encrypted_key_len;
    if (EVP_PKEY_encrypt(enc_ctx, NULL, &encrypted_key_len, key, strlen(key)) <= 0) {
        handle_errors();
    }
    unsigned char encrypted_key[encrypted_key_len];
    if (EVP_PKEY_encrypt(enc_ctx, encrypted_key, &encrypted_key_len, key, strlen(key)) <= 0) {
        handle_errors();
    }

// Now I encrypt the IV used in the symm encryption with the Bob's public key
    EVP_PKEY *pkB;
    EVP_PKEY_CTX* enc_ctx = EVP_PKEY_CTX_new(pkB, NULL);
    if (EVP_PKEY_encrypt_init(enc_ctx) <= 0) {
        handle_errors();
    }
    // Specific configurations can be performed through the initialized context
    if (EVP_PKEY_CTX_set_rsa_padding(enc_ctx, RSA_PKCS1_OAEP_PADDING) <= 0) {
        handle_errors();
    }
    // Determine the size of the output
    size_t encrypted_iv_len;
    if (EVP_PKEY_encrypt(enc_ctx, NULL, &encrypted_iv_len, iv, strlen(iv)) <= 0) {
        handle_errors();
    }
    unsigned char encrypted_iv[encrypted_iv_len];
    if (EVP_PKEY_encrypt(enc_ctx, encrypted_iv, &encrypted_iv_len, iv, strlen(iv)) <= 0) {
        handle_errors();
    }

    send_bob(f_out);
    send_bob(encrypted_key);
    send_bob(encrypted_iv);

    RSA_free(pkB);
    EVP_CIPHER_CTX_free(ctx);

    fclose(f_in);
    fclose(f_out);

    // completely free all the cipher data
    CRYPTO_cleanup_all_ex_data();
    /* Remove error strings */
    ERR_free_strings();
    

    return 0;

}