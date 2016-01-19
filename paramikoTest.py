import paramiko

def sendPi(command):
    stdin, stdout, stderr = client.exec_command(command)
    for line in stdout:
        print ('... ' + line.strip('\n'))

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('stgcpi', username='pi', password='raspberry')

sendPi('sudo python /home/pi/multiplexControl/setPins.py 1 4')


client.close()


