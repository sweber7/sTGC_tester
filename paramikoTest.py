import paramiko, base64
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('stgcpi', username='pi', password='raspberry')
stdin, stdout, stderr = client.exec_command('ls')
for line in stdout:
    print ('... ' + line.strip('\n'))
client.close()


