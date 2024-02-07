# Rev
A bunch homemade compiled code and C source code for rev practice

### Compiling

When compiling a C or C++ program for a Rev or PWN challenge, you want to be able to control what gcc does to your file. Here are some example commands to help along the process of compiling

Basic compilation you just need an output file:
```C
gcc example.c -o outputfile
```

Useful flags:
```C
-no-pie : disable PIE
-fno-stack-protector : disable SSP, or the Stack Canary and Stack Bounds checks
-z execstack : control elf settings, specifically make an executable stack
-m32 : compile in 32 bit
```