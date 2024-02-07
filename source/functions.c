#include <stdio.h>
#include <string.h>

void name(char first[], char last[]) {
    char full[50];
    char space[] = " ";
    strcpy(full, first);
    strcat(full, space);
    strcat(full, last);
    printf("%s\n", full);
}

int sum(int k) {
    if (k > 0) {
        return k + sum(k - 1);
    } else {
        return 0;
    }
}

void countdown(int k) {
    while (k > 0) {
        k--;
    }
}

void forloop(int k) {
    for (; k > 0; k--) {
        printf("%d\n", k);
    }
}

int main() {
    // function call with args
    char john[] = "John", smith[] = "Smith", julie[] = "Julie", nelson[] = "Nelson";
    name(john, smith);
    name(julie, nelson);

    // recursive functions
    int sum12 = sum(12);
    printf("%d\n", sum12);

    // while loop
    countdown(10);

    // for loop
    forloop(10);

    return 0;
}