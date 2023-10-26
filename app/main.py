import socket
def parse_request(data) -> {str, str}:
    data = data.decode("utf-8")
    data_lines = data.split("/r/n")
    http_method = data_lines[0]
    host = data_lines[2]
    user_agent = data_lines[3]
    method = http_method.split()[0]
    path = http_method.split()[1]
    return method, path, host, user_agent
    
def handle_request(data) -> str:
    method, path, host, user_agent = parse_request(data)
    if method == "GET":
        if path == "/":
            response = b"HTTP/1.1 200 OK\r\n\r\n"
        elif path.startswith("/echo"):
            random_text = path[6:]
            text_len = len(random_text)
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {text_len}\r\n\r\n{random_text}".encode("utf-8")
        elif path.startswith("/user-agent"):
            text_len = len(user_agent)
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {text_len}\r\n\r\n{user_agent}".encode("utf-8")
        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"

    return response

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    client_socket, client_addr = server_socket.accept() # wait for client
    data = client_socket.recv(1024)
    response = handle_request(data)
    client_socket.send(response)

    client_socket.close()


if __name__ == "__main__":
    main()
