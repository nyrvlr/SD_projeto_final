import socket
import random

class Gerenciador:
    def __init__(self, port, servidores):
        self.port = port
        self.servidores = servidores

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', self.port))
            s.listen()
            print(f'Gerenciador iniciado na porta {self.port}...')
            while True:
                conn, addr = s.accept()
                self.handle_client(conn)

    def handle_client(self, conn):
        with conn:
            # Recebe o nome do arquivo
            arquivo = conn.recv(1024).decode()
            print(f'Requisição de backup recebida para o arquivo: {arquivo}')
            
            # Escolhe servidores
            principal, replica = self.escolher_servidores()
            resposta = f'{principal}::{replica}'
            
            # Envia a decisão para o cliente
            conn.sendall(resposta.encode())
            print(f'Enviado ao cliente: {resposta}')

    def escolher_servidores(self):
        principal = random.choice(self.servidores)
        replica = random.choice([s for s in self.servidores if s != principal])
        return principal, replica

if __name__ == '__main__':
    servidores = ['127.0.0.1:5001', '127.0.0.1:5002']  # Adicione os IPs e portas dos servidores
    gerenciador = Gerenciador(5000, servidores)
    gerenciador.start()
