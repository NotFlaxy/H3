import sys
import logging
import paramiko
import json
from getpass import getpass

# Inlæser config filen.
with open('.\\HardwareInfo\\config.json', 'r') as config_file:
    config = json.load(config_file)

def Main():
    try:
        local_script = "HardwareInfo\\InfoGather.py"
        remote_script = "C:\\TMP\\Hwinfo.py"  
        ip_address = input("Server-IP: ")
        if ip_address == "":
            ip_address = config["SSH"]["ip-address"]
        username = input("Username: ")
        if username == "":
            username = config["SSH"]["username"]
        password = getpass("Password: ")
        if password == "":
            password = config["SSH"]["password"]
        SSH(local_script, remote_script, ip_address, username, password)
    except Exception as e:
        print(f"An unexpected error has occured {e}")

# Initialize SSH Connection and transfer + execute script.
def SSH(local_script, remote_script, ip_address, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(ip_address, 22, username=username, password=password)
    except paramiko.AuthenticationException:
        print("Error: Authentication failed. Please check your username/password.")
        return
    except paramiko.SSHException as e:
        print(f"SSH connection error {e}")
        return
    except Exception as e:
        print(f"An error occurred during connection: {e}")
        return
    
    try:
        # Transfer the script to the server.
        sftp = ssh.open_sftp()
        try:
            sftp.put(local_script, remote_script)
        except FileNotFoundError:
            print(f"Error: Local script {local_script} not found.")
            return
        except IOError as e:
            print(f"Error during file transfer: {e}")
            return
        finally:
            sftp.close()

        # Fetch the hostname of the remote machine and save to variable.
        stdin, stdout, stderr = ssh.exec_command("hostname")
        hostName = stdout.read().decode().strip()
        LOG_FILE = f".\\HardwareInfo\\{hostName}.txt"

        # Execute the remote script.
        stdin, stdout, stderr = ssh.exec_command(f"py {remote_script}")
        
        # Output of the execution and Error output.
        try:
            LOG = open(LOG_FILE, "w", newline="")
            generalOutput = stdout.read().decode().strip()
            if generalOutput:
                LOG.write(generalOutput)
                LOG.close()
            errorOutput = stderr.read().decode().strip()
            if errorOutput:
                print("\nError Output:" + errorOutput + "\n")
        except Exception as e:
            print(f"Error while reading script output: {e}")

        # Remove the remote script (Clean up).
        ssh.exec_command(f"del {remote_script}")
    except Exception as e:
        print(f"An error occured during the removal of {remote_script}: {e}")
    finally:
        ssh.close()

def getHelp():
    arg = sys.argv[1].lower()
    if arg == '-help' or arg == '-h':
        print('Hello this is the help function of my script.')
    else:
        print('This is not a vlid argument. Use -help or -h')

# Exectuion af functions of implementering af help function.
length = len(sys.argv)
if length == 1:
    Main()
    print("The script has reached the end")
else:
    getHelp()