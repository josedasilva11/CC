import socket
import json
import os
import sys
import hashlib
import time
project_root = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.append(project_root)
from fs_node.node_handler import query_file_location


import random
import threading



# Configurações globais
BLOCK_SIZE = 4096  # Tamanho do bloco em bytes (aqui, 4KB)
MAX_RETRIES = 5    # Número máximo de tentativas de retransmissão para cada bloco

def calculate_block_hash(data):
    # Calcula o hash SHA-256 de um bloco de dados.
    return hashlib.sha256(data).hexdigest()

def send_udp_request(server_name, server_address, request_data):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.settimeout(5)
        try:
            request_data['server_name'] = server_name  # Adiciona o nome do servidor ao request
            udp_socket.sendto(json.dumps(request_data).encode(), server_address)
            response, _ = udp_socket.recvfrom(4096)
            return json.loads(response.decode()), None
        except socket.timeout:
            return None, "Timeout"
        except Exception as e:
            return None, str(e)

def request_block(blocks, block_index, file_name, source, expected_checksum):
    print(f"Solicitando bloco {block_index} do arquivo {file_name} de {source}")
    server_address = (source['address'], source['port'])
    retries = 0
    while retries < MAX_RETRIES:
        request_data = {'action': 'request_block', 'file_name': file_name, 'block_id': block_index}
        response, error = send_udp_request('FS_Server', server_address, request_data)

        if response and 'data' in response:
            block_data = response['data'].encode('latin1')
            block_hash = calculate_block_hash(block_data)

            if block_hash == expected_checksum:
                blocks[block_index] = block_data
                print(f"Bloco {block_index} recebido e verificado.")
                return
            else:
                print(f"Erro de integridade no bloco {block_index}. Tentando novamente...")

        retries += 1
        print(f"Erro ao receber bloco {block_index}: {error}")
        time.sleep(1)

    print(f"Não foi possível obter o bloco {block_index} após {MAX_RETRIES} tentativas.")
    blocks[block_index] = None

def request_file(file_name, output_file):
    # Informações do arquivo obtidas do FS_Tracker
    file_info = {
            "texto.txt": {
            "filesize": 1058,
            "blocks": ["687fce6eeba4d004714f4b2f3b237c6619e14f3b687065dcc2dcd79194becebd"]
        }
    }

    servidores = [('localhost', 9091)] 
    # Verifique se o arquivo está na lista
    if file_name not in file_info:
        print(f"Arquivo {file_name} não encontrado.")
        return

    blocks_info = file_info[file_name]["blocks"]
    blocks = [None] * len(blocks_info)

    # Função para solicitar cada bloco
    def request_each_block(block_index):
        for servidor in servidores:
            if blocks[block_index] is None:  # Se o bloco ainda não foi baixado
                source = {'address': servidor[0], 'port': servidor[1]}
                expected_checksum = blocks_info[block_index]
                request_block(blocks, block_index, file_name, source, expected_checksum)

    # Criar threads para baixar cada bloco
    threads = [threading.Thread(target=request_each_block, args=(i,)) for i in range(len(blocks_info))]
    
    # Iniciar todas as threads
    for thread in threads:
        thread.start()
    
    # Aguardar todas as threads terminarem
    for thread in threads:
        thread.join()

    # Escrever os blocos no arquivo de saída
    with open(output_file, 'wb') as file:
        for block_data in blocks:
            if block_data:
                file.write(block_data)
            else:
                print(f"Falha ao baixar um dos blocos do arquivo {file_name}.")
                return

def select_sources(file_blocks_info):
    # Esta função pode ser simples (escolha aleatória) ou complexa (baseada em critérios específicos)
    selected_sources = {}
    for block in file_blocks_info['blocks']:
        selected_node = random.choice(block['available_nodes'])
        selected_sources[block['index']] = selected_node
    return selected_sources

def download_file(file_name, file_blocks_info, output_file):
    selected_sources = select_sources(file_blocks_info)
    blocks = {}
    threads = []

    for block_info in file_blocks_info['blocks']:
        block_index = block_info['index']
        expected_checksum = block_info['hash']
        source = selected_sources[block_index]

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
        print("Uso: python udp_client.py <nome_do_arquivo>")
        sys.exit(1)

    file_name = sys.argv[1]
    output_file = 'output_' + file_name  

    request_file(file_name, output_file)