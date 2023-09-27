# HTTP Server v1.1


This is a Python-based HTTP server that implements version 1.1 of the HTTP protocol. It is designed to handle various HTTP methods including HEAD, GET, PUT, POST, and DELETE. With multi-threading capabilities, it efficiently manages multiple client connections simultaneously.

---

## Features

- **HTTP/1.1 Protocol**
- **Built with Socket Programming**
- **Multi-threaded for concurrent multiple client connections**
- **Supported HTTP Methods**
- **Handles status codes**

---

## Getting Started

### **Prerequisites**

Before you begin, ensure you have the following prerequisites:

- Python3 installed on your system.
- Basic understanding of HTTP protocols.

### **Installation**

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/akshaykhoje/HTTP-Server.git
    ```

2. Navigate to the project directory:

    ```bash
    cd  HTTP-Server
    ```

###  **Run the Server**

   ```bash
    python3 httpServer.py [portNumber]
   ```

### **Close the Server**

```
Press Ctrl+C to exit
```

---

## Supported HTTP Methods

- **HEAD**: Retrieve the headers for a resource without the actual content.
- **GET**: Retrieve the content of a resource along with the headers.
- **POST**: Submit data to be processed by a resource, often used for form submissions.
- **PUT**: Create a new resource or replace a representation of the target resource.
- **DELETE**: Remove a resource from the server.with the request payload

The above methods can be used as following:
1. HEAD => Use Postman
2. GET => Use Browser/Postman
3. POST => Use Browser/Postman
4. PUT => Use Postman
5. DELETE => Use commandline as follows:
> curl -X DELETE http://127.0.0.1:portNumber/database.txt/id

---

## Resources Used

- [HTTP MDN DOCS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
- [Socket Programming](https://realpython.com/python-sockets/)
- [Thread](https://stackoverflow.com/questions/5882362/thread-start-new-thread-vs-threading-thread-start)
- [Thread2](https://python-course.eu/applications-python/threads.php)

## Learning Outcomes

- Our understanding of HTTP and the underlying paradigms got better
- Better understanding  of the Python programming language
- Concepts of Object Oriented Programming revised
- Linux command line and network commands
- Postman API

---
<br>

## Project Execution

### GET RESPONSE 
Step 1
![1](https://github.com/shrirang010/HTTP-Server/assets/103894310/7fc27201-586a-41d8-8241-7e59efe4bc38)
<br>
Step 2
![Screenshot from 2023-09-26 10-43-02](https://github.com/shrirang010/HTTP-Server/assets/103894310/7f9cc6df-fbb5-45ef-a570-d7ecc1725815)
<br>
Step 3
![Screenshot from 2023-09-26 10-27-27](https://github.com/shrirang010/HTTP-Server/assets/103894310/4cf4dd5f-8090-47b8-945e-0d88cbc07c9c)
---
### POST REPSPONSE
Step 1
![1](https://github.com/shrirang010/HTTP-Server/assets/103894310/7fc27201-586a-41d8-8241-7e59efe4bc38)
<br>
Step 2
![2](https://github.com/shrirang010/HTTP-Server/assets/103894310/dd3f9922-011e-48dc-9ad6-1f935822b7f9)
<br>
Step 3
![3](https://github.com/shrirang010/HTTP-Server/assets/103894310/b30e60d4-32da-494a-bf32-344ebd16b5a6)
**Note:**
This project was developed by beginner-level python developers with primitive understanding of applications of networking in the real world.
--- 
<br>
        
<p style="text-align: center; font-size: 24px; font-weight: bold; font-style:italic">ARIGATOU 😊</p>
