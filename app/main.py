import socket

def handle_request(data) -> str:
    data = data.decode("utf-8")
    http_method = data.split("/r/n")[0]
    path = http_method.split()[1]
    print(f"path: {path}")
    if path != "/":
        response = b"HTTP/1.1 200 OK\r\n\r\n"
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
