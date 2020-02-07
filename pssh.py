import paramiko
import requests
import settings

from datetime import datetime
from time import sleep

host = '192.168.1.1'
user = 'admin'
secret = settings.secret
port = 22
commands = ['show sys']
encoding = 'utf-8'

filepath = 'data.txt'
word_search = 'cpu'

message = 'Ahtung!'

def find_text(text: str):
    if word_search in text:
        send_telegram(message)
        print(message)


def send_telegram(text: str):

    url = "https://api.telegram.org/bot" + settings.token
    chat_id = settings.chat_id

    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": chat_id,
         "text": text
          })

    if r.status_code != 200:
        print('Error send to telegram')


def main():
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

        data = data.decode(encoding)
        find_text(data)
        
        with open('data.txt', 'a') as file_data:
            file_data.write(str(datetime.today().strftime("%Y-%m-%d %H:%M:%S") + '\n'))
            file_data.write(data + '\n')


        sleep(10)


if __name__ == '__main__':
    main()

