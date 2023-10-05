import socketserver

class SFTPServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.sendall(b"Welcome to the Simple File Sharing Server!\n")
        
        while True:
            self.request.sendall(b"Enter 'get filename' to download a file: ")
            data = self.request.recv(1024).decode("utf-8").strip()
            
            if not data:
                break
            
            command, filename = data.split(maxsplit=1)
            
            if command == 'get':
                self.send_file(filename)
            else:
                self.request.sendall(b"Invalid command. Use 'get filename'.\n")
        
        self.request.close()

    def send_file(self, filename):
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
