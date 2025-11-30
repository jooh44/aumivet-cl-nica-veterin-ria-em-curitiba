import paramiko
import sys

HOST = "46.202.147.75"
USER = "root"
PASSWORD = ",1E1FD2Y&'V2Rp,5o25p"

command = " ".join(sys.argv[1:]) or "hostname"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, username=USER, password=PASSWORD, look_for_keys=False, allow_agent=False, timeout=900)
try:
    stdin, stdout, stderr = client.exec_command(command)
    out = stdout.read()
    err = stderr.read()
    if out:
        sys.stdout.buffer.write(out)
    if err:
        sys.stderr.buffer.write(err)
finally:
    client.close()