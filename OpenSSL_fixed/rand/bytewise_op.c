#include <stdlib.h>
#include <string.h>
#include <stdio.h>

void byteWiseOR(const char rand1[], const char rand2[], char result[], int size) {
    for (int i = 0; i < size; i++) {
        result[i] = rand1[i] | rand2[i];
    }
}

void byteWiseAND(const char rand1[], const char rand2[], char result[], int size) {
    for (int i = 0; i < size; i++) {
        result[i] = rand1[i] & rand2[i];
    }
}

void byteWiseXOR(const char rand1[], const char rand2[], char result[], int size) {
    for (int i = 0; i < size; i++) {
        result[i] = rand1[i] ^ rand2[i];
    }
}

int main() {
    // '\x' per avere esadecimali
    char rand1[] = {'\x63', '\x3b', '\x6d', '\x07', '\x65', '\x1a', '\x09', '\x31', '\x7a', '\x4f', '\xb4', '\xaa', '\xef', '\x3f', '\x7a', '\x55', '\xd0', '\x33', '\x93', '\x52', '\x1e', '\x81', '\xfb', '\x63', '\x11', '\x26', '\xed', '\x9e', '\x8e', '\xa7', '\x10', '\xf6', '\x63', '\x9d', '\xeb', '\x92', '\x90', '\xeb', '\x76', '\x0b', '\x90', '\x5a', '\xeb', '\xb4', '\x75', '\xd3', '\xa1', '\xcf', '\xd2', '\x91', '\x39', '\xc1', '\x89', '\x32', '\x84', '\x22', '\x12', '\x4e', '\x77', '\x57', '\x4d', '\x25', '\x85', '\x98'};
    char rand2[] = {'\x92', '\x05', '\xd8', '\xb5', '\xfa', '\x85', '\x97', '\xb6', '\x22', '\xf4', '\xbd', '\x26', '\x11', '\xcf', '\x79', '\x8c', '\xdb', '\x4a', '\x28', '\x27', '\xbb', '\xd3', '\x31', '\x56', '\x74', '\x16', '\xdf', '\xcb', '\xf5', '\x61', '\xa7', '\x9d', '\x18', '\xc2', '\x63', '\x92', '\xf1', '\xcb', '\xc3', '\x6d', '\x2b', '\x77', '\x19', '\xaa', '\x21', '\x07', '\x8e', '\xfe', '\x8b', '\x1a', '\x4f', '\x7d', '\x70', '\x6e', '\xa4', '\x7b', '\xc8', '\x68', '\x30', '\x43', '\x12', '\x50', '\x30', '\x1e'};

    int size = sizeof(rand1) / sizeof(rand1[0]);

    char k1[size];
    char k2[size];
    char key[size];

    byteWiseOR(rand1, rand2, k1, size);
    byteWiseAND(rand1, rand2, k2, size);
    byteWiseXOR(k1, k2, key, size);

    printf("Risultato dell'operazione OR:\n");
    for (int i = 0; i < size; i++) {
        printf("%02x-", (unsigned char)k1[i]);
    }
    printf("\n");

    printf("Risultato dell'operazione AND:\n");
    for (int i = 0; i < size; i++) {
        printf("%02x-", (unsigned char)k2[i]);
    }
    printf("\n");

    printf("Risultato dell'operazione XOR:\n");
    for (int i = 0; i < size; i++) {
        printf("%02x-", (unsigned char)key[i]);
    }
    printf("\n");

    return 0;
}
