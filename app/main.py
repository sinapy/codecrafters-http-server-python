# Uncomment this to pass the first stage
import socket
import re
import threading


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        connection, address = server_socket.accept() # wait for client
        threading.Thread(target=lambda: handleHttpRequest(connection)).start() 

def handleHttpRequest(connection):
    data = connection.recv(1024)
    print(data)
    route = data.split(b" ")[1]
    if (route == b"/"):
        connection.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    elif route.split(b"/")[1] == b"echo" and len(route.split(b"/")) == 3 and route.split(b"/")[2] != b"":
        connection.sendall(b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nContent-Length: %d\r\n\r\n%s" % (len(route.split(b"/")[2]), route.split(b"/")[2]))
    elif route.split(b"/")[1] == b"user-agent":
        user_agent = [x for x in data.split(b"\r\n") if x.startswith(b"User-Agent:")][0].removeprefix(b"User-Agent:").strip()
        connection.sendall(b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nContent-Length: %d\r\n\r\n%s" % (len(user_agent), user_agent))
    elif data.split()[0] == "GET" and route.split(b"/")[1] == b"files" and len(route.split(b"/")) == 3 and route.split(b"/")[2] != b"":
        try:
            with open(b"/tmp/data/codecrafters.io/http-server-tester/" + route.split(b"/")[2], "rb") as f:
                file_data = f.readline()
                print(b"HTTP/1.1 200 OK\r\nContent-type: application/octet-stream\r\nContent-Length: %d\r\n\r\n%s" % (len(f.read()), f.read()))
                connection.sendall(b"HTTP/1.1 200 OK\r\nContent-type: application/octet-stream\r\nContent-Length: %d\r\n\r\n%s" % (len(file_data), file_data))
        except FileNotFoundError:
            print('hello 2')
            connection.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
    elif data.split()[0] == "POST" and route.split(b"/")[1] == b"files" and len(route.split(b"/")) == 3 and route.split(b"/")[2] != b"":
        try:
            with open(b"/tmp/data/codecrafters.io/http-server-tester/" + route.split(b"/")[2], "wb") as f:
                f.write(data.split(b"\r\n\r\n")[1])
                connection.sendall(b"HTTP/1.1 201 Created\r\n\r\n")
        except FileNotFoundError:
            print('hello')
            connection.sendall(b"HTTP/1.1 Hello")
    else:
        connection.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

if __name__ == "__main__":
    main()
