import os
import difflib
import argparse

def diff_files(*files):
    for i in range(len(files) - 1):
        with open(files[i], 'r') as f1, open(files[i + 1], 'r') as f2:
            file1_lines = f1.readlines()
            file2_lines = f2.readlines()
            
            differ = difflib.Differ()
            diff = list(differ.compare(file1_lines, file2_lines))
            
            print(f"\nDifferences between {os.path.basename(files[i])} and {os.path.basename(files[i + 1])}:")
            for line in diff:
                if line.startswith('- ') or line.startswith('+ ') or line.startswith('? '):
                    print(line)

def main():
    parser = argparse.ArgumentParser(description="Compare multiple quine files.")
    parser.add_argument('files', nargs='+', help='Files to compare')
    args = parser.parse_args()

    diff_files(*args.files)

if __name__ == "__main__":
    main()