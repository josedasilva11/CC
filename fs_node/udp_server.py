import socket
import json
import threading
import time
import hashlib
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import utilities



BLOCK_SIZE = 4096  # Tamanho do bloco em bytes

# Cria uma estrutura de dados para rastrear as métricas de desempenho
performance_metrics = {}

if len(sys.argv) < 2:
    print("Uso: python udp_server.py /caminho/para/pasta")
    sys.exit(1)

server_directory = sys.argv[1]

def calculate_block_hash(data):
    # Calcula o hash SHA-256 de um bloco de dados, usado para verificar a integridade no lado do cliente.
    #
    # Args:
    #     data (bytes): Dados do bloco para calcular o hash.
    #
    # Returns:
    #     str: Hash SHA-256 dos dados.

    return hashlib.sha256(data).hexdigest()

def get_block_data(file_name, block_id):
    file_path = os.path.join(server_directory, file_name)
    block_data = utilities.get_file_block(file_path, block_id, BLOCK_SIZE)
    return block_data

    

def handle_request(data, addr, udp_socket):
    message = json.loads(data.decode())
    action = message.get('action')
    
    if action == 'request_block':
        file_name = message.get('file_name')
        block_id = message.get('block_id')
        print(f"Bloco solicitado: {block_id} do arquivo {file_name} por {addr}")

        block_data = get_block_data(file_name, block_id)

        if block_data:
            checksum = calculate_block_hash(block_data)
            response = {'status': 'success', 'data': block_data.decode('latin1'), 'checksum': checksum}
            print(f"Enviando bloco {block_id} para {addr}")
        else:
            response = {'status': 'error', 'message': 'Block not found.'}
            print(f"Bloco {block_id} não encontrado para {addr}")

        udp_socket.sendto(json.dumps(response).encode(), addr)


def start_udp_server(address):
    # Inicia o servidor UDP, configurando-o para ouvir solicitações e processá-las em threads separadas para lidar com múltiplas solicitações simultâneas.
    #
    # Args:
    #     address (tuple): Endereço para o servidor ouvir (host, port).

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind(address)
        print(f"Servidor UDP iniciado em {address}")
        while True:
            data, addr = udp_socket.recvfrom(65536)  # Tamanho máximo do datagrama.
            message = json.loads(data.decode())
            message['start_time'] = time.time()  # Registra o tempo de início antes de processar a solicitação
            threading.Thread(target=handle_request, args=(data, addr, udp_socket)).start()

# Exemplo de uso
server_address = ('192.168.1.223', 9091)  # Endereço do servidor
start_udp_server(server_address)
