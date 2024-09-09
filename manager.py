import socket

class Gerenciador:
    def __init__(self, port, servidores): ## armazena a porta e uma lista de servidores
        self.port = port
        self.servidores = servidores

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: ##cria o socket
            s.bind(('0.0.0.0', self.port)) ## associa à porta
            s.listen() ## deixa pronto pra receber conexões
            print(f'Gerenciador iniciado na porta {self.port}...') 
            while True:
                conn, addr = s.accept() ## aguarda e retorna uma conexão nova (conn) e envia o endereço do cliente
                self.handle_client(conn) ## envia a conexão para o handle_client

    def handle_client(self, conn):
        with conn:
            # Recebe o nome do arquivo
            arquivo = conn.recv(1024).decode()
            print(f'Requisição de backup recebida para o arquivo: {arquivo}')
            
            # Escolhe servidores com base no espaço disponível
            principal, replica = self.escolher_servidores()
            resposta = f'{principal}::{replica}'
            
            # Envia a decisão para o cliente contendo o endereço dos servidores escolhidos
            conn.sendall(resposta.encode())
            print(f'Enviado ao cliente: {resposta}')

    def escolher_servidores(self):
        # Obtém o espaço disponível em cada servidor
        server_spaces = [(server, self.get_server_space(server)) for server in self.servidores]  ## pra cada servidor da lista, usa o get_server_space e cria a tupla (servidor, espaço disponivel)
        
        # Ordena os servidores de forma decrescente, de acordo com o espaço disponível
        server_spaces.sort(key=lambda x: x[1], reverse=True)

        # Seleciona os dois servidores com mais espaço
        principal = server_spaces[0][0]
        replica = server_spaces[1][0]
        return principal, replica

    def get_server_space(self, server):
        try:
            host, port = server.split(':') ## separa o endereço IP e a porta do servidor
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, int(port))) ## conecta ao servidor usando o endereço e a porta fornecidos
                s.sendall(b'get_space') ## envia uma solicitação ao servidor pra puxar o espaço disponível 
                response = s.recv(4096) ## recebe a resposta do servidor com o espaço livre em bytes
                return int(response.decode()) ## transforma a resposta em um int
        except Exception as e:
            print(f"Erro ao obter espaço disponível do servidor {server}: {e}")
            return 0 ## retorna 0 em caso de erro

if __name__ == '__main__':
    servidores = ['127.0.0.1:5001', '127.0.0.1:5002']  # Adicione os IPs e portas dos servidores
    gerenciador = Gerenciador(5000, servidores) # cria uma instancia de gerenciador que escuta na porta 5000 e gerencia os servidores listados
    gerenciador.start()
