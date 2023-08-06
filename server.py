import socket
from _thread import *
import signal
from urllib.parse import parse_qs
import os
import datetime


def read_file_contents(file_path):
    content = ""
    with open(file_path, 'r') as file:
        for line in file:
            content +="\r\n"+ line.strip()  # Remove leading/trailing whitespace if desired
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

def handle_delete_request(client,clientport,resource): 
    #if present then delete and send status code 204
    #check if resource is present
    #if resource is /database.txt/123 where 123 is id
    #extract id from resource
    #delete resource
    ip='127.0.0.1'
    index=resource.find('database.txt/')
    if(index == -1):
        #call status code error
        print("Not found")
        return
    id=resource[index+13:]
    with open("./database.txt",'r') as file:
        lines=file.readlines()
    count=len(lines)
    with open("database.txt",'r') as file:    
        for line in file:
            row=line.split(' ')
            if(row[0] == id):
                lines.remove(line)
                break
    if(len(lines) == count):
        print("Resource Not found")
        #call status code error
        exit        
    else:
        with open("database.txt",'w') as file:
            file.writelines(lines)
        print("Resource Deleted successfully!") 
    text='\r\nHTTP/1.1 204 No Content'
    text += '\r\nConnection: keep-alive'
    text += '\r\nContent-Language: en-US'
    text += '\r\nServer: ' + ip
    client.send(text.encode())

def handle_get_request(client, port,entity,serverport):
    isItFile = os.path.isfile(entity)
    isItDir  = os.path.isdir(entity)
    ip = '127.0.0.1'
    textdata=''
    if(isItDir):
        textdata += '\r\n<!DOCTYPE html>'
        textdata += '\r\n<html lang="en">'
        textdata += '\r\n<head>'
        textdata += '\r\n<meta charset="utf-8">'
        textdata += '\r\n<title>STUDY MATERIAL</title>'
        textdata += '\r\n</head>'
        textdata += '\r\n<body>'
        textdata += '\r\n<h1>Current Directory </h1>'
        dir_list1 = os.listdir(entity)
        textdata+="\r\n<ul>"    
        for line in dir_list1:
            if entity == '/':
                # link = 'http://' + ip + ':' + str(serverport) + entity + '/'+ line
                l = '\r\n<li><a href ="'+link+'">'+line+'</a></li>'
                text += l
            else:
                link = 'http://' + ip + ':' + str(serverport) + entity + '/'+ line
                l = '\r\n<li><a href ="'+link+'">'+line+'</a></li>'
                textdata += l
        textdata+="\r\n</ul>"
        textdata+="\r\n<br>"
        textdata+="\r\n<h2>Post Request Form</h2>"
        textdata+=read_file_contents("./postform.html")
        textdata += '\r\n</body>'
        textdata += '\r\n</html>'
        dir_data_length=len(textdata)   #Length of data to be sent if a directory
    #Preparing http get response
    text = '\r\nHTTP/1.1 200 OK'
    text += '\r\nConnection: keep-alive'
    text += '\r\nContent-Language: en-US'
    text += '\r\nServer: ' + ip
    text += '\r\nStrict-Transport-Security: max-age=63072000'
    text += '\r\nX-Content-Type-Options: nosniff'
    text += '\r\nX-Frame-Options: DENY'
    text += '\r\nX-XSS-Protection: 1; mode=block'
    # Adding data
    if(isItDir):
        text += '\r\nContent-type: text/html; charset=utf-8'
        text+='\r\nContent-length: '+str(dir_data_length)
        text += '\r\n\r\n'
        text+=textdata
        encoded=text.encode()
        client.send(encoded)
        print("Response Sent...",port)
    elif(isItFile):
        size = os.path.getsize(entity)
        text+='\r\n\Content-type: text/plain'
        text+='\r\nContent-length: '+str(size)
        text += '\r\n\r\n'
        try:            
            f = open(entity, "rb")
            encoded=text.encode()
            client.send(encoded)
            client.sendfile(f)
            print("Response Sent... ",port)
        except:
            pass
        return
    else:
        pass
    return    

def handle_post_request(client,clientport,entity,headers,post_data):
        index=headers.find('Content-Type:')
        content_type =headers[index+14 : index+14+33]
        if(content_type != 'application/x-www-form-urlencoded'):
            #some status code 
            pass
        #Process & Extract Post method data
        print(post_data) 
        index1= post_data.find("name=")
        index2= post_data.find("&email")
        Name =post_data[index1+5:index2]
        index3=post_data.find("mis=")
        index4=post_data.find("&name")
        Id=post_data[index3+4 :index4]
        index1=post_data.find("email=")
        Email=post_data[index1+6:]

        #Write the processed data to database.txt
        f =open("database.txt","+a")
        f.write("\n")
        f.write(Id + "  "+ Name + " " + Email)
        responsedata=read_file_contents("./postresponse.html")
        text = 'HTTP/1.1 200 OK'
        ip = '127.0.0.1'
        text += '\r\nConnection: keep-alive'
        text += '\r\nContent-Language: en-US'
        text+='\r\nContent-length: '+str(len(responsedata))
        text += '\r\nContent-type: text/html; charset=utf-8'
        text += '\r\n Server: ' + ip
        text+="\r\n\r\n"
        text+=responsedata
        client.send(text.encode())
        return
    
def client_request_handler(server, client, port,serverport):
    try:
        while True:
            data = client.recv(1024)  # HTTP REQUEST FROM CLIENT
            print("Hello here is client http request from  PORT", port)
            print()
            req_body = data.decode('utf-8')
            if(len(req_body) == 0):
                break
            Request_body_array =req_body.split(' ')
            method = Request_body_array[0]
            entity = Request_body_array[1]
            version= Request_body_array[2]

            req_list = req_body.split('\r\n\r\n')
            headers=req_list[0]

            if(method == "POST"):
                post_data=req_list[1]
            
            if(entity == '/'):
                entity=os.getcwd()
            elif(entity == '/favicon.ico'):   
                entity =os.getcwd() + '/favicon.ico'

            if method == 'GET':
                handle_get_request(client, port,entity,serverport)
            elif method == 'POST':
                handle_post_request(client, port,entity,headers,post_data)
            elif method == 'DELETE':
                handle_delete_request(client,port,entity)
            if not data:
                print("IF NOT DATA!!!")
                break
    except socket.timeout:
        pass
    client.close()
    print("Connection  closed for", port)
    return


def main():
    HOST = '127.0.0.1'
    PORT = 8135
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print('http://'+ HOST+':'+str(PORT)+'/')
    while (True):
        # TCP CONNECTION ESTABLISHED BETWEEN SERVER & CLIENT
        client, address, = server.accept()
        print("Connected to ", address[0], address[1])
        start_new_thread(client_request_handler, (server, client, address[1],PORT))


if __name__ == '__main__':
    main()