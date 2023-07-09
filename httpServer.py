import sys
from socket import *
from config import *

if __name__ == "__main__":
    ip = IP
    port = int(sys.argv[1])
    server_socket = socket(AF_INET, SOCK_STREAM)  # TCP socket
    try:
        server_socket.bind(('', port))
    except:
        print("ENTER THE FOLLOWING COMMAND TO RUN THE SERVER : \npython3 main.py --port <port_number>")
        exit(0)
    server_socket.listen(4) # it is the number of unnaccepted connections the system will allow before refusing connections
    # connect to the server hereafter
    exit(0)