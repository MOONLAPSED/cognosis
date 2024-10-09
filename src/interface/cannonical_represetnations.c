#include <stdio.h>

// Homoiconic 'operators' and primitive (non-python) types

int main() {
  unsigned char a = 0x53; // 0101 0011 in binary
  unsigned char b = 0xA6; // 1010 0110 in binary
  
  // bitwise AND
  unsigned char c = a & b; // 0000 0010 in binary
  printf("a & b = 0x%x\n", c); // output: a & b = 0x2
  
  // bitwise OR
  unsigned char d = a | b; // 1111 0111 in binary
  printf("a | b = 0x%x\n", d); // output: a | b = 0xf7
  
  // bitwise XOR
  unsigned char e = a ^ b; // 1111 0101 in binary
  printf("a ^ b = 0x%x\n", e); // output: a ^ b = 0xf5
  
  // bitwise complement
  unsigned char f = ~a; // 1010 1100 in binary
  printf("~a = 0x%x\n", f); // output: ~a = 0xac
  
  // left shift
  unsigned char g = a << 2; // 0101 1100 in binary
  printf("a << 2 = 0x%x\n", g); // output: a << 2 = 0x5c
  
  // right shift
  unsigned char h = b >> 3; // 0001 0100 in binary
  printf("b >> 3 = 0x%x\n", h); // output: b >> 3 = 0x14
  
  return 0;
}
/*
In this program, we have two variables a and b, each with a value assigned in hexadecimal. We use various bitwise operators to perform operations on these variables.

The & operator performs a bitwise AND operation between a and b.
The | operator performs a bitwise OR operation between a and b.
The ^ operator performs a bitwise XOR operation between a and b.
The ~ operator performs a bitwise complement operation on a.
The << operator performs a left shift operation on a by 2 bits.
The >> operator performs a right shift operation on b by 3 bits.
Each operation is assigned to a new variable, which we then print out using printf with the %x format specifier to print the result in hexadecimal.
*/
