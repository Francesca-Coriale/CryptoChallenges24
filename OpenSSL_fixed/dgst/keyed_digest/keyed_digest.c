#include <stdio.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include <string.h>

#define MAXBUF 1024

void handle_errors(){
    ERR_print_errors_fp(stderr);
    abort();
}


int main(int argc, char **argv){

    unsigned char secret[] = "this_is_my_secret";
    unsigned int secret_len = strlen(secret);

    if(argc != 2){
        fprintf(stderr,"Invalid parameters. Usage: %s filename\n",argv[0]);
        exit(1);
    }

    FILE *f_in;
    if((f_in = fopen(argv[1],"r")) == NULL) {
            fprintf(stderr,"Couldn't open the input file, try again\n");
            exit(1);
    }

    /* Load the human readable error strings for libcrypto */
    ERR_load_crypto_strings();// deprecated since version 1.1.0
    /* Load all digest and cipher algorithms */
    OpenSSL_add_all_algorithms();// deprecated since version 1.1.0

    //EVP_MD_CTX *EVP_MD_CTX_new(void);
    //pedantic mode? Check if md == NULL
    EVP_MD_CTX *md = EVP_MD_CTX_new();

    //int EVP_DigestInit(EVP_MD_CTX *ctx, const EVP_MD *type);
    // int EVP_DigestInit_ex(EVP_MD_CTX *ctx, const EVP_MD *type, ENGINE *impl);
    // Returns 1 for success and 0 for failure.
    if(!EVP_DigestInit(md, EVP_sha512()))
        handle_errors();


    EVP_DigestUpdate(md, secret,secret_len);

    int n_read;
    unsigned char buffer[MAXBUF];
    while((n_read = fread(buffer,1,MAXBUF,f_in)) > 0){
    // Returns 1 for success and 0 for failure.
        if(!EVP_DigestUpdate(md, buffer, n_read))
            handle_errors();
    }

    EVP_DigestUpdate(md, secret,secret_len);

    unsigned char md_value[EVP_MD_size(EVP_sha512())];
    int md_len;

    //int EVP_DigestFinal_ex(EVP_MD_CTX *ctx, unsigned char *md, unsigned int *s);
    if(!EVP_DigestFinal_ex(md, md_value, &md_len))
        handle_errors();

    // void EVP_MD_CTX_free(EVP_MD_CTX *ctx);
    EVP_MD_CTX_free(md);

    printf("The digest is: ");
    for(int i = 0; i < md_len; i++)
                printf("%02x", md_value[i]);
    printf("\n");

    // completely free all the cipher data
    CRYPTO_cleanup_all_ex_data();// deprecated since version 1.1.0
    /* Remove error strings */
    ERR_free_strings();// deprecated since version 1.1.0


	return 0;

}