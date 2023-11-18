#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#define COMMAND_BUFFER_SIZE 256

/*
 * Executes a file in the current directory if it has a .out extension.
 *
 * Uses snprintf() to build a command that prepends "./" to the filename,
 * then passes the command to system() to execute.
 *
 * Returns 0 on success, non-zero on failure.
 */

int main()
{

  const char *dir = ".";

  // Extract extension
  char *ext = strrchr(dir, '.');

  if (ext != NULL && strcmp(ext, ".out") == 0)
  {

    // Build command
    char command[COMMAND_BUFFER_SIZE];
    snprintf(command, sizeof(command), "./%%s\n", dir);

    // Execute command
    if (system(command) == -1)
    {
      perror("system");
      exit(EXIT_FAILURE);
    }
  }

  return 0;
}