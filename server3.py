import socket
import os

class Servidor:
    def __init__(self, port):
        self.port = port
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
            data = conn.recv(1024)
            if data:
                filename, content = data.decode().split('::', 1)
                filepath = os.path.join(self.data_dir, filename)
                with open(filepath, 'w') as f:
                    f.write(content)
                print(f'Arquivo {filename} recebido e armazenado.')

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
    servidor = Servidor(port)
    servidor.start()
