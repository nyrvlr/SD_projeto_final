import socket
import json

class Gerenciador:
    def __init__(self, port, servidores):
        self.port = port
        self.servidores = servidores  # Lista de dicionários com 'host', 'port' e 'capacity'
        self._initialize_server_capacities()

    def _initialize_server_capacities(self):
        for server in self.servidores:
            server['used_space'] = 0  # Espaço usado inicial

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
            arquivo = conn.recv(1024).decode()
            print(f'Requisição de backup recebida para o arquivo: {arquivo}')
            
            principal, replica = self.escolher_servidores()
            resposta = json.dumps({'principal': principal, 'replica': replica})
            
            conn.sendall(resposta.encode())
            print(f'Enviado ao cliente: {resposta}')

    def escolher_servidores(self):
        sorted_servers = sorted(self.servidores, key=lambda s: s['capacity'] - s['used_space'], reverse=True)
        principal = sorted_servers[0]
        replica = sorted_servers[1] if len(sorted_servers) > 1 else principal
        return f"{principal['host']}:{principal['port']}", f"{replica['host']}:{replica['port']}"

if __name__ == '__main__':
    servidores = [
        {'host': '127.0.0.1', 'port': 5001, 'capacity': 1000},
        {'host': '127.0.0.1', 'port': 5002, 'capacity': 2000}
    ]
    gerenciador = Gerenciador(5000, servidores)
    gerenciador.start()
