import socketserver
import os

class SFTPServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.sendall(b"Welcome to the Simple File Sharing Server!\n")
        
        while True:
            command = self.request.recv(1024).decode("utf-8")

            if command == 'list': # Client wants to list the files
                self.list_files()

            elif command == "get": # Clent wants to download a file
                self.send_file()
                
            elif command == "send": # Client wants to upload a file
                self.get_file()

            else:
                self.request.sendall(b"Invalid command.\n")
        
        self.request.close()

    def list_files(self):
        files = os.listdir('files')
        file_list = '\n'.join(files)
        self.request.sendall(file_list.encode("utf-8"))

    def send_file(self):
        self.request.sendall(b"Enter the filename to download a file: ")
        filename = self.request.recv(1024).decode("utf-8").strip()

        try:
            with open("files/"+filename, 'rb') as file:
                data = file.read()
                self.request.sendall(data)
        except FileNotFoundError:
            self.request.sendall(b"File not found.\n")

    def get_file(self):
        try:
            # Get the filename from the client
            filename = self.request.recv(1024).decode("utf-8").strip()
            
            # Save the file
            with open("files/"+filename, 'wb') as file:
                while True:
                    data = self.request.recv(1024)
                    if not data:
                        break
                    file.write(data)
            
            self.request.sendall(b"File uploaded successfully.\n")
        
        except Exception as e:
            self.request.sendall(f"Error: {str(e)}\n".encode("utf-8"))

if __name__ == "__main__":
    host, port = "192.168.8.135", 2222
    server = socketserver.TCPServer((host, port), SFTPServerHandler)
    print(f"SFTP server is running on {host}:{port}")
    server.serve_forever()
