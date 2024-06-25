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
    elif route.split(b"/")[1] == b"user-agent":
        print(data.split(b"\r\n"))
        user_agent = [x for x in data.split(b"\r\n") if x.startswith(b"User-Agent:")][0].removeprefix(b"User-Agent:").strip()
        connection.sendall(b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nContent-Length: %d\r\n\r\n%s" % (len(user_agent), user_agent))
    else:
        connection.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

if __name__ == "__main__":
    main()
