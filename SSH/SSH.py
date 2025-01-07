import json
import paramiko

# Inlæser config filen.
with open('.\ssh\config.json', 'r') as config_file:
    config = json.load(config_file)

# Initializer og indlæs values.
def Main():
    local_script = input("Navn på skript du vil execute: ")
    if local_script == "":
        local_script = config["DefaultScript"]
        remote_script = "C:\\TMP\\script.py"
    else:
        local_script = ".\\SSH\\" + local_script
        remote_script = "C:\\TMP\\" + local_script
    ip_address = input("Server-IP: ")
    if ip_address == "":
        ip_address = config["SSH"]["ip-address"]
    username = input("Username: ")
    if username == "":
        username = config["SSH"]["username"]
    password = input("Password: ")
    if password == "":
        password = config["SSH"]["password"]
    SSH(local_script, remote_script, ip_address, username, password)

def SSH(local_script, remote_script, ip_address, username, password):
    # Initialize SSH Connection.
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip_address, 22, username=username, password=password)

    # Transfer the script to the server.
    sftp = ssh.open_sftp()
    sftp.put(local_script, remote_script)
    sftp.close()

    # Execute the remote script.
    stdin, stdout, stderr = ssh.exec_command(f"py {remote_script}")

    generalOutput = stdout.read().decode().strip()
    if generalOutput:
        print("\nOutput:\n" + generalOutput + "\n")
    errorOutput = stderr.read().decode().strip()
    if errorOutput:
        print("\nError Output:" + errorOutput + "\n")

    # Remove the remote script (Clean up).
    stdin, stdout, stderr = ssh.exec_command(f"del {remote_script}")

    ssh.close()

Main()
print("The script has reached the end")