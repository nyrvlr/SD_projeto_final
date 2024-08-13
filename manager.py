import socket
import json

class Gerenciador:
    def __init__(self, port):
        self.port = port
        self.servidores = []
        self.server_ip = '127.0.0.1'  # IP fixo dos servidores

    def start(self):
        self._configurar_servidores()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', self.port))
            s.listen()
            print(f'Gerenciador iniciado na porta {self.port}...')
            while True:
                conn, addr = s.accept()
                self.handle_client(conn)

    def _configurar_servidores(self):
        num_servidores = int(input('Quantos servidores existem? '))
        for _ in range(num_servidores):
            port = int(input('Digite a porta do servidor: '))
            capacity = int(input('Digite a capacidade do servidor (em bytes): '))
            self.servidores.append({'host': self.server_ip, 'port': port, 'capacity': capacity, 'used_space': 0})

    def handle_client(self, conn):
        with conn:
            arquivo = conn.recv(1024).decode()
            print(f'Requisição de backup recebida para o arquivo: {arquivo}')
            
            principal, replica = self.escolher_servidores()
            resposta = json.dumps({'principal': principal, 'replica': replica})
            
            conn.sendall(resposta.encode())
            print(f'Enviado ao cliente: {resposta}')

    def escolher_servidores(self):
        # Ordena servidores por capacidade disponível (capacidade - espaço usado), em ordem decrescente
        sorted_servers = sorted(self.servidores, key=lambda s: s['capacity'] - s['used_space'], reverse=True)
        
        if len(sorted_servers) < 2:
            raise Exception("Não há servidores suficientes para armazenar e replicar o arquivo.")
        
        principal = sorted_servers[0]
        replica = sorted_servers[1]
        
        return f"{principal['host']}:{principal['port']}", f"{replica['host']}:{replica['port']}"

if __name__ == '__main__':
    gerenciador = Gerenciador(5000)
    gerenciador.start()
