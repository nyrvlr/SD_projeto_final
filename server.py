import socket
import os

class Servidor:
    def __init__(self, port, capacity):
        self.port = port
        self.capacity = capacity
        self.used_space = 0
        self.data_dir = f'data_{port}'
        os.makedirs(self.data_dir, exist_ok=True)

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', self.port))
            s.listen()
            print(f'Servidor iniciado na porta {self.port}...')
            while True:
                conn, addr = s.accept()
                self.handle_client(conn)

    def handle_client(self, conn):
        with conn:
            data = conn.recv(1024).decode()
            if data:
                filename, content = data.split('::', 1)
                filepath = os.path.join(self.data_dir, filename)
                if self.store_file(filepath, content):
                    print(f'Arquivo {filename} armazenado em {self.port}.')
                else:
                    print(f'Erro ao armazenar o arquivo {filename}. Espaço insuficiente.')

    def store_file(self, filepath, content):
        if len(content) + self.used_space <= self.capacity:
            with open(filepath, 'w') as f:
                f.write(content)
            self.used_space += len(content)
            return True
        return False

    def replicar_arquivo(self, filepath, replica_host, replica_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((replica_host, replica_port))
            with open(filepath, 'r') as f:
                content = f.read()
            filename = os.path.basename(filepath)
            s.sendall(f'{filename}::{content}'.encode())
            print(f'Replicação do arquivo {filename} enviada para {replica_host}:{replica_port}.')

if __name__ == '__main__':
    port = int(input('Digite a porta do servidor: '))
    capacity = int(input('Digite a capacidade do servidor (em bytes): '))
    servidor = Servidor(port, capacity)
    servidor.start()
