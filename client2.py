import socket
import os

class Client:
    def __init__(self, manager_address):
        self.manager_address = manager_address
        self.root_dir = "client_files"
        os.makedirs(self.root_dir, exist_ok=True)
    
    def backup_file(self, file_name):
        file_path = os.path.join(self.root_dir, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                data = file.read()
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect(self.manager_address)
                client_socket.send(file_name.encode())
                client_socket.send(data)
        else:
            print("File does not exist.")

    def run(self):
        while True:
            file_name = input("Enter the file name to backup: ")
            self.backup_file(file_name)

# Inicia o cliente
client = Client(('localhost', 9000))
client.run()
