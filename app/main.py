import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept() # wait for client
    data = conn.recv(1024)
    data = data.decode("utf-8")
    http_method = data.readline()
    path = http_method.split()[1]
    if not path.startswith("/"):
        response = b"HTTP/1.1 200 OK\r\n\r\n"
    else:
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"
    conn.send(response)
    conn.close()


if __name__ == "__main__":
    main()
