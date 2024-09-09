import socket
import os

class Cliente:
    def __init__(self, gerenciador_host, gerenciador_port): ## conexão com o servidor
        self.gerenciador_host = gerenciador_host
        self.gerenciador_port = gerenciador_port

    def enviar_arquivo(self, filename):
        if os.path.exists(filename):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.gerenciador_host, self.gerenciador_port))
                s.sendall(filename.encode())
                resposta = s.recv(1024).decode()
                servidor_principal, servidor_replica = resposta.split('::')

                # Enviar para o servidor principal
                self.enviar_para_servidor(servidor_principal, filename)

                # Enviar para o servidor de réplica
                self.enviar_para_servidor(servidor_replica, filename)
        else:
            print('Arquivo não encontrado.')

    def enviar_para_servidor(self, servidor, filename): ## envio do arquivo em pacotes 
        host, port = servidor.split(':')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, int(port)))
            s.sendall(filename.encode())  # Enviar o nome do arquivo
            s.recv(1024)  # Aguardar confirmação

            with open(filename, 'rb') as f: ## abre o arquivo em modo binário para leitura
                while (chunk := f.read(1024)):  # lê e envia o arquivo em pacotes de 1024 bytes
                    s.sendall(chunk)
            print(f'Arquivo {filename} enviado para {host}:{port}.')

if __name__ == '__main__':
    cliente = Cliente('127.0.0.1', 5000)  # IP e porta do gerenciador
    filename = input('Digite o nome do arquivo para backup: ')
    cliente.enviar_arquivo(filename)
