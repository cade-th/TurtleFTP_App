import socket

BUFFER_SIZE = 1024  # Size of chunks (1 KB)

def tcp_client():
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 8000)  # Replace with your server's IP and port
    clientSocket.connect(server_address)

    while True:
        command = input("Enter command (SEND/RETR): ")
        filename = input("Enter filename: ")

        if command.upper() == "SEND":
            clientSocket.send(f"{command}|{filename}".encode())
            try:
                with open(filename, 'rb') as f:
                    while True:
                        bytes_read = f.read(BUFFER_SIZE)
                        if not bytes_read:
                            break
                        clientSocket.sendall(bytes_read)
                clientSocket.send(b'DONE')
                print("File uploaded successfully")
            except FileNotFoundError:
                print("File not found locally")

        elif command.upper() == "RETR":
            clientSocket.send(f"{command}|{filename}".encode())
            with open(filename, 'wb') as f:
                while True:
                    bytes_read = clientSocket.recv(BUFFER_SIZE)
                    if bytes_read == b'DONE':
                        print("File downloaded successfully")
                        break
                    f.write(bytes_read)

        else:
            print("Unknown command")

    clientSocket.close()

if __name__ == "__main__":
    tcp_client()
