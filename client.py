import socket

def showOptions():
    print("Here are your options.")
    print("1) Download a file")
    print("2) Upload a file")
    print("3) Delete a file")
    print("c) Close")
    return "->"

def download_file(client_socket):
    print(client_socket.recv(1024).decode("utf-8")) # Give options

    filename = input(">")  # Get with the desired filename from the user
    command = f"get {filename}"
    client_socket.sendall(command.encode("utf-8"))
    
    response = client_socket.recv(1024).decode("utf-8").strip()
    if response == "Invalid command. Use 'get filename'.":
        print(response)
    elif response == "File not found.":
        print(response)
    else:
        with open(filename, 'wb') as file:
            file.write(response.encode())

def connect_to_server(server_host, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        #Connect to the client, and confirm connection to the user
        client_socket.connect((server_host, server_port))
        print(client_socket.recv(1024).decode("utf-8"))  # Welcome message


        next = ""
        while (next != "c"):
            next = input(showOptions())
            if next == "1":
                download_file(client_socket)
            elif next == "2":
                print("Upload")
            elif next == "3":
                print("Delete")
            elif next == "c":
                pass
            else:
                print("Command not accepted. Try again.")


if __name__ == "__main__":
    server_host, server_port = "192.168.8.135", 2222
    connect_to_server(server_host, server_port)
