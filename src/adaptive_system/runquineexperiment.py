import subprocess
import os
import argparse

def run_quine(n):
    quine_files = []
    current_file = "quine.py"
    
    for i in range(n):
        output_file = f"equine{i+1}.py"
        quine_files.append(output_file)
        
        # Run the current quine and save its output
        with open(output_file, 'w') as f:
            subprocess.run(["python", current_file], stdout=f, text=True)
        
        current_file = output_file
    
    return quine_files

def main():
    parser = argparse.ArgumentParser(description="Generate and compare multiple quine iterations.")
    parser.add_argument('n', type=int, help='Number of quine iterations to generate')
    args = parser.parse_args()

    # Generate quine files
    quine_files = run_quine(args.n)
    
    # Compare the generated files
    compare_command = ["python", "quinecompare.py"] + quine_files
    subprocess.run(compare_command)

if __name__ == "__main__":
    main()