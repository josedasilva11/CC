import socket
import json
import threading
import time
import logging
import hashlib
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual
project_root = os.path.join(script_dir, '..', '..', '..')  # Diretório raiz do projeto
sys.path.append(project_root)

from common import utilities

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

server_running = True
BLOCK_SIZE = 4096  # Tamanho do bloco em bytes

server_directory = os.path.join(os.getcwd(), "server5")

# Certifique-se de que o diretório existe
if not os.path.exists(server_directory):
    logging.error(f"A pasta do servidor não existe: {server_directory}")
    sys.exit(1)
# Funções auxiliares
def calculate_block_hash(data):
    return hashlib.sha256(data).hexdigest()

def get_block_data(file_name, block_id):
    file_path = os.path.join(server_directory, file_name)
    return utilities.get_file_block(file_path, block_id, BLOCK_SIZE)


def register_server_with_tracker(tracker_address, node_name, node_address, files):
    server_info = {
        "action": "register",
        "node_name": node_name,
        "node_address": node_address,
        "files": files
    }
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(tracker_address)
            s.sendall(json.dumps(server_info).encode('utf-8'))
            response = json.loads(s.recv(1024).decode('utf-8'))
            logging.info(f"Resposta do FS_Tracker ao registro: {response}")
    except Exception as e:
        logging.error(f"Erro ao registrar no FS_Tracker: {e}")



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

def check_server_status():
    global server_running
    while server_running:
        # Verifica o estado do servidor a cada 5 segundos
        time.sleep(5)
        if not server_running:
            break
        try:
            # Tente enviar uma solicitação ao servidor para verificar se ele está em execução
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
                udp_socket.settimeout(2)  # Tempo limite de 2 segundos para a resposta
                udp_socket.sendto(b'check', server_address)
                response, _ = udp_socket.recvfrom(1024)
                if response.decode() == 'server_running':
                    logging.info("O servidor está em execução.")
                else:
                    logging.warning("O servidor não está respondendo.")
        except Exception as e:
            logging.error(f"Erro ao verificar o servidor: {str(e)}")

def handle_request(data, addr, udp_socket):
    try:
        # Verifique se os dados não estão vazios
        if not data:
            print(f"Dados vazios recebidos de {addr}")
            response = {'status': 'error', 'message': 'Empty data received.'}
            udp_socket.sendto(json.dumps(response).encode(), addr)
            return

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
    except json.JSONDecodeError:
        # Trate exceção se os dados não puderem ser decodificados como JSON válido
        print(f"Dados inválidos recebidos de {addr}")
        response = {'status': 'error', 'message': 'Invalid data format.'}
        udp_socket.sendto(json.dumps(response).encode(), addr)


def start_udp_server(address):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind(address)
        logging.info(f"Servidor UDP iniciado em {address}")
        print(f"Servidor UDP iniciado em {address}")
        while True:
            data, addr = udp_socket.recvfrom(65536)  # Tamanho máximo do datagrama.
            
            # Verifique se os dados recebidos não estão vazios
            if not data:
                print(f"Nenhum dado recebido de {addr}")
                continue

            try:
                # Tente decodificar os dados como JSON
                message = json.loads(data.decode())
                message['start_time'] = time.time()  # Registra o tempo de início antes de processar a solicitação
                threading.Thread(target=handle_request, args=(data, addr, udp_socket)).start()
            except json.JSONDecodeError:
                print(f"Dados inválidos recebidos de {addr}")
                continue

if __name__ == "__main__":
    node_name = "Server1"  
    node_address = "localhost:9091" 

    # Obter a lista de arquivos do diretório do servidor
    files = utilities.get_file_info(server_directory)

    # Endereço e porta do FS_Tracker
    tracker_address = ('localhost', 9091)

    # Registrar o servidor no FS_Tracker
    register_server_with_tracker(tracker_address, node_name, node_address, files)

    # Iniciar o servidor UDP
    server_address = ('localhost', 9091)
    server_thread = threading.Thread(target=start_udp_server, args=(server_address,))
    server_thread.start()



def stop_server():
    global server_running
    server_running = False
    logging.info("Encerrando o servidor.")


server_address = ('localhost', 9091)  # Endereço do servidor

# Inicia o servidor em uma thread separada
server_thread = threading.Thread(target=start_udp_server, args=(server_address,))
server_thread.start()

# Inicia a verificação do servidor em uma thread separada
status_thread = threading.Thread(target=check_server_status)
status_thread.start()

try:
    while True:
        # Mantém o programa principal em execução
        time.sleep(1)
except KeyboardInterrupt:
    # Captura Ctrl+C para encerrar o servidor
    stop_server()
    server_thread.join()
    status_thread.join()