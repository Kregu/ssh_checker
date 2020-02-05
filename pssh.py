import paramiko
from datetime import datetime
from time import sleep

host = '192.168.1.1'
user = 'admin'
secret = '13425'
port = 22
commands = ['ls', 'show sys']
encoding = 'utf-8'

while True:

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=port)

    data = bytes()
    for command in commands:
        stdin, stdout, stderr = client.exec_command(command)
        data += stdout.read() + stderr.read()
        sleep(0.1)
             
    client.close()

    
    with open('data.txt', 'a') as file_data:
        file_data.write(str(datetime.today().strftime("%Y-%m-%d %H:%M:%S") + '\n'))
        file_data.write(data.decode(encoding) + '\n')


    sleep(5)


