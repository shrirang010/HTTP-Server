import socket
from _thread import *
import threading

print_lock = threading.Lock()

def thread_client(client):
    while(True):
        data=client.recv(1024).decode('utf-8')
        if(data == "exit"):
                client.close()
        
def client_request_handler(server):
    client,address,=server.accept()
    print_lock.acquire()
    start_new_thread(thread_client,(client ,))

def main():
    HOST="127.0.0.1"
    PORT=8000
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((HOST,PORT))
    server.listen()
    client_request_handler(server)


if __name__ ==  '__main__':
    main()
