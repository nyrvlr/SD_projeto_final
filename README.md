# 1. Introdução
Este documento descreve a implementação de um sistema de backup distribuído, implementado em Python, como parte da disciplina de Sistemas Distribuídos. O objetivo desse sistema é realizar o backup de arquivos de forma eficiente, com suporte para replicação, a fim de garantir a integridade dos dados. Esse sistema foi projetado para operar em um ambiente distribuído, sendo composto por três elementos principais: um Gerenciador (Manager), um ou mais Servidores (Servers), e um ou mais Clientes (Clients). Cada elemento do sistema é tratado como um componente distribuído independente, com comunicação estabelecida via sockets TCP. Essa arquitetura garante que os dados estejam protegidos contra falhas individuais dos servidores.
# 2. Arquitetura do Sistema
## 2.1. Gerenciador (Manager)
O Gerenciador é responsável por coordenar as operações de backup no sistema. Ele decide qual servidor será o principal responsável pelo armazenamento de um arquivo e qual servidor será o responsável por armazenar a réplica do arquivo.
## 2.2. Servidores (Servers)
Os Servidores são responsáveis por armazenar os arquivos recebidos dos Clientes. Um servidor também pode ser responsável por replicar arquivos para outros servidores, conforme instruído pelo Gerenciador. Recebem os arquivos em pedaços menores e o reconstroem para garantir que eles não sejam corrompidos.
## 2.3. Clientes (Clients)
Os Clientes são responsáveis por iniciar a operação de backup. Eles enviam os arquivos para o Gerenciador, que então coordena o processo de armazenamento e replicação dos arquivos. Enviam os arquivos em pedaços menores para garantir que eles não sejam corrompidos.
# 3. Implementação
## 3.1. Estrutura do Diretório
O projeto está organizado da seguinte forma:
### servidor:
SD
/servidor
/server.py
### gerenciador:
SD
/gerenciador
/manager.py
### cliente:
SD
/cliente
/client.py
## 3.2. Gerenciador (Manager)
O `manager.py` implementa o Gerenciador, que coordena as operações de backup. Ele
escolhe servidores e, em seguida, instrui o servidor principal a armazenar o arquivo e a enviar uma réplica para outro servidor.
### Execução:
python3 manager.py
## 3.3. Servidores (Servers)
Cada servidor é representado pelo script `server.py`, que é colocado em diferentes diretórios (`/data_5001/`, `/data_5002/`, etc.). Cada servidor pode armazenar arquivos e replicá-los para outros servidores.
### Execução:
python3 server.py
## 3.4. Cliente (Client)
O `client.py` permite que os usuários escolham arquivos para backup, que são então
enviados ao Gerenciador para processamento.
### Execução:
python3 client.py
# 4. Procedimento para Testes
## 4.1. Preparação
  1. Navegue até o diretório raiz do projeto `SD/`.
  2. Em terminais separados, inicie os servidores:
    cd ../servidor
    python3 server.py
    cd ../servidor
    python3 server.py
    Será solicitada a porta de cada um dos servidores. Exemplo para execução: 5001 e 5002
  3. Inicie o Gerenciador:
    cd ../gerenciador
    python3 manager.py
    Aparecerá a seguinte mensagem: Gerenciador iniciado na porta 5000...
  4. Inicie o Cliente:
    cd ../cliente
    python3 client.py
    Será solicitado o nome do arquivo para backup. Insira junto com a extensão (exemplo: teste.txt). Esse arquivo precisa estar dentro da pasta cliente
  5. O sistema irá automaticamente gerenciar o armazenamento e replicação do arquivo.
  6. Verifique se os arquivos foram corretamente armazenados nos diretórios dos servidores.
# 5. Considerações Finais
Este sistema de backup distribuído foi desenvolvido para ser simples e modular, garantindo a transparência de distribuição e a capacidade de lidar com arquivos de tamanhos variados. A estrutura modular permite a fácil extensão do sistema para incluir mais servidores ou adicionar funcionalidades, como criptografia ou compressão de arquivos.
