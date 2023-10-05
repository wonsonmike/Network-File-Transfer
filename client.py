import socket

def download_file(filename, server_host, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_host, server_port))
        client_socket.recv(1024)  # Welcome message
        
        command = f"get {filename}"
        client_socket.sendall(command.encode("utf-8"))
        
        response = client_socket.recv(1024).decode("utf-8").strip()
        if response == "Invalid command. Use 'get filename'.":
            print(response)
        else:
            with open(filename, 'wb') as file:
                file.write(response.encode())

if __name__ == "__main__":
    server_host, server_port = "127.0.0.1", 2222
    filename = "sample.txt"  # Replace with the desired filename
    download_file(filename, server_host, server_port)
    print(f"File '{filename}' downloaded successfully.")
