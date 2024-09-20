// key = "0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF"
// IV = "11111111111111112222222222222222";
// msg_B64 = "jyS3NIBqen2CWpDI2jkSu+z93NkDbWkUMitg2Q==";
// we need to decode msg_B64:
// 1. echo "jyS3NIBqen2CWpDI2jkSu+z93NkDbWkUMitg2Q==" > encoded.txt
// 2. openssl base64 -d -in encoded.txt -out file.enc


//to give the imput parameters:
// gcc first_dec.c -o first_dec.exe -lssl -lcrypto
// ./first_dec.exe inputfile key IV outputfile


//from code.c
/**************************************************/
#include <stdio.h>
#include <string.h>

#include <openssl/evp.h>
#include <openssl/err.h>


#define ENCRYPT 1
#define DECRYPT 0
#define MAX_BUFFER 1024

void handle_errors(){
    ERR_print_errors_fp(stderr);
    abort();
}

int main(int argc, char **argv)
{
//  int EVP_CipherInit(EVP_CIPHER_CTX *ctx, const EVP_CIPHER *type, const unsigned char *key, const unsigned char *iv, int enc);
//  int EVP_CipherUpdate(EVP_CIPHER_CTX *ctx, unsigned char *out, int *outl, const unsigned char *in, int inl);
//  int EVP_CipherFinal(EVP_CIPHER_CTX *ctx, unsigned char *outm, int *outl);
    if(argc != 5){
        fprintf(stderr,"Invalid parameters. Usage: %s file_in key iv file_out\n",argv[0]);
        exit(1);
    }

    FILE *f_in;
    if((f_in = fopen(argv[1],"r")) == NULL) {
            fprintf(stderr,"Couldn't open the input file, try again\n");
            abort();
    }
 
    if(strlen(argv[2])!=64){
        fprintf(stderr,"Wrong key length\n");
        abort();
    }   
    if(strlen(argv[3])!=32){
        fprintf(stderr,"Wrong IV length\n");
        abort();
    }
    
    FILE *f_out;
    if((f_out = fopen(argv[4],"wb")) == NULL) {
            fprintf(stderr,"Couldn't open the output file, try again\n");
            abort();
    }

    unsigned char key[strlen(argv[2])/2];
    for(int i = 0; i < strlen(argv[2])/2;i++){
        sscanf(&argv[2][2*i],"%2hhx", &key[i]);
    }

    unsigned char iv[strlen(argv[3])/2];
    for(int i = 0; i < strlen(argv[3])/2;i++){
        sscanf(&argv[3][2*i],"%2hhx", &iv[i]);
    }

/*************************************************************/
//from code.c + dec1.c

    /* Load the human readable error strings for libcrypto */
    ERR_load_crypto_strings();
    /* Load all digest and cipher algorithms */
    OpenSSL_add_all_algorithms();

    // pedantic mode: check NULL
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();

    if(!EVP_CipherInit(ctx,EVP_chacha20(), key, iv, DECRYPT))
        handle_errors();

    int update_len, final_len;
    int decrypted_len=0;

    int n_read;
    unsigned char buffer[MAX_BUFFER];

    unsigned char plaintext[MAX_BUFFER+16];

    while((n_read = fread(buffer,1,MAX_BUFFER,f_in)) > 0){
        printf("n_Read=%d-",n_read);
/////////////// from dec1.c ///////////////////////////////
        if(!EVP_CipherUpdate(ctx,plaintext,&update_len,buffer,n_read))
            handle_errors();
        decrypted_len+=update_len;
        printf("update size: %d\n",decrypted_len);

        EVP_CipherFinal_ex(ctx,plaintext+decrypted_len,&final_len);
        decrypted_len+=final_len;
////////////////// end ////////////////////////////////////
        if(fwrite(plaintext, 1, decrypted_len, f_out) < decrypted_len){
            fprintf(stderr,"Error writing the output file\n");
            abort();
        }
    }

    EVP_CIPHER_CTX_free(ctx);

    fclose(f_in);
    fclose(f_out);

    printf("File decrypted!\n");

    // completely free all the cipher data
    CRYPTO_cleanup_all_ex_data();
    /* Remove error strings */
    ERR_free_strings();

    return 0;
}
