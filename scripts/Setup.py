import sys
import os
import subprocess

print("Setting up environment...")

# Exit scripts directory
os.chdir("../")
BASE_DIR = os.getcwd()
ENV_NAME = "OceanBot_env"

print(f"Creating virutal environment: {ENV_NAME}")
subprocess.call(["python","-m","venv",str(ENV_NAME)])

print("Activating virtual env and installing modules...")
ENV_INTERPRETER = [f"{BASE_DIR}\{ENV_NAME}\Scripts\python.exe"]
subprocess.call(ENV_INTERPRETER + ["-m","pip","install","--upgrade","pip"])
subprocess.call(ENV_INTERPRETER + ["-m","pip","install","-r","requirements.txt"])