import time
from socket import *
from config import *


class Server:
    def __init__(self, IP, PORT):
        self.ip = IP
        self.port = PORT
        self.client_threads = []
        self.server_socket = socket(AF_INET, SOCK_STREAM)  # TCP socket
        self.server_socket.bind(('', self.port))
        self.server_socket.listen(1)

    def main_menu(self):
        while True:
            print(f"Starting the HTTP Server using port {self.port}")
            print("*"*25, "\n")
            print("Displaying the main menu...\n")
            print("Press s to start the server")
            print("Press q to exit the program!")
            choice = input()
            if choice.lower() == 's':
                print("Starting the server...")
                time.sleep(2)
                self.server()
            if choice.lower() == 'q':
                print("Quitting the server...")
                time.sleep(1)
                exit(0)
            else:
                print(f"Invalid input: {choice}")
                print("*"*25, "\n\n\n")
                continue

    def server(self):
        print("Inside server method...")
        print(f"Go to browser at : http://{self.ip}/{self.port}")
        # print("Server Port number : {self.port}")

        self.func("runs good till here")
        # conn_socket, addr = self.server_socket.accept() # conn_socket -> socket to transfer data; addr -> address of socket on other end of conn
        # self.client_threads.append(conn_socket) # add connections to the list of client threads

    def func(self, arg):
        print(f"Hello {arg}")
