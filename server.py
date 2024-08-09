import socket
import threading
import os
import json

class Server:
    def __init__(self, host, port, server_id):
        self.host = host
        self.port = port
        self.server_id = server_id

    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(4096)
            request = json.loads(data.decode())
            filename = request['filename']
            filedata = request['filedata']
            replica_info = request['replica']
            
            # Save the file
            with open(filename, 'wb') as f:
                f.write(filedata.encode())
            
            # Send replica
            self.send_replica(replica_info, filename, filedata)
        finally:
            client_socket.close()

    def send_replica(self, replica_info, filename, filedata):
        replica_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        replica_socket.connect((replica_info['host'], replica_info['port']))
        request = {'filename': filename, 'filedata': filedata}
        replica_socket.send(json.dumps(request).encode())
        replica_socket.close()

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server {self.server_id} started on {self.host}:{self.port}")
        
        while True:
            client_socket, _ = server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    server = Server('localhost', 5001, 'Server1')
    server.start()
