import json
import paramiko

# Inlæser config filen.
with open('.\ssh\config.json', 'r') as config_file:
    config = json.load(config_file)

# Initializer og indlæs values.
def Main():
    try:
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
    except Exception as e:
        print(f"An unexpected error has occured {e}")

def SSH(local_script, remote_script, ip_address, username, password):
    # Initialize SSH Connection.
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

        # Execute the remote script.
        stdin, stdout, stderr = ssh.exec_command(f"py {remote_script}")
        
        try:
            # Output of the execution and Error output.
            generalOutput = stdout.read().decode().strip()
            if generalOutput:
                print("\nOutput:\n" + generalOutput + "\n")
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

Main()
print("The script has reached the end")