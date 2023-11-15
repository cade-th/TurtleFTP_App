import socket

BUFFER_SIZE = 1024  # Size of chunks (1 KB)

# Global variable for the server socket
serverSocket = None

def socket_create():
    global serverSocket
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print(f"Error creating socket: {msg}")

def socket_bind(ip='0.0.0.0', port=8000):
    global serverSocket
    try:
        print(f"Binding socket to port: {port}")
        serverSocket.bind((ip, port))
    except socket.error as msg:
        print(f"Error binding socket to port: {msg}")

def tcp_server():
    global serverSocket

    socket_create()
    socket_bind()

    serverSocket.listen(1)
    while True:
        try:
            print("********************************")
            print("Waiting for client...")
            connectionSocket, addr = serverSocket.accept()
            print("Connected to client -> IP: " + addr[0] + "| Port: " + str(addr[1]))

            raw_packet = connectionSocket.recv(1024)
            message = raw_packet.decode('utf-8')
            packet = message.split('|')

            if packet[0] == "SEND":
                # Implement file upload
                file_name = packet[1]
                with open(file_name, 'wb') as f:
                    while True:
                        bytes_read = connectionSocket.recv(BUFFER_SIZE)
                        if bytes_read == b'DONE':
                            break
                        f.write(bytes_read)

            elif packet[0] == "RETR":
                file_name = packet[1]
                try:
                    with open(file_name, "rb") as f:
                        while True:
                            bytes_read = f.read(BUFFER_SIZE)
                            if not bytes_read:
                                break
                            connectionSocket.sendall(bytes_read)
                    connectionSocket.send(b'DONE')
                except FileNotFoundError as e:
                    print(str(e))
                    connectionSocket.send(b'File not found')

            connectionSocket.close()
        except socket.error as msg:
            print(str(msg))

    serverSocket.close()


if __name__ == "__main__":
    tcp_server()
