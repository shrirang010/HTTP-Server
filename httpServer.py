from config import *
import socket
import sys
from _thread import *

class httpMethods:
    def __init__(self):
        pass

class server:
    def __init__(self, PORT):
        self.conn = True
        self.HOST = SERVER_IP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_threads_list = list()
        self.f_flag = 0

    def run_server(self):
        print("\nINSIDE server.run_server()\n")
        self.server_socket.bind((self.HOST, PORT))    # server will have the IP address 127.0.0.1 and will listen on port 'PORT'
        self.server_socket.listen(5)
        print('http://'+ self.HOST+':'+str(PORT)+'/')
        print("client_threads_list : ",self.client_threads_list)
        while True:
            self.socket_connection, client_addr = self.server_socket.accept()
            self.client_threads_list.append(self.socket_connection) 

            if len(self.client_threads_list) > MAX_CLIENT_REQUESTS:
                print("\n\n\nMAX CONNECTION LIMIT REACHED!\n\n")
                # send status 503 and close connection
                self.socket_connection.close()
                continue
            else:
                print(f"\n length : {len(self.client_threads_list)}  client_threads_list : {self.client_threads_list}\n")
                start_new_thread(self.client_handler())

        self.server_socket.close()
        
        print("\nEND OF server.run_server()\n")
        return
    
    def client_handler(self):
        print("\nINSIDE server.client_handler()\n")
        while True:
            if not self.conn:
                break
            if SIZE != 0:
                pass
            else:
                break
            try:
                self.message = self.socket_connection.recv(SIZE)
            except Exception as e:
                print(f"\nError while receiving data: {e}\n")
            try:
                self.f_flag = 0
                self.message = self.message.decode('utf-8')
                self.req_list = self.message.split('\r\n\r\n')
            except UnicodeDecodeError:
                self.f_flag = 1
                self.req_list = self.message.split(b'\r\n\r\n')
                self.req_list[0] = self.req_list[0].decode(errors='ignore')
            print(f"message : {self.message}")
            # write further code here
        print("\nENDserver.client_handler()\n")
        return

    # def test(self):
    #     print("\nINSIDE server.test()\n")
    #     print(f"client_threads_list : {self.client_threads_list}")
    #     print(f"REMOVING item from list...")
    #     self.client_threads_list.remove(self.socket_connection)
    #     self.socket_connection.close()
    #     print(f"AFTER REMONING client_threads_list : {self.client_threads_list}")
    #     print("\nEND OF server.test()\n")   
    #     return


if __name__ == "__main__":
    PORT = int(sys.argv[1])
    s1 = server(PORT)
    s1.run_server()