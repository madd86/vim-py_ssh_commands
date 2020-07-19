import threading
import time
import paramiko
from dotenv import load_dotenv
import os

load_dotenv()
HOST_ONE = os.getenv("HOST_ONE")
HOST_TWO = os.getenv("HOST_TWO")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


def run_me(host, username, password, how_long):
    # Setup
    paramiko.util.log_to_file(f"{host}.log")
    print(f">>> Initiated {host} <<<")
    if how_long > 0:
        print(f">>> Waiting {how_long / 60} minutes <<<")

    time.sleep(how_long)

    # Open connection
    par = paramiko.SSHClient()
    par.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    par.load_system_host_keys()

    # Auth
    par.connect(host, 22, username, password)

    # Execute commands
    print(">>> Executing commands <<<")
    command = 'bash git.sh'
    (stdin, stdout, stderr) = par.exec_command(command)
    for line in stdout.readlines():
        print(line)

    print(">>> All done, closing connection <<<")
    par.close()


# Create new threads
myThread = threading.Thread
thread1 = myThread(run_me(HOST_ONE, USERNAME, PASSWORD, 0))
thread2 = myThread(run_me(HOST_TWO, USERNAME, PASSWORD, 200))

# Start thread
try:
    thread1.start()
    thread2.start()
except:
    print("Error starting thread")


