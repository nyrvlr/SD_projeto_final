import socket
import threading
import json
import random

class Manager:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.servers = []
        self.lock = threading.Lock()
        
    def register_server(self, server_info):
        with self.lock:
            self.servers.append(server_info)
    
    def choose_servers(self):
        with self.lock:
            if len(self.servers) < 2:
                raise Exception("Not enough servers to perform backup")
            return random.sample(self.servers, 2)
    
    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(1024)
            filename = data.decode()
            primary, replica = self.choose_servers()
            response = json.dumps({'primary': primary, 'replica': replica})
            client_socket.send(response.encode())
        finally:
            client_socket.close()

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Manager started on {self.host}:{self.port}")
        
        while True:
            client_socket, _ = server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    manager = Manager('localhost', 5000)
    manager.start()
