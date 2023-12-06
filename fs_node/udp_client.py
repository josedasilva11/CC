import socket
import json
import os
import hashlib
import time

# Configurações globais
BLOCK_SIZE = 4096  # Tamanho do bloco em bytes (aqui, 4KB)
MAX_RETRIES = 5    # Número máximo de tentativas de retransmissão para cada bloco

def calculate_block_hash(data):
#    Calcula o hash SHA-256 de um bloco de dados.
#
#    Args:
#        data (bytes): Bloco de dados para o qual calcular o hash.
#
#    Returns:
#        str: Hash SHA-256 do bloco de dados.
   
    return hashlib.sha256(data).hexdigest()

def send_udp_request(server_name, server_address, request_data):
#    Envia uma requisição UDP e espera pela resposta.
#
#    Args:
#        server_address (tuple): Endereço do servidor (host, port).
#        request_data (dict): Dados a serem enviados ao servidor.
#
#    Returns:
#        tuple: Resposta do servidor e um valor de erro, se houver.
   
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

def request_block(file_name, block_id, server_name, server_address):
#    Solicita um bloco específico do arquivo ao servidor, com retransmissões se necessário.
#
#    Args:
#        file_name (str): Nome do arquivo a ser solicitado.
#        block_id (int): ID do bloco do arquivo a ser solicitado.
#        server_address (tuple): Endereço do servidor (host, port).
#
#    Returns:
#        bytes: Dados do bloco solicitado ou None se falhar.
   
    retries = 0
    while retries < MAX_RETRIES:
        # Prepara a solicitação de bloco.
        request_data = {'action': 'request_block', 'file_name': file_name, 'block_id': block_id}
        response, error = send_udp_request(server_name, server_address, request_data)

        if response and 'data' in response:
            # Decodifica e verifica a integridade do bloco.
            block_data = response['data'].encode()
            block_hash = calculate_block_hash(block_data)

            if block_hash == response.get('checksum'):
                return block_data
            else:
                print(f"Erro de integridade no bloco {block_id}. Tentando novamente...")
        else:
            print(f"Erro ao solicitar o bloco {block_id}: {error}. Tentando novamente...")

        retries += 1
        time.sleep(1)

    print(f"Não foi possível obter o bloco {block_id} após {MAX_RETRIES} tentativas.")
    return None

def request_file(file_name, server_name, server_address, output_file):
#    Solicita um arquivo inteiro, bloco por bloco, do servidor e o monta localmente.
#
#    Args:
#        file_name (str): Nome do arquivo a ser solicitado.
#        server_address (tuple): Endereço do servidor (host, port).
#        output_file (str): Caminho do arquivo onde os dados serão salvos.

    # Determina o número de blocos necessários para o arquivo.
    file_size = os.path.getsize(file_name)
    num_blocks = (file_size + BLOCK_SIZE - 1) // BLOCK_SIZE


    with open(output_file, 'wb') as file:
        for block_id in range(num_blocks):
            # Solicita cada bloco e escreve no arquivo de saída.
            block_data = request_block(file_name, block_id, server_address)
            if block_data is None:
                print(f"Falha ao baixar o bloco {block_id} do arquivo {file_name}.")
                return
            file.write(block_data)

# Exemplo de uso
file_name = 'example.txt'             # Nome do arquivo a ser solicitado
server_address = ('localhost', 9091)  # Endereço do servidor
output_file = 'output_example.txt'    # Arquivo de saída para os dados baixados

