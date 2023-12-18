import socket
import json
import sys
from datetime import datetime
import os


from ..common import utilities


# Função para gerar a lista de informações dos arquivos para registro
def get_file_info(directory):
    
#    Gera a lista de informações dos arquivos para registro.
#
#    Args:
#        directory (str): O diretório contendo os arquivos a serem registrados.
#
#    Returns:
#        list: Uma lista de dicionários contendo informações sobre cada arquivo.
    
    files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            filepath = os.path.join(directory, filename)
            blocks = get_file_blocks(filepath)
            files.append({
                "filename": filename,
                "filesize": os.path.getsize(filepath),
                "blocks": [{"index": i, "hash": block_hash} for i, (block, block_hash) in enumerate(blocks)]
            })
    return files

# Função para enviar uma requisição para o FS_Tracker e receber a resposta
def send_request_to_tracker(tracker_address, request_data):
    
#    Envia uma requisição para o FS_Tracker e recebe a resposta.
#
#    Args:
#        tracker_address (tuple): Uma tupla contendo o endereço IP e a porta do FS_Tracker.
#        request_data (dict): Um dicionário contendo os dados da requisição.
#
#    Returns:
#        dict: Um dicionário com a resposta do FS_Tracker.

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(tracker_address)
        s.sendall(json.dumps(request_data).encode('utf-8'))
        response = s.recv(1024)
    return json.loads(response.decode('utf-8'))

# Função para registrar o nó no FS_Tracker com a lista de arquivos
def register_node(tracker_address, node_name, node_address, directory):

#    Registra o nó no FS_Tracker com a lista de arquivos.
#
#    Args:
#        tracker_address (tuple): Uma tupla contendo o endereço IP e a porta do FS_Tracker.
#        node_id (str): O ID único do nó.
#        node_address (str): O endereço do nó.
#        directory (str): O diretório contendo os arquivos do nó.
#
#    Returns:
#        dict: Um dicionário com a resposta do FS_Tracker.

    files = get_file_info(directory)
    request_data = {
        "action": "register",
        "node_name": node_name,
        "node_address": node_address,
        "files": files,
        "timestamp": datetime.now().isoformat()
    }
    return send_request_to_tracker(tracker_address, request_data)

# Função para atualizar as informações do nó no FS_Tracker
def update_node_info(tracker_address, node_name, node_address, directory):

#    Atualiza as informações do nó no FS_Tracker.
#
#    Args:
#        tracker_address (tuple): Uma tupla contendo o endereço IP e a porta do FS_Tracker.
#        node_id (str): O ID único do nó.
#        node_address (str): O endereço do nó.
#        directory (str): O diretório contendo os arquivos do nó.
#
#    Returns:
#        dict: Um dicionário com a resposta do FS_Tracker.

    files = get_file_info(directory)
    request_data = {
        "action": "update",
        "node_name": node_name,
        "node_address": node_address,
        "files": files,
        "timestamp": datetime.now().isoformat()
    }
    return send_request_to_tracker(tracker_address, request_data)

# Função para consultar a localização de um arquivo no FS_Tracker
def query_file_location(tracker_address, node_name, file_name):
    
#    Consulta a localização de um arquivo no FS_Tracker.
#
#    Args:
#        tracker_address (tuple): Uma tupla contendo o endereço IP e a porta do FS_Tracker.
#        node_id (str): O ID único do nó.
#        file_name (str): O nome do arquivo a ser consultado.
#
#    Returns:
#        dict: Um dicionário com a resposta do FS_Tracker.

    request_data = {
        "action": "query",
        "node_name": node_name,
        "filename": file_name,
        "timestamp": datetime.now().isoformat()
    }
    return send_request_to_tracker(tracker_address, request_data)
