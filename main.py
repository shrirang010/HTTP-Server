import argparse
import os
from config import *


parser = argparse.ArgumentParser()


def start(PORT):
    os.system(f'python3 httpServer.py {PORT}')    # starts the http server
    while True:
        print(f"Starting the HTTP Server using port {PORT}")
        print("*"*25, "\n")
        print("Displaying the main menu...\n")
        print("Press q to quit")
        choice = input()
        if choice == 'q':
            print("Quitting the server...")
            exit(0)
        else:
            print(f"Invalid input: {choice}")
            print("*"*25, "\n\n\n")
            continue


def pre_start():
    # adding args
    parser.add_argument('--port', '-p', default=5432, help='Enter port number to listen on')

    http_port = parser.parse_args()
    PORT = http_port.port

    if http_port is not None:
        start(PORT)


if __name__ == '__main__':
    pre_start()
