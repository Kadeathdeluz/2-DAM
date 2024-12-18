# This library let us create, manipulate and control processes
import subprocess

# Start with a try block to ensure that the program doesn't crashes
try:
    # Runs the calc
    subprocess.run(["calc.exe"])
except Exception as e:
    print("An error ocurr trying to open the calc: ", str(e))