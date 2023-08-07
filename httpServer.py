from config import *
import socket
import sys
from _thread import *
import os
from utilities.breakdown import breakdown

class HTTPMethods:
    def __init__(self, socket_connection, method, entity, query, switcher, server_socket, conn, client_thread, IP, PORT, f_flag):
        self.socket_connection = socket_connection
        self.method = method
        self.entity = entity
        self.query = query
        self.switcher = switcher
        self.server_socket = server_socket
        self.conn = client_thread
        self.client_thread = client_thread
        self.f_flag = f_flag


    def determine_method(self):
        """
        Checks which is the method requested and calls the appropriate function.
        """
        print("\nInside HTTPMethods.determine_method()\n")
        print(f"self.method : {self.method}")
        if self.method == 'GET':
            self.handle_GET()
        elif self.method == 'POST':
            self.handle_POST()
        elif self.method == 'PUT':
            self.handle_PUT()
        elif self.method == 'DELETE':
            self.handle_DELETE()
        elif self.method == 'HEAD':
            self.handle_HEAD()
        print("\nEND HTTPMethods.determine_method()\n")
        
    def handle_GET(self):
        print("\nInside HTTPMethods.handle_GET()\n")
        print("\nSending dummy status code from handle_GET() to status() method!\n")
        server(PORT).status(self.socket_connection, 403)
    
    def handle_HEAD(self):
        pass

class server:
    def __init__(self, PORT):
        self.conn = True
        self.HOST = SERVER_IP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_threads_list = list()
        self.f_flag = 0 # required for PUT method
        self.scode = 0  # status code initialization
    
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
                message = self.socket_connection.recv(SIZE)
            except Exception as e:
                print(f"\nError while receiving data: {e}\n")
            try:
                self.f_flag = 0
                message = message.decode('utf-8')
                req_list = message.split('\r\n\r\n')
            except UnicodeDecodeError:
                self.f_flag = 1
                req_list = message.split(b'\r\n\r\n')
                req_list[0] = req_list[0].decode(errors='ignore')
            if(len(req_list) == 1):
                self.status(505)
                break
            elif len(req_list) == 0:
                print("Return Status code : 505 with error in headers")
                break
            ent_body = req_list[1]  # not used in GET requests, but in PUT, POST, DELETE etc
            header_list = req_list[0].split('\r\n')
            request_line = header_list[0].split(' ')
            print(f"\nmessage : {message}\n")
            print(f"\nent_body : {ent_body}\n")
            print(f"\nrequest_line : {request_line}\n")
            print(f"\nentire req_line : {req_list}\n")
            if len(req_list) < 2:
                print("Return status code : 505")
            self.method = request_line[0]
            self.entity = request_line[1]
            if self.entity == '/':
                self.entity = os.getcwd()
            elif self.entity == favicon or self.entity == 'favicon' or self.entity == 'favicon.ico':
                self.entity = FAVICON
            self.entity, self.query = breakdown(self.entity)
            print(f"entity: {self.entity}, query: {self.query}")
            if len(self.entity) > MAX_URL:
                print("Return status code 414")
                self.socket_connection.close()
                break
            version = request_line[2]
            print(f"HTTP version: {version}")
            try:
                version_num = version.split('/')[1]
                if version_num != RUNNING_VERSION:
                    print("Return status code : 505")
            except IndexError:
                print("Return status code : 505")
            request_line = header_list.pop(0)
            self.switcher = dict()
            for x in header_list:
                item = x.split(': ')
                self.switcher[item[0].strip()] = item[1].strip()
            print(f"switcher : {self.switcher}")
            break
            # if self.method == 'HEAD':
            # send socket_connection, method, entity, query, switcher, server_socket, conn, client_thread, IP, PORT, f_flag to the httpmethod class for further calling the appropriate methods
        
        http_obj = HTTPMethods(self.socket_connection, self.method, self.entity, self.query, self.switcher, self.server_socket, self.conn, self.client_threads_list, SERVER_IP, PORT, self.f_flag)
        http_obj.determine_method()

        print("\nEND server.client_handler()\n")
        return
    

    def status(self, socket_connection, code):
        """
        Responds to the client when server is busy
        """
        print("\nINSIDE server.status()\n")
        print("Received STATUS : ", code)
        show_response = ''
        self.scode = code
        if(int(code) == 505):
            print("Return Status code : 505")
            show_response += 'HTTP/1.1 505 HTTP version not supported'
        elif(int(code) == 415):
            print("Return Status code : 415")
            show_response += 'HTTP/1.1 415 Unsupported Media Type'
        elif(int(code) == 403):
            print("Return Status code : 403")
            show_response += 'HTTP/1.1 403 Forbidden'
        elif(int(code) == 404):
            print("Return Status code : 404")
            show_response += 'HTTP/1.1 404 Not Found'
        elif (int(code) == 414):
            print("Return Status code : 414")
            show_response += 'HTTP/1.1 414 Request-URI Too Long'
        elif(int(code) == 500):
            print("Return Status code : 500")
            show_response += 'HTTP/1.1 500 Internal Server Error'
        elif(int(code) == 503):
            print("Return Status code : 503")
            show_response += 'HTTP/1.1 503 Service Unavailable'
        show_response += '\r\nServer: ' + self.HOST + ':' + str(PORT)
        show_response += '\r\n' + "DATE!!!"
        show_response += '\r\n\r\n'
        encoded = show_response.encode()
        socket_connection.send(encoded)
        try:
            self.client_threads_list.remove(socket_connection)
            socket_connection.close()
        except:
            pass
        print("\nEND server.status()\n")
        return

    def run_server(self):
        print("\nINSIDE server.run_server()\n")
        self.server_socket.bind((self.HOST, PORT))    # server will have the IP address 127.0.0.1 and will listen on port 'PORT'
        self.server_socket.listen(5)
        print('http://'+ self.HOST+':'+str(PORT)+'/')
        print("client_threads_list : ",self.client_threads_list)
        while True:
            if len(self.client_threads_list) < MAX_CLIENT_REQUESTS:
                self.socket_connection, client_addr = self.server_socket.accept()
                self.client_threads_list.append(self.socket_connection) 
                print(f"\n length : {len(self.client_threads_list)}  client_threads_list : {self.client_threads_list}\n")
                start_new_thread(self.client_handler, ())
                # break   # at present, if the conn limit exceeds 6, the server is shut down immediately
            else:
                print("\n\n\nMAX CONNECTION LIMIT REACHED!\n\n")
                # send status 503 and close connection
                self.socket_connection.close()
                break

        self.server_socket.close()  # shut down the server socket
        
        print("\nEND OF server.run_server()\n")
        return


if __name__ == "__main__":
    PORT = int(sys.argv[1])
    s1 = server(PORT)
    s1.run_server()
