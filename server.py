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
            filename = conn.recv(1024).decode()
            filepath = os.path.join(self.data_dir, filename)
            conn.sendall(b'ACK')  # Enviar confirmação de recebimento do nome do arquivo
            
            with open(filepath, 'wb') as f:  # Abre o arquivo em modo binário
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)
                print(f'Arquivo {filename} recebido e armazenado.')

    def replicar_arquivo(self, filepath, replica_host, replica_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((replica_host, replica_port))
            with open(filepath, 'rb') as f:
                while (chunk := f.read(1024)):
                    s.sendall(chunk)
            print(f'Replicação do arquivo {filepath} enviada para {replica_host}:{replica_port}.')

if __name__ == '__main__':
    port = int(input('Digite a porta do servidor: '))
    servidor = Servidor(port)
    servidor.start()