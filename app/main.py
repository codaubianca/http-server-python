import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

def parse_request(data) -> {str, str}:
    data = data.decode("utf-8")
    data_lines = data.split("\r\n")
    print("http header: ", data_lines[0])
    method, path, version = data_lines[0].split(" ")
    headers = {}
    for line in data_lines[1:]:
        if line == "":
            continue
        key, content = line.split(": ")
        headers[key] = content
    return method, path, version, headers
    
def handle_request(data) -> str:
    method, path, version, headers = parse_request(data)
    if method == "GET":
        if path == "/":
            response = b"HTTP/1.1 200 OK\r\n\r\n"
        elif path.startswith("/echo"):
            random_text = path[6:]
            text_len = len(random_text)
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {text_len}\r\n\r\n{random_text}".encode("utf-8")
        elif path.startswith("/user-agent"):
            user_agent = headers["User-Agent"]
            text_len = len(user_agent)
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {text_len}\r\n\r\n{user_agent}".encode("utf-8")
        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"

    return response

def accept_wrapper(server_socket):
    client_socket, client_addr = server_socket.accept() # wait for client
    client_socket.setblocking(False)
    print("Accepted connection from ", client_addr)
    data = types.SimpleNamespace(addr=client_addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(client_socket, events, data=data)


def server_connection(key, mask):
    client_socket = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = client_socket.recv(1024)
        if recv_data:
            print("receiving data:", recv_data)
            data.outb += recv_data
        else:
            sel.unregister(client_socket)
            client_socket.close()
    
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print("final data.outb:", data.outb)
            response = handle_request(data.outb)
            sent = client_socket.send(response)
            data.outb = data.outb[sent:]


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.setblocking(False)
    sel.register(server_socket, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    server_connection(key, mask)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        sel.close()


if __name__ == "__main__":
    main()
