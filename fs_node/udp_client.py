import socket
import json
import os
import hashlib
import time
from node_handler import query_file_location
from node_handler import send_request_to_tracker

import random
import threading


# Configurações globais
BLOCK_SIZE = 4096  # Tamanho do bloco em bytes (aqui, 4KB)
MAX_RETRIES = 5    # Número máximo de tentativas de retransmissão para cada bloco

def calculate_block_hash(data):
    # Calcula o hash SHA-256 de um bloco de dados.
    #
    # Args:
    #     data (bytes): Bloco de dados para o qual calcular o hash.
    #
    # Returns:
    #     str: Hash SHA-256 do bloco de dados.
   
    return hashlib.sha256(data).hexdigest()

def send_udp_request(server_name, server_address, request_data):
    # Envia uma requisição UDP e espera pela resposta.
    #
    # Args:
    #     server_address (tuple): Endereço do servidor (host, port).
    #     request_data (dict): Dados a serem enviados ao servidor.
    #
    # Returns:
    #     tuple: Resposta do servidor e um valor de erro, se houver.
   
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
    server_address = (source['address'], source['port'])
    retries = 0
    while retries < MAX_RETRIES:
        request_data = {'action': 'request_block', 'file_name': file_name, 'block_id': block_index}
        response, error = send_udp_request(server_address, request_data)

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

    with open(output_file, 'wb') as file:
        for block_info in file_blocks_info['blocks']:
            block_id = block_info['index']
            expected_checksum = block_info['hash']
            block_data = request_block(file_name, block_id, server_name, server_address)
            if block_data is None:
                print(f"Falha ao baixar o bloco {block_id} do arquivo {file_name}.")
                return
            file.write(block_data)
            
            
def select_sources(file_blocks_info):
    # Esta função pode ser simples (escolha aleatória) ou complexa (baseada em critérios específicos)
    selected_sources = {}
    for block in file_blocks_info['blocks']:
        selected_node = random.choice(block['available_nodes'])
        selected_sources[block['index']] = selected_node
    return selected_sources            

def get_alternative_source(tracker_address, file_name, block_id, excluded_source):
    """
    Obtém uma fonte alternativa para um bloco específico de um arquivo.

    Args:
        tracker_address (tuple): Endereço do FS_Tracker (host, port).
        file_name (str): Nome do arquivo que está sendo baixado.
        block_id (int): ID do bloco que precisa de uma fonte alternativa.
        excluded_source (dict): Fonte a ser excluída da nova busca.

    Returns:
        dict or None: Retorna uma nova fonte se disponível, caso contrário None.
    """
    request_data = {
        "action": "query_alternative_source",
        "filename": file_name,
        "block_id": block_id,
        "excluded_source": excluded_source
    }

    response = send_request_to_tracker(tracker_address, request_data)
    if response and 'status' in response and response['status'] == 'success':
        return response.get('new_source')
    else:
        print("Não foi possível encontrar uma fonte alternativa.")
        return None

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

def request_block(blocks, block_index, file_name, source, expected_checksum):
    retries = 0
    while retries < MAX_RETRIES:
        server_address = (source['address'], source['port'])
        block_data = send_udp_request(file_name, block_index, server_address, expected_checksum)

        if block_data:
            blocks[block_index] = block_data
            return
        else:
            print(f"Retransmissão para o bloco {block_index} falhou. Tentando outra fonte...")
            # Lógica para escolher outra fonte, se disponível.
            new_source = get_alternative_source(file_name, block_index)
            if new_source:
                source = new_source
            else:
                print(f"Não há fontes alternativas disponíveis para o bloco {block_index}.")
                break

        retries += 1


# Exemplo de uso
file_name = 'example.txt'             # Nome do arquivo a ser solicitado
server_address = ('localhost', 9091)  # Endereço do servidor
output_file = 'output_example.txt'    # Arquivo de saída para os dados baixados

request_file(file_name, 'FS_Server', server_address, output_file)