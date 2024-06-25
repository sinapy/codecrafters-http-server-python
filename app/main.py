# Uncomment this to pass the first stage
import socket
import re


def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    connection, address = server_socket.accept() # wait for client
    data = connection.recv(1024)
    route = data.split(b" ")[1]
    if (route == b"/"):
        connection.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    elif route.split(b"/")[1] == b"echo" and len(route.split(b"/")) == 3 and route.split(b"/")[2] != b"":
        connection.sendall(b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nContent-Length: %d\r\n\r\n%s" % (len(route.split(b"/")[2]), route.split(b"/")[2]))
    else:
        connection.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

if __name__ == "__main__":
    main()
