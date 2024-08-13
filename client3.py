import socket
import os

class Cliente:
    def __init__(self, gerenciador_host, gerenciador_port):
        self.gerenciador_host = gerenciador_host
        self.gerenciador_port = gerenciador_port

    def enviar_arquivo(self, filename):
        if os.path.exists(filename):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.gerenciador_host, self.gerenciador_port))
                s.sendall(filename.encode())
                resposta = s.recv(1024).decode()
                servidor_principal, servidor_replica = resposta.split('::')

                with open(filename, 'r') as f:
                    content = f.read()

                # Enviar para o servidor principal
                self.enviar_para_servidor(servidor_principal, filename, content)

                # Enviar para o servidor de réplica
                self.enviar_para_servidor(servidor_replica, filename, content)
        else:
            print('Arquivo não encontrado.')

    def enviar_para_servidor(self, servidor, filename, content):
        host, port = servidor.split(':')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, int(port)))
            s.sendall(f'{filename}::{content}'.encode())
            print(f'Arquivo {filename} enviado para {host}:{port}.')

if __name__ == '__main__':
    cliente = Cliente('127.0.0.1', 5000)  # IP e porta do gerenciador
    filename = input('Digite o nome do arquivo para backup: ')
    cliente.enviar_arquivo(filename)
