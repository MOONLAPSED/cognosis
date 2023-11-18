#include <python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
strreplace("/", "\\", argv[1]);
#endif

#ifdef _WIN32
#define TRUSTED_DIR "C:\\cntnt\\"
#else
#define TRUSTED_DIR "/cntnt/"
#endif

int is_python_file(char *filename)
{
  int len = strlen(filename);
  if (len < 4)
    return 0;
  if (filename[len - 3] == '.' && filename[len - 2] == 'p' && filename[len - 1] == 'y')
    return 1;
  return 0;
}

if (argc < 2 || !argv[1])
{
  fprintf(stderr, "Missing filename\n");
  return 1;
}

size_t len = strlen(argv[1]);
if (len > MAX_PATH)
{
  fprintf(stderr, "Filename too long\n");
  return 1;
}

int main(int argc, char *argv[])
{
  char *buf;
  if (argc < 2)
  {
    fprintf(stderr, "Usage: ploader <python file>\n");
    return 1;
  }
  if (!is_python_file(argv[1]))
  {
    fprintf(stderr, "Error: %s is not a python file\n", argv[1]);
    return 1;
  }
  FILE *fp = fopen(argv[1], "r");
  if (!fp)
  {
    fprintf(stderr, "Error: cannot open %s\n", argv[1]);
    return 1;
  }

  fseek(fp, 0, SEEK_END);
  int size = ftell(fp);
  fseek(fp, 0, SEEK_SET);
  buf = (char *)malloc(size + 1);
  if (!buf)
  {
    fprintf(stderr, "Error: cannot allocate memory\n");
    fclose(fp);
    return 1;
  }
  fread(buf, 1, size, fp);
  buf[size] = 0;
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

int startswith(const char *str, const char *pre)
{
  size_t lenpre = strlen(pre), lenstr = strlen(str);
  return lenstr < lenpre ? 0 : memcmp(pre, str, lenpre) == 0;
}

int run_script(char *filename)
{

  FILE *fp = fopen(filename, "r");
  if (!fp)
  {
    return 1;
  }

  // Read file contents

  fclose(fp);

  // Run script

  return 0;
}

int main(int argc, char *argv[])
{

  if (argc < 2)
  {
    fprintf(stderr, "Missing filename\n");
    return 1;
  }

  size_t len = strlen(argv[1]);
  if (len > 255)
  {
    fprintf(stderr, "Filename too long\n");
    return 1;
  }

  if (!startswith(argv[1], TRUSTED_DIR))
  {
    fprintf(stderr, "Untrusted file\n");
    return 1;
  }

  int rc = run_script(argv[1]);

  return rc;
}