# ALGORITHMS TO IMPLEMENTING THE HTTP SERVER

## RESPONSE FROM SERVER

1. Create a class let's say `HTTP_Response`
2. Create a method to determine the status code for the request - `status_code()`
3. Create a method to determine the type of HTTP request `request_type()` - **GET, POST, PUT, DELETE, etc**
4. Create a method to check if it is a **conditional GET** and respond accordingly
4. Depending on the type of request, Create appropriate methods to generate response for each type - `response_GET(), respose_POST(), response_PUT(), etc`
5. Create a method to **send response** to the **client** 
```
if method.upper() == 'GET':
    response_GET()
if method.upper() == 'POST':
    response_POST()
```

```
def response_GET():
    return response_headers, response_body
```