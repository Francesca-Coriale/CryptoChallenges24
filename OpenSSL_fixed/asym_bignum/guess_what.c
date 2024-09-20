#include <stdio.h>
#include <openssl/bn.h>
#include <string.h> //to use sizeof()

void remove_colons(char *src, char *dest) {
    while (*src) {
        if (*src != ':') {
            *dest = *src;
            dest++;
        }
        src++;
    }
    *dest = '\0'; // Null-terminate the destination string
}

int main ()
{
    char string1[] = "00:9e:ee:82:dc:2c:d4:a0:0c:4f:5a:7b:86:63:b0:c1:ed:06:77:fc:eb:de:1a:23:5d:f4:c3:ff:87:6a:7d:ad:c6:07:fa:a8:35:f6:ae:05:03:57:3e:22:36:76:d5:0d:57:4f:99:f9:58:ad:63:7a:e7:45:a6:aa:fa:02:34:23:b6:9d:34:15:7b:11:41:b6:b1:ca:b9:1a:cd:29:55:bd:42:f5:04:ab:df:45:4a:9d:4e:ca:4e:01:f9:f8:74:59:67:ee:b6:a9:fb:96:b7:c0:94:00:17:8a:53:0e:b6:d8:31:c9:68:e6:64:38:d3:63:3a:04:d7:88:6b:f0:e1:ad:60:7f:41:bd:85:7b:d9:04:e1:97:5b:1f:9b:05:ce:ac:2c:c4:55:3f:b4:8b:89:4d:0a:50:9a:09:4e:5e:8f:5b:5f:55:69:72:5f:04:9b:3a:8a:09:b4:7f:8d:b2:ca:52:0e:5e:bf:f4:b0:ee:c9:ba:dc:93:4f:6d:d3:1f:82:1a:d9:fc:2c:a7:3f:18:23:0d:d7:44:c7:28:54:67:84:ee:73:92:65:f0:1c:e8:1e:6d:4d:95:65:b4:c8:4f:b8:04:62:58:2b:ee:32:64:a0:a7:dc:99:25:0e:50:53:76:bc:30:db:71:5e:93:d6:9f:1f:88:1c:76:5d:82:c8:59:39:51";
    char string2[] = "00:d2:c6:01:32:6b:4c:4b:85:5f:52:7b:b7:8e:d6:8a:e4:c8:76:7e:6b:c9:24:9a:3e:ca:cd:2f:c9:b8:75:d4:f9:71:11:e1:cf:be:62:d3:2c:5f:f9:fd:9b:fa:ed:62:f3:df:44:c7:57:fb:ee:9b:b2:32:cb:54:49:29:6c:69:2e:30:1d:8c:1f:fa:b1:8e:e4:49:66:c1:fb:92:7c:82:ca:60:c9:40:a4:0a:b2:db:50:ec:f6:ff:98:a7:16:23:38:8d:06:d2:7c:a9:85:8a:c2:2b:4d:d4:e6:f1:89:e5:b0:42:54:a0:5f:3c:dd:c7:64:33:05:11:fb:ee:8b:26:07";
    unsigned int len1 = sizeof(string1)/sizeof(string1[0]);
    unsigned int len2 = sizeof(string2)/sizeof(string2[0]);

    char hex1[len1];
    char hex2[len2];
    remove_colons(string1, hex1);
    remove_colons(string2, hex2);


    BIGNUM *big_number1 = BN_new();
    BIGNUM *big_number2 = BN_new();
    //creeate from hexadecimal strings
    BN_hex2bn(&big_number1, hex1);
    BN_hex2bn(&big_number2, hex2);

    BN_print_fp(stdout,big_number1);
    printf("\n");
    BN_print_fp(stdout,big_number2);
    printf("\n");

    BN_CTX *ctx = BN_CTX_new();
    BIGNUM *div = BN_new();
    BIGNUM *res = BN_new();

    printf("Big_number1 is prime? %d\n", BN_is_prime_ex(big_number1, 64, ctx, NULL));
    printf("Big_number2 is prime? %d\n", BN_is_prime_ex(big_number2, 64, ctx, NULL));

    BN_gcd(res, big_number1, big_number2, ctx);
    printf("Max Comune Divisore: \n");
    BN_print_fp(stdout,res);
    printf("\n");

    //BN_mod(res,big_number1,big_number2,ctx); //res = big_number1 (mod big_number2)
    // print in hex format
    //printf("modulo: \n");
    //BN_print_fp(stdout,res);
    //printf("\n");

    BN_div(div,res,big_number1,big_number2,ctx);
    //printf("div=%lu, res=%lu \n",BN_get_word(div),BN_get_word(res));
    printf("divisione: \n");
    BN_print_fp(stdout, div);
    printf("\n");
    printf("resto: \n");
    BN_print_fp(stdout, res);
    printf("\n");

    //BIGNUM *bigmult = BN_new();
    //BN_hex2bn(&bigmult, mult);
    //BN_mul(res,big_number2,bigmult, ctx);
    //printf("moltiplicazione:\n");
    //BN_print_fp(stdout, res);
    //printf("\n");
    //int compare = BN_cmp(res, big_number1);
    //printf("compare:%d\n", compare);
    //printf("\n");

    BN_free(big_number1);
    BN_free(big_number2);
    BN_free(div);
    BN_free(res);

    BN_CTX_free(ctx);

    return 0;
}
