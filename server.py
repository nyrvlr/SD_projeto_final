import socket
import os
import shutil

class Servidor:
    def __init__(self, port): ## armazena o numero da porta, define o nome do diretório e cria
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
            request = conn.recv(1024).decode() ## recebe a mensagem de um cliente
            if request == 'get_space': ## verifica se é uma solicitação de espaço disponível
                self.send_available_space(conn) ## retorna com o espaço disponível
            else:
                self.receive_file(conn, request) ## retorna com o nome do arquivo

    def receive_file(self, conn, filename):
        filepath = os.path.join(self.data_dir, filename) ## define o caminho onde o arquivo será armazenado
        conn.sendall(b'ACK')  # Enviar confirmação de recebimento do nome do arquivo

        with open(filepath, 'wb') as f:  # Abre o arquivo para escrita em modo binário
            while True:
                data = conn.recv(1024) ## recebe os dados do arquivo em pedaços de 1024 bytes
                if not data:
                    break
                f.write(data) ## escreve os dados recebidos no arquivo 
            print(f'Arquivo {filename} recebido e armazenado.')

    def send_available_space(self, conn):
        total, used, free = shutil.disk_usage(self.data_dir) ## puxa o espaço total, usado e livre do diretório de armazenamento
        conn.sendall(str(free).encode()) ## envia o espaço livre ao cliente como uma string codificada em bytes

    def replicar_arquivo(self, filepath, replica_host, replica_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((replica_host, replica_port)) ## conecta ao servidor da replica
            with open(filepath, 'rb') as f: ## abre o arquivo pra leitura em modo binário
                while (chunk := f.read(1024)):
                    s.sendall(chunk)
            print(f'Replicação do arquivo {filepath} enviada para {replica_host}:{replica_port}.')

if __name__ == '__main__':
    port = int(input('Digite a porta do servidor: '))
    servidor = Servidor(port)
    servidor.start()
