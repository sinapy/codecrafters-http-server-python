# Uncomment this to pass the first stage
import socket


def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    connection, address = server_socket.accept() # wait for client
    data = connection.recv(1024).split()[1]
    if (data == b"/"):
        connection.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    else:
        connection.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

if __name__ == "__main__":
    main()
