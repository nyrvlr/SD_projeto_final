import socket
import json
import os

class Client:
    def __init__(self, manager_host, manager_port):
        self.manager_host = manager_host
        self.manager_port = manager_port

    def backup_file(self, filename):
        with open(filename, 'rb') as f:
            filedata = f.read().decode()
        
        # Contact manager
        manager_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        manager_socket.connect((self.manager_host, self.manager_port))
        manager_socket.send(filename.encode())
        
        response = manager_socket.recv(1024)
        server_info = json.loads(response.decode())
        manager_socket.close()
        
        # Send file to primary server
        primary_info = server_info['primary']
        primary_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        primary_socket.connect((primary_info['host'], primary_info['port']))
        request = {'filename': filename, 'filedata': filedata, 'replica': server_info['replica']}
        primary_socket.send(json.dumps(request).encode())
        primary_socket.close()

if __name__ == "__main__":
    client = Client('localhost', 5000)
    client.backup_file('example.txt')
