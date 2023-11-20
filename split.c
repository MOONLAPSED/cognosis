#include <python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#define BLOB_BUFFER_SIZE 1024

/* input_stream = ...<im_start>BLOB<im_end><im_start>BLOB<im_end>...
 * BLOB is binary encoded data pull from a SQL table
 * inblb[0] --> <im_start>\n
 * inblb[1] --> BLOB\n
 * inblb[2] --> <im_end>\n
 * inblb[3] --> <im_start>\n
 * ...
 * Returns 0 on success, non-zero on failure. Saves a file to /logs/ upon success containing split input_stream
 * */

int main(int argc){

}
