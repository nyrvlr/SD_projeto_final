import socket
import os
import hashlib
import threading

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.storage_dir = f"server_storage_{port}"
        os.makedirs(self.storage_dir, exist_ok=True)
    
    def store_file(self, file_name, data):
        file_path = os.path.join(self.storage_dir, file_name)
        with open(file_path, 'wb') as file:
            file.write(data)
    
    def verify_integrity(self, file_name, received_checksum):
        file_path = os.path.join(self.storage_dir, file_name)
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as file:
            buf = file.read()
            hasher.update(buf)
        return hasher.hexdigest() == received_checksum
    
    def replicate_file(self, file_name, target_address):
        try:
            file_path = os.path.join(self.storage_dir, file_name)
            with open(file_path, 'rb') as file:
                data = file.read()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as replica_socket:
                replica_socket.connect(target_address)
                replica_socket.send(f"STORE {file_name}".encode())
                replica_socket.send(data)
                checksum = hashlib.sha256(data).hexdigest()
                replica_socket.send(checksum.encode())
        except Exception as e:
            print(f"Error replicating file: {e}")

    def handle_client(self, client_socket):
        try:
            message = client_socket.recv(1024).decode()
            if message.startswith("STORE"):
                file_name = message.split()[1]
                data = client_socket.recv(1024)
                self.store_file(file_name, data)
                
                checksum = hashlib.sha256(data).hexdigest()
                client_socket.send("STORED".encode())
                
                if client_socket.recv(1024).decode().startswith("REPLICATE"):
                    replica_server = client_socket.recv(1024).decode()
                    replica_host, replica_port = replica_server.split(':')
                    self.replicate_file(file_name, (replica_host, int(replica_port)))
        except Exception as e:
            print(f"Error handling client request: {e}")

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server running on {self.host}:{self.port}...")
        
        while True:
            client_socket, _ = server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

# Inicia o servidor
server = Server('localhost', 8001)
server.run()
