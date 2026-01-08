"""
Pipeline runner for Novel Analyzer Project
PDF - Clean - Embed - Store in Vector DB
"""

import subprocess #used to run other python files from this file
import sys        #lets you know which python interpreter is running and helps exit the program safely if something fails

def run_step(script_name):                #Takes python files, runs them, checks if they succeed or fail
    print(f"\n Running {script_name}...") 
    result = subprocess.run(              
        [sys.executable, script_name],    #using the same python and selecting file to run
        capture_output=True,              #capture print statements and errors
        text=True                         #return output as strings
    )

    if result.returncode !=0:             #(0= success and not 0=failure)
        print(f"Error in {script_name}")  #prints the error, stops entire pipeline, prevents corrupted data from going forward
        print(result.stderr)
        sys.exit(1)

    else:
        print(result.stdout)              #Shows the output,confirms success, moves to the next step
        print(f"{script_name} completed successfully!")


def main():
    run_step("pdf_parser.py")
    run_step("preprocessor.py")
    run_step("embedder.py")
    run_step("vector_db.py")

    print("\n Pipeline completed successfully!")

if __name__ == "__main__":
    main()