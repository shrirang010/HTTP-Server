import argparse
from config import *
from httpServer import Server


parser = argparse.ArgumentParser()    


def pre_start():
    # adding args
    parser.add_argument('--port', '-p', default=5432, type=int, help='Enter port number to listen on')
    parser.add_argument('--size', '-s', default=4096, type=int, help='Enter size')

    http_port = parser.parse_args()
    PORT = http_port.port

    if http_port is not None:
        driver_obj = Server(IP, PORT)
        driver_obj.main_menu()


if __name__ == '__main__':
    pre_start()
