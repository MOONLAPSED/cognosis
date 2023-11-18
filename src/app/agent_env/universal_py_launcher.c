#include <python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
#include <windows.h>
#define PATH_SEPARATOR '\\'
#else
#include <unistd.h>
#define PATH_SEPARATOR '/'
#endif

#define MAX_PATH 1024

#ifdef _WIN32
#define TRUSTED_DIR "C:\\cognic\\"
#else
#define TRUSTED_DIR "/cognic/"
#endif

char *strreplace(char *orig, char *rep, char *with)
{
  char *result;  // the return string
  char *ins;     // the next insert point
  char *tmp;     // varies
  int len_rep;   // length of rep (the string to remove)
  int len_with;  // length of with (the string to replace rep with)
  int len_front; // distance between rep and end of last rep
  int count;     // number of replacements

  // sanity checks and initialization
  if (!orig || !rep)
    return NULL;
  len_rep = strlen(rep);
  if (len_rep == 0)
    return NULL; // empty rep causes infinite loop during count
  if (!with)
    with = "";
  len_with = strlen(with);

  // count the number of replacements needed
  ins = orig;
  for (count = 0; tmp = strstr(ins, rep); ++count)
  {
    ins = tmp + len_rep;
  }

  tmp = result = malloc(strlen(orig) + (len_with - len_rep) * count + 1);

  if (!result)
    return NULL;

  // first time through the loop, all the variable are set correctly
  // from here on,
  //    tmp points to the end of the result string
  //    ins points to the next occurrence of rep in orig
  //    orig points to the remainder of orig after "end of rep"
  while (count--)
  {
    ins = strstr(orig, rep);
    len_front = ins - orig;
    tmp = strncpy(tmp, orig, len_front) + len_front;
    tmp = strcpy(tmp, with) + len_with;
    orig += len_front + len_rep; // move to next "end of rep"
  }
  strcpy(tmp, orig);
  return result;
}

int is_python_file(const char *filename)
{
  size_t len = strlen(filename);
  return (len >= 3 && strcmp(filename + len - 3, ".py") == 0);
}

int run_script(const char *filename)
{
  FILE *fp = fopen(filename, "r");
  if (!fp)
  {
    fprintf(stderr, "Error: cannot open %s\n", filename);
    return 1;
  }

  fseek(fp, 0, SEEK_END);
  int size = ftell(fp);
  fseek(fp, 0, SEEK_SET);

  char *buf = (char *)malloc(size + 1);
  if (!buf)
  {
    fprintf(stderr, "Error: cannot allocate memory\n");
    fclose(fp);
    return 1;
  }

  fread(buf, 1, size, fp);
  buf[size] = '\0';
  fclose(fp);

  Py_Initialize();
  int err = PyRun_SimpleString(buf);
  Py_Finalize();

  free(buf);

  if (err == -1)
  {
    fprintf(stderr, "Error: cannot run the Python script\n");
    return 1;
  }

  return 0;
}

int main(int argc, char *argv[])
{
  if (argc < 2 || !argv[1])
  {
    fprintf(stderr, "Usage: ploader <python file>\n");
    return 1;
  }

  size_t len = strlen(argv[1]);
  if (len > MAX_PATH)
  {
    fprintf(stderr, "Filename too long\n");
    return 1;
  }

  char fullFilePath[MAX_PATH];
#ifdef _WIN32
  strcpy(fullFilePath, TRUSTED_DIR);
  strcat(fullFilePath, argv[1]);
#else
  snprintf(fullFilePath, sizeof(fullFilePath), "%s%s", TRUSTED_DIR, argv[1]);
#endif
  if (access(fullFilePath, F_OK) == -1)
  {
    fprintf(stderr, "Error: File does not exist or is not accessible\n");
    return 1;
  }

  int rc = run_script(fullFilePath);

  return rc;
}
