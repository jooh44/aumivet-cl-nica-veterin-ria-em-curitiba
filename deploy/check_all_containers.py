import paramiko
import os

# Configuration
HOST = "46.202.147.75"
USER = "root"
password = ",1E1FD2Y&'V2Rp,5o25p"

print(f"Connecting to {HOST}...")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(HOST, username=USER, password=password)
    print("Connected successfully!")
    
    print("\n--- All Running Containers ---")
    stdin, stdout, stderr = client.exec_command("docker ps --format '{{.ID}} {{.Image}} {{.Names}} {{.Ports}}'")
    print(stdout.read().decode())

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client.close()
