import socket
import json
import threading

import hashlib

BLOCK_SIZE = 4096  # Tamanho do bloco em bytes

def calculate_block_hash(data):
#    Calcula o hash SHA-256 de um bloco de dados, usado para verificar a integridade no lado do cliente.
#
#    Args:
#        data (bytes): Dados do bloco para calcular o hash.
#
#    Returns:
#        str: Hash SHA-256 dos dados.

    return hashlib.sha256(data).hexdigest()

def get_block_data(file_name, block_id):
#    Lê e retorna um bloco específico de um arquivo. Útil para responder às solicitações de blocos dos clientes.
#
#    Args:
#        file_name (str): Caminho do arquivo.
#        block_id (int): Identificador do bloco a ser lido.
#
#    Returns:
#        tuple: Dados do bloco e uma mensagem de erro, se houver.

    try:
        with open(file_name, 'rb') as file:
            file.seek(block_id * BLOCK_SIZE)  # Posiciona no início do bloco.
            data = file.read(BLOCK_SIZE)  # Lê o bloco de dados.
            return data, None
    except FileNotFoundError:
        return None, f"Arquivo {file_name} não encontrado."
    except IOError as e:
        return None, f"Erro ao ler o arquivo {file_name}: {e}"

def handle_request(data, addr, udp_socket):
#    Manipula a requisição recebida do cliente. Processa as solicitações recebidas dos clientes, lê o bloco solicitado e envia de volta. Responde com erro se o bloco não puder ser lido.
#
#    Args:
#        data (bytes): Dados recebidos.
#        addr (tuple): Endereço do remetente.
#        udp_socket (socket): Socket UDP do servidor.

    message = json.loads(data.decode())
    action = message.get('action')
    
    # Processa a ação de solicitação de bloco.
    if action == 'request_block':
        file_name = message.get('file_name')
        block_id = message.get('block_id')
        server_name = message.get('server_name')  # Nome do servidor solicitado
        block_data, error = get_block_data(file_name, block_id)

        # Prepara a resposta.
        if block_data:
            checksum = calculate_block_hash(block_data)
            response = {'status': 'success', 'data': block_data.decode(), 'checksum': checksum}
        else:
            response = {'status': 'error', 'message': error or 'Erro desconhecido.'}

        # Envia a resposta ao cliente.
        udp_socket.sendto(json.dumps(response).encode(), addr)

def start_udp_server(address):
#    Inicia o servidor UDP, configurando-o para ouvir solicitações e processá-las em threads separadas para lidar com múltiplas solicitações simultâneas.
#
#    Args:
#        address (tuple): Endereço para o servidor ouvir (host, port).

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind(address)
        print(f"Servidor UDP iniciado em {address}")
        while True:
            data, addr = udp_socket.recvfrom(65536)  # Tamanho máximo do datagrama.
            threading.Thread(target=handle_request, args=(data, addr, udp_socket)).start()

# Exemplo de uso
server_address = ('localhost', 9091)  # Endereço do servidor
start_udp_server(server_address)
