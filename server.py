import socketserver
import os

class SFTPServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.sendall(b"Welcome to the Simple File Sharing Server!\n")
        
        while True:
            command = self.request.recv(1024).decode("utf-8")

            if command == 'get': # Client wants to download a file
                self.send_file()

            elif command == "list": # Clent wants to list the files
                self.list_files()
                
            else:
                self.request.sendall(b"Invalid command.\n")
        
        self.request.close()

    def list_files(self):
        files = os.listdir('.')
        file_list = '\n'.join(files)
        self.request.sendall(file_list.encode("utf-8"))

    def send_file(self):
        self.request.sendall(b"Enter the filename to download a file: ")
        filename = self.request.recv(1024).decode("utf-8").strip()

        try:
            with open(filename, 'rb') as file:
                data = file.read()
                self.request.sendall(data)
        except FileNotFoundError:
            self.request.sendall(b"File not found.\n")

if __name__ == "__main__":
    host, port = "192.168.8.135", 2222
    server = socketserver.TCPServer((host, port), SFTPServerHandler)
    print(f"SFTP server is running on {host}:{port}")
    server.serve_forever()
