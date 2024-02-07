#include <stdint.h>
#include <sys/types.h>

#define DELTA 0x9e3779b9
#define MX (((z>>5^y<<2) + (y>>3^z<<4)) ^ ((sum^y) + (k[p&3^e]^z)))

uint32_t btea(uint32_t* v, ssize_t n, uint32_t* k) {
uint32_t z, y, sum, e, q;
ssize_t p;
if (n > 1) {          /* Coding Part */
    q = 6 + 52/n;
    sum = 0;
    z = v[n-1];
    for (; q > 0; --q) {
    sum += DELTA;
    e = (sum >> 2) & 3;
    for (p=0; p<n-1; p++) {
        y = v[p+1];
        z = v[p] += MX;
    }
    y = v[0];
    z = v[n-1] += MX;
    }
    return 0 ; 
} else if (n < -1) {  /* Decoding Part */
    n = -n;
    q = 6 + 52/n;
    sum = q*DELTA ;
    y = v[0];
    for (; q > 0; --q) {
    e = (sum >> 2) & 3;
    for (p=n-1; p>0; p--) {
        z = v[p-1];
        y = v[p] -= MX;
    }
    z = v[n-1];
    y = v[0] -= MX;
    sum -= DELTA;
    }
    return 0;
}
return 1;
}