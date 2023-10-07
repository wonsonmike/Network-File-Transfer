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
    # Tell the server to list files
    command = "list"
    client_socket.sendall(command.encode("utf-8")) 

    # Get the list of files from the server and display them
    response = client_socket.recv(4096).decode("utf-8").strip()
    print("List of files in the directory:")
    print(response)

def download_file(client_socket):
    # Tell the server I want to download a file
    command = "get"
    client_socket.sendall(command.encode("utf-8"))

    # List the files to choose from
    filenames = client_socket.recv(4096).decode("utf-8").strip()
    print("List of files in the directory:")
    print(filenames)

    # Get the filename from the user and send it to server
    filename = input("Enter the filename to download a file: ")
    client_socket.sendall(filename.encode("utf-8")) 
    
    # Check if the filename is valid with the server
    check = client_socket.recv(1024).decode("utf-8")

    # If the filename is valid, get the file data (or error message)
    if "Proceed" in check:
        print(check)
        response = b""
        while True: # Loop until response has all data from the file
            data = client_socket.recv(4096)
            if not data:
                break
            elif b"===EOF===" in data:
                response += data.replace(b"===EOF===", b"")
                break
            elif b"File not found." in data:
                response += data
                break
            else:
                response += data

        # If it's an error, display it. Otherwise, save the file in the files folder
        if b"File not found." in response:
            print(response.decode("utf-8"))
        else:
            with open("files/"+filename, 'wb') as file:
                file.write(response)
            print("File successfully downloaded to the files folder.")
    else: # Filename is not valid
        print(check)

def upload_file(client_socket):
    # Tell the server I want to upload a file
    command = "send"
    client_socket.sendall(command.encode("utf-8")) 

    # List the files from the uploading folder
    print("Select from the following files to upload: ")
    files = os.listdir('uploading')
    file_list = '\n'.join(files)
    print(file_list)

    # Choose a file to upload and send the filename
    filename = input("Enter the filename for upload: ")
    while filename not in files:
        filename = input("File not found. Enter the filename for upload: ")
    client_socket.sendall(filename.encode("utf-8"))

    # Upload the file, or the error message
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

def delete_file(client_socket):
    # Tell the server I want to delete a file
    command = "delete"
    client_socket.sendall(command.encode("utf-8"))

    # List the files available to be deleted 
    filenames = client_socket.recv(4096).decode("utf-8").strip()
    print("List of files in the directory:")
    print(filenames)

    # Get the filename from the user and send it to server
    filename = input("Enter the filename to download a file: ")
    client_socket.sendall(filename.encode("utf-8")) 

    # Verify that the filename is valid from the server
    verify = client_socket.recv(1024).decode("utf-8")
    print(verify)

def connect_to_server(server_host, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the client, and confirm connection to the user
        client_socket.connect((server_host, server_port))
        print(client_socket.recv(1024).decode("utf-8"))  # Welcome message

        # Get the next option from the user
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
                delete_file(client_socket)
            elif next == "c":
                pass
            else:
                print("Command not accepted. Try again.")

        # Close connection with the server
        command = "close"
        client_socket.sendall(command.encode("utf-8")) 


if __name__ == "__main__":
    # Connect to the server
    server_host, server_port = "192.168.8.135", 2222
    connect_to_server(server_host, server_port)
