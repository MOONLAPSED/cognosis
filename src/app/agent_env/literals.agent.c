#include <stdio.h>
#include <stdlib.h>

int main()
{
  // Part 1: Array Manipulation using Pointers and Malloc
  double *A = (double *)malloc(4 * sizeof(double));

  if (A == NULL)
  {
    printf("Memory allocation failed.\n");
    return 1;
  }

  A[0] = 9.0;
  A[1] = 2.9;
  A[2] = 3.E+25;
  A[3] = 0.00007;

  printf("Array Manipulation using Pointers and Malloc:\n");
  for (size_t i = 0; i < 4; ++i)
  {
    printf("Element %zu is %g,\tits square is %g\n",
           i,
           A[i],
           A[i] * A[i]);
  }

  free(A); // Free allocated memory

  // Part 2: Bitwise Operations
  printf("\nBitwise Operations:\n");
  unsigned char a = 0x53; // 0101 0011 in binary
  unsigned char b = 0xA6; // 1010 0110 in binary

  // Bitwise AND
  unsigned char c = a & b;     // 0000 0010 in binary
  printf("a & b = 0x%x\n", c); // output: a & b = 0x2

  // Bitwise OR
  unsigned char d = a | b;     // 1111 0111 in binary
  printf("a | b = 0x%x\n", d); // output: a | b = 0xf7

  // Bitwise XOR
  unsigned char e = a ^ b;     // 1111 0101 in binary
  printf("a ^ b = 0x%x\n", e); // output: a ^ b = 0xf5

  // Bitwise complement
  unsigned char f = ~a;     // 1010 1100 in binary
  printf("~a = 0x%x\n", f); // output: ~a = 0xac

  // Left shift
  unsigned char g = a << 2;     // 0101 1100 in binary
  printf("a << 2 = 0x%x\n", g); // output: a << 2 = 0x5c

  // Right shift
  unsigned char h = b >> 3;     // 0001 0100 in binary
  printf("b >> 3 = 0x%x\n", h); // output: b >> 3 = 0x14// ... (Same bitwise operations as before)

  return 0;
}
// Print formatting (printf)

char a = 'C';     // single character    %c
char b[] = "bee"; // array of characters %s

float c = 3.141592;           // 4 bytes (32 bits of precision) 6 - 7 digits %f
double d = 3.141592653589793; // 8 bytes (64 bits of precision) 15 - 16 digits %lf

bool e = true; // 1 byte (true or false) %d

char f = 120;          // 1 byte (-128 to +127) %d or %c
unsigned char g = 255; // 1 byte (0 to +255) %d or %c

short h = 32767;          // 2 bytes (−32,768 to +32,767) %d
unsigned short i = 65535; // 2 bytes (0 to +65,535) %d

int j = 2147483647;          // 4 bytes (-2,147,483,648 to +2,147,483,647) %d
unsigned int k = 4294967295; // 4 bytes (0 to +4,294,967,295) %u

long long int l = 9223372036854775807;            // 8 bytes (-9 quintillion to +9 quintillion) %lld
unsigned long long int m = 18446744073709551615U; // 8 bytes (0 to +18 quintillion) %llu

printf("%c\n", a);   // char
printf("%s\n", b);   // character array
printf("%f\n", c);   // float
printf("%lf\n", d);  // double
printf("%d\n", e);   // bool
printf("%d\n", f);   // char as numeric value
printf("%d\n", g);   // unsigned char as numeric value
printf("%d\n", h);   // short
printf("%d\n", i);   // unsigned short
printf("%d\n", j);   // int
printf("%u\n", k);   // unsigned int
printf("%lld\n", l); // long long int
printf("%llu\n", m); // unsigned long long int