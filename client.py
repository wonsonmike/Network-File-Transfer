import socket
import os

def showOptions():
    print("\nHere are your options.")
    print("1) List the files")
    print("2) Download a file")
    print("3) Upload a file")
    print("4) Delete a file")
    print("c) Close")
    return "->"

def list_files(client_socket):
    command = "list"
    client_socket.sendall(command.encode("utf-8")) # Tell the server to list files

    response = client_socket.recv(4096).decode("utf-8").strip()
    print("List of files in the directory:")
    print(response)

def download_file(client_socket):
    command = "get"
    client_socket.sendall(command.encode("utf-8")) # Tell the server I want to download a file

    filename = input(client_socket.recv(1024).decode("utf-8")) # Print the filename request
    client_socket.sendall(filename.encode("utf-8")) # Send the filename to the server
    
    response = b""
    while True: # Loop until response has all data from the file
        data = client_socket.recv(4096)
        if not data:
            break
        elif b"===EOF===" in data:
                response += data.replace(b"===EOF===", b"")
                break
        else:
            response += data

    if response == b"File not found.":
        print(response.decode("utf-8"))
    else:
        with open("files/"+filename, 'wb') as file:
            file.write(response)
        print("File successfully downloaded to the files folder.")

def upload_file(client_socket):
    command = "send"
    client_socket.sendall(command.encode("utf-8")) # Tell the server I want to upload a file

    # List the files from the uploading folder
    print("Select from the following files to upload: ")
    files = os.listdir('uploading')
    file_list = '\n'.join(files)
    print(file_list)

    # Choose a file to upload and send the filename
    filename = input("Enter the filename for upload: ")
    client_socket.sendall(filename.encode("utf-8"))

    # Upload the file
    try:
        with open("uploading/"+filename, 'rb') as file:
            data = file.read()
            client_socket.sendall(data)
            client_socket.sendall(b"===EOF===")
    except FileNotFoundError:
        client_socket.sendall(b"Error")

    # Print the response
    response = client_socket.recv(1024).decode("utf-8")
    print(response)

def connect_to_server(server_host, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        #Connect to the client, and confirm connection to the user
        client_socket.connect((server_host, server_port))
        print(client_socket.recv(1024).decode("utf-8"))  # Welcome message


        next = ""
        while (next != "c"):
            next = input(showOptions())
            if next == "1":
                list_files(client_socket)
            elif next == "2":
                download_file(client_socket)
            elif next == "3":
                upload_file(client_socket)
            elif next == "4":
                print("Delete")
            elif next == "c":
                pass
            else:
                print("Command not accepted. Try again.")


if __name__ == "__main__":
    server_host, server_port = "192.168.8.135", 2222
    connect_to_server(server_host, server_port)
