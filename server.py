import socket
from _thread import *
import signal

def read_file_contents(file_path):
    content = ""
    with open(file_path, 'r') as file:
        for line in file:
            content += line.strip()  # Remove leading/trailing whitespace if desired
    return content

def client_request_handler(server,client,port):
        try:
            while True:
                data = client.recv(1024)                         #HTTP REQUEST FROM CLIENT
                print("Hello here is client http request from  PORT",port)
                print() #Print empty line just for better output display 
                print(data.decode())

                print("Checking request method ......")         #CHECK IF METHOD IS GET/POST/DELETE

                print("Preparing appropriate response .. ")     #PREPARE HTTP RESPONSE ACCORDING TO THE REQUEST
                text ='HTTP/1.1 200 OK'
                ip ='127.0.0.1'
                text+='\r\nContent-type: text/html; charset=utf-8'
                text+='\r\n Connection: keep-alive'
                text+='\r\n Content-Language: en-US'  
                text+='\r\n Server:' + ip
                text+='\r\nStrict-Transport-Security: max-age=63072000'
                text+='\r\nX-Content-Type-Options: nosniff'
                text+='\r\nX-Frame-Options: DENY'
                text+='\r\nX-XSS-Protection: 1; mode=block'
                text+='\r\n\r\n'
                #Adding data
                text+='\r\n<!DOCTYPE html>'
                text+='\r\n<html lang="en">'
                text+='\r\n<head>'
                text+='\r\n<meta charset="utf-8">'
                text+='\r\n<title>A simple webpage</title>'
                text+='\r\n</head>'
                text+='\r\n<body>'
                text+='\r\n<h1>Current Directory </h1>'
                text+='\r\n<p>Hello, world!</p>'
                text+='\r\n</body>'
                text+='\r\n</html>'
                print("Sending response...")
                client.send(text.encode()) 
                if not data:
                    break
        except socket.timeout:
            pass
        client.close()
        print("Connection  closed for",port)
        return 

def main():
    HOST="127.0.0.1"
    PORT=  9530
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((HOST,PORT))
    server.listen(5)
    while(True):
        client,address,=server.accept()    # TCP CONNECTION ESTABLISHED BETWEEN SERVER & CLIENT
        print("Connected to ",address[0],address[1])
        start_new_thread(client_request_handler,(server,client,address[1]))
if __name__ ==  '__main__':
    main()
