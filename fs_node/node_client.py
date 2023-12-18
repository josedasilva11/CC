import socket
import json
import sys
import hashlib
import time
import os
from datetime import datetime
from node_handler import query_file_location
from node_handler import send_request_to_tracker

import random
import threading

# Configurações globais
BLOCK_SIZE = 4096  # Tamanho do bloco em bytes (aqui, 4KB)
MAX_RETRIES = 5    # Número máximo de tentativas de retransmissão para cada bloco

def register_with_tracker(tracker_address, node_info):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(tracker_address)
            message = json.dumps(node_info).encode('utf-8')
            s.sendall(message)
            print(f"Registrando no tracker com informações: {node_info}")
            data = s.recv(1024)
        response = json.loads(data.decode('utf-8'))
        print(f"Resposta do tracker: {response}")
        return response
    except socket.error as e:
        return {'status': 'error', 'message': str(e)}

def calculate_block_hash(data):
    # Calcula o hash SHA-256 de um bloco de dados.
    return hashlib.sha256(data).hexdigest()

def send_udp_request(server_name, server_address, request_data):
    # Envia uma requisição UDP e espera pela resposta.
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.settimeout(5)
        try:
            request_data['server_name'] = server_name
            udp_socket.sendto(json.dumps(request_data).encode(), server_address)
            response, _ = udp_socket.recvfrom(4096)
            return json.loads(response.decode()), None
        except socket.timeout:
            return None, "Timeout"
        except Exception as e:
            return None, str(e)

def request_block(blocks, block_index, file_name, source, expected_checksum):
    retries = 0
    while retries < MAX_RETRIES:
        server_address = (source['address'], source['port'])
        request_data = {'action': 'request_block', 'file_name': file_name, 'block_id': block_index}
        response, error = send_udp_request('FS_Server', server_address, request_data)

        if response and 'data' in response:
            block_data = response['data'].encode('latin1')
            block_hash = calculate_block_hash(block_data)

            if block_hash == expected_checksum:
                blocks[block_index] = block_data
                return
            else:
                print(f"Erro de integridade no bloco {block_index}. Tentando novamente...")

        retries += 1
        time.sleep(1)

    print(f"Não foi possível obter o bloco {block_index} após {MAX_RETRIES} tentativas.")
    blocks[block_index] = None

def request_file(file_name, server_name, server_address, output_file):
    file_blocks_info = query_file_location(server_address, server_name, file_name)
    if 'blocks' not in file_blocks_info:
        print("Erro ao obter informações do arquivo do FS_Tracker.")
        return

    blocks = {}
    threads = []

    for block_info in file_blocks_info['blocks']:
        block_index = block_info['index']
        expected_checksum = block_info['hash']
        source = {'address': server_address[0], 'port': server_address[1]}  # Exemplo de fonte

        thread = threading.Thread(target=request_block, args=(blocks, block_index, file_name, source, expected_checksum))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    with open(output_file, 'wb') as file:
        for i in range(len(file_blocks_info['blocks'])):
            if blocks[i]:
                file.write(blocks[i])
            else:
                print(f"Falha ao reconstruir o arquivo: Bloco {i} está faltando.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python node_client.py [caminho do diretório compartilhado]")
        sys.exit(1)

    shared_directory = sys.argv[1]
    tracker_address = ('localhost', 9091)  # Endereço e porta do tracker
    node_name = "Node1"  # Nome deste nodo

    node_info = {
        "action": "register",
        "node_name": node_name,
        "node_address": "seu_endereco_ip:porta",
        "files_directory": shared_directory,
        "timestamp": datetime.now().isoformat() + 'Z'
    }
    response = register_with_tracker(tracker_address, node_info)

    # Verificar a resposta do tracker e imprimir uma mensagem de sucesso ou falha
    if response['status'] == 'success':
        print(f"Conectado com sucesso! Nome do nó: {node_name}")

# Exemplo de uso
file_name = 'examplo.txt'
server_address = ('localhost', 9090)
output_file = 'output_example.txt'

request_file(file_name, 'FS_Server', server_address, output_file)
