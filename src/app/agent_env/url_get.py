import commands
import requests

def download_file(url):
  """Downloads the contents of a URL to a file.

  Args:
    url: The URL to download the file from.

  Returns:
    The path to the downloaded file.
  """

  filename = url.split("/")[-1]
  with open(filename, "wb") as f:
    response = requests.get(url)
    f.write(response.content)

  return filename

def main():
  url = input("Enter the URL of the file to download: ")
  filename = download_file(url)
  print("The file was downloaded to {}.".format(filename))

if __name__ == "__main__":
  main()