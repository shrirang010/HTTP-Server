import socket
from _thread import *
import signal
from urllib.parse import parse_qs
import os
import csv
import datetime


def read_file_contents(file_path):
    content = ""
    with open(file_path, 'r') as file:
        for line in file:
            content += line.strip()  # Remove leading/trailing whitespace if desired
    return content


def date():
    #  Sun, 06 Nov 1994 08:49:37 GMT  ; RFC 822, updated by RFC 1123
    # Sunday, 06-Nov-94 08:49:37 GMT ; RFC 850, obsoleted by RFC 1036
    # Sun Nov  6 08:49:37 1994       ; ANSI C's asctime() format
    now = datetime.datetime.now()
    datenow = now.strftime('%A,%d %B %Y %H:%M:%S ')
    datenow += "GMT"
    conversation = 'Date: ' + datenow
    return conversation


def handle_get_request(client, port,entity,serverport):
    print(f"Sending request to {client}:{port}")
    print("Entity : ",entity)
    isItFile = os.path.isfile(entity)
    isItDir = os.path.isdir(entity)
    text = 'HTTP/1.1 200 OK'
    ip = '127.0.0.1'
    text += '\r\nContent-type: text/html; charset=utf-8'
    text += '\r\n Connection: keep-alive'
    text += '\r\n Content-Language: en-US'
    text += '\r\n Server:' + ip
    text += '\r\nStrict-Transport-Security: max-age=63072000'
    text += '\r\nX-Content-Type-Options: nosniff'
    text += '\r\nX-Frame-Options: DENY'
    text += '\r\nX-XSS-Protection: 1; mode=block'
    text += '\r\n\r\n'
    # Adding data
    text += '\r\n<!DOCTYPE html>'
    text += '\r\n<html lang="en">'
    text += '\r\n<head>'
    text += '\r\n<meta charset="utf-8">'
    text += '\r\n<title>A simple webpage</title>'
    text += '\r\n</head>'
    text += '\r\n<body>'
    text += '\r\n<h1>Current Directory </h1>'
    text += '\r\n<p>Hello, world!</p>'
    if(isItDir):
        dir_list = os.listdir(entity)    
        for line in dir_list:
            if entity == '/':
                # link = 'http://' + ip + ':' + str(serverport) + entity + '/'+ line
                l = '\r\n<li><a href ="'+link+'">'+line+'</a></li>'
                text += l
            else:
                link = 'http://' + ip + ':' + str(serverport) + entity + '/'+ line
                l = '\r\n<li><a href ="'+link+'">'+line+'</a></li>'
                text += l
    elif(isItFile):
        try:
            size = os.path.getsize(entity)
            f = open(entity, "rb")
            text += '\r\n</body>'
            text += '\r\n</html>'
            # client.send(text.encode())
            client.sendfile(f)
        except:
            pass
        return
    text += '\r\n</body>'
    text += '\r\n</html>'
    print("Sending response...")
    client.send(text.encode())


def handle_post_request(client, port, ent_body):
    entity = os.getcwd() + '/output.csv'
    query = parse_qs(ent_body)
    print("entity : ", entity)
    print("query : ", query)
    if os.access(entity, os.W_OK):
        print("You can write to the fiel!")
    else:
        print("NO ACCESS GRANTED FOR POST REQUEST")
    fields = ''
    row = ''
    for d in query:
        fields += ', '
        for i in query[d]:
            row += i + ', '
    file_exists = os.path.exists(entity)
    if file_exists:
        fi = open(entity, "a")
        show_response += 'HTTP/1.1 200 OK'
        scode = 200
        csvwriter = csv.writer(fi)
        csvwriter.writerow(row)
    else:
        fi = open(entity, "w")
        show_response += 'HTTP/1.1 201 Created'
        scode = 201
        show_response += '\r\nLocation: ' + entity
        csvwriter = csv.writer(fi)
        csvwriter.writerow(fields)
        csvwriter.writerow(row)
    fi.close()

    show_response += date()
    f = open("./workfile.html", "rb")
    show_response += '\r\nContent-Language: en-US,en'
    size = os.path.getsize("./workfile.html")
    conversation = 'Content-Length: ' + str(size)
    show_response += '\r\nContent-Type: text/html'
    show_response += '\r\n' + conversation

    encoded = show_response.encode()
    client.send(encoded)
    client.sendfile(f)


def client_request_handler(server, client, port,serverport):
    try:
        while True:
            data = client.recv(1024)  # HTTP REQUEST FROM CLIENT
            print("Hello here is client http request from  PORT", port)
            print()  # Print empty line just for better output display
            req_body = data.decode('utf-8')
            print("req_body :::  ",req_body)
            Request_body_array =req_body.split(' ')
            # CHECK IF METHOD IS GET/POST/DELETE
            print("Checking request method ......")

            # PREPARE HTTP RESPONSE ACCORDING TO THE REQUEST
            print("Preparing appropriate response .. ")

            # call the appropriate method for the type of request here
            req_list = req_body.split('\r\n\r\n')
            # ent_body = req_list[1]   #CONTAINS HEADERS
            method = Request_body_array[0]
            # print()
            entity=Request_body_array[1]
            if(entity == '/'):
                entity=os.getcwd()
            else:   
                entity =os.getcwd() + '/favicon.ico'
            if method == 'GET':
                handle_get_request(client, port,entity,serverport)
            # elif method == 'POST':
            # print("req_list : ", req_list)
            # print("ent_body : ", ent_body)
            # handle_post_request(client, port, ent_body)

            if not data:
                print("IF NOT DATA!!!")
                break

    except socket.timeout:
        pass
    client.close()
    print("Connection  closed for", port)
    return


def main():
    HOST = "127.0.0.1"
    PORT = 21009
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    while (True):
        # TCP CONNECTION ESTABLISHED BETWEEN SERVER & CLIENT
        client, address, = server.accept()
        print("Connected to ", address[0], address[1])
        start_new_thread(client_request_handler, (server, client, address[1],PORT))


if __name__ == '__main__':
    main()
