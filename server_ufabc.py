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
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', self.port))
                s.listen()
                print(f'Servidor iniciado na porta {self.port}...')
                while True:
                    conn, addr = s.accept()
                    self.handle_client(conn)
        except Exception as e:
            print(f'Erro ao iniciar o servidor: {e}')

    def handle_client(self, conn):
        try:
            with conn:
                data = conn.recv(1024).decode()
                if data:
                    filename, content = data.split('::', 1)
                    filepath = os.path.join(self.data_dir, filename)
                    if self.store_file(filepath, content):
                        print(f'Arquivo {filename} armazenado em {self.port}.')
                    else:
                        print(f'Erro ao armazenar o arquivo {filename}. Espaço insuficiente.')
        except Exception as e:
            print(f'Erro ao processar a requisição do cliente: {e}')

    def store_file(self, filepath, content):
        try:
            if len(content) + self.used_space <= self.capacity:
                with open(filepath, 'w') as f:
                    f.write(content)
                self.used_space += len(content)
                return True
            return False
        except Exception as e:
            print(f'Erro ao gravar o arquivo {filepath}: {e}')
            return False

    def get_free_space(self):
        return self.capacity - self.used_space

if __name__ == '__main__':
    import sys
    try:
        port = int(sys.argv[1])
        capacity = int(sys.argv[2])
        servidor = Servidor(port, capacity)
        servidor.start()
    except IndexError:
        print("Porta e capacidade devem ser fornecidas como argumentos.")
    except ValueError:
        print("Porta e capacidade devem ser números inteiros.")
