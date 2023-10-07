import socketserver
import os

class SFTPServerHandler(socketserver.BaseRequestHandler):
    def handle(self):

        self.request.sendall(b"Welcome to the Simple File Sharing Server!\n")
        
        while True:
            # Get the command from the client
            command = self.request.recv(1024).decode("utf-8")

            if command == 'list': # Client wants to list the files
                self.list_files()

            elif command == "get": # Client wants to download a file
                self.send_file()
                
            elif command == "send": # Client wants to upload a file
                self.get_file()

            elif command == "delete": # Client wants to delete a file
                self.delete_file()

            elif command == "close": # Client wants to close the connection
                break

            else:
                self.request.sendall(b"Invalid command.\n")
        
        self.request.close()

    def list_files(self): # Client wants to list the files
        # Get the list of files from the files folder
        files = os.listdir('files')
        file_list = '\n'.join(files)

        # Send the list of files to the user
        self.request.sendall(file_list.encode("utf-8"))

    def send_file(self): # Client wants to download a file
        # Send a list of the files available to download
        files = os.listdir('files')
        file_list = '\n'.join(files)
        self.request.sendall(file_list.encode("utf-8"))

        # Get the filename from the user
        filename = self.request.recv(1024).decode("utf-8").strip()

        # Check the filename from the user
        if filename in files:
            self.request.sendall(b"File found. Proceed.\n")
        else: 
            self.request.sendall(b"File not found. Try again.\n")
        
        # If the file exists, send the data
        if filename in files:
            try:
                with open("files/"+filename, 'rb') as file:
                    data = file.read()
                    self.request.sendall(data)
                    self.request.sendall(b"===EOF===") # Clarify this is the end of the file
            except FileNotFoundError:
                self.request.sendall(b"File not found.\n")

    def get_file(self): # Client wants to upload a file
        # Get the filename from the client
        filename = self.request.recv(1024).decode("utf-8").strip()

        # Get file data (or error message)
        response = b""
        while True:
            data = self.request.recv(4096)
            if not data:
                break
            elif b"===EOF===" in data: # It's the end of the file
                response += data.replace(b"===EOF===", b"")
                break
            elif b"Error" in data:
                response += data
                break
            else:
                response += data

        # If possible, save the file. Send a message either confirming file upload or error
        if b"Error" in response:
            self.request.sendall(b"File not found. Try again.\n")
        else:
            with open("files/"+filename, 'wb') as file:
                file.write(response)
            self.request.sendall(b"File uploaded successfully.\n")
    def delete_file(self):
        # Send a list of the files available to download
        files = os.listdir('files')
        file_list = '\n'.join(files)
        self.request.sendall(file_list.encode("utf-8"))

        # Get the filename from the user
        filename = self.request.recv(1024).decode("utf-8").strip()

        # Check the filename from the user
        if filename in files:
            self.request.sendall(b"File found. Proceed.\n")
        else: 
            self.request.sendall(b"File not found. Try again.\n")

        # If the file exists, delete it.
        if filename in files:
            os.remove("files/"+filename)
            if filename not in os.listdir("files"):
                self.request.sendall(b"File deleted successfully.")
            else:
                self.request.sendall(b"File not deleted. Try again.")
        

if __name__ == "__main__":
    # Start the server, and verify the host and port of the server
    host, port = "192.168.8.135", 2222
    server = socketserver.TCPServer((host, port), SFTPServerHandler)
    print(f"SFTP server is running on {host}:{port}")
    server.serve_forever()
