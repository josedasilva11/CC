import socket
import json
from datetime import datetime
import os
import hashlib

# Função para calcular o hash SHA-256 de um arquivo
def get_file_hash(filepath):

#    Calcula o hash SHA-256 de um arquivo.
#
#    Args:
#        filepath (str): O caminho para o arquivo.
#
#    Returns:
#        str: O hash SHA-256 do arquivo.

    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Função para registrar as informações do nó com o tracker
def register_with_tracker(tracker_address, node_info):
 
#    Registra as informações do nó com o tracker.
#
#    Args:
#        tracker_address (tuple): Uma tupla contendo o endereço IP e a porta do tracker.
#        node_info (dict): Um dicionário contendo informações sobre o nó.
#
#    Returns:
#        dict: Um dicionário com a resposta do tracker.
 
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(tracker_address)
            message = json.dumps(node_info).encode('utf-8')
            s.sendall(message)
            data = s.recv(1024)
        return json.loads(data.decode('utf-8'))
    except socket.error as e:
        return {'status': 'error', 'message': str(e)}

if __name__ == "__main__":
    tracker_address = ('localhost', 9090)  # Endereço e porta do tracker
    node_address = "seu_endereco_ip:porta"  # Substitua pelo seu endereço IP e porta
    node_id = hashlib.sha256(node_address.encode('utf-8')).hexdigest()
    files_directory = 'files'

    # Informações sobre o nó
    node_info = {
        "action": "register",
        "node_id": node_id,
        "node_address": node_address,
        "timestamp": datetime.now().isoformat() + 'Z'
    }

    # Registrar o nó com o tracker
    response = register_with_tracker(tracker_address, node_info)

    # Verificar a resposta do tracker e imprimir uma mensagem de sucesso ou falha
    if response['status'] == 'success':
        print(f"Conectado com sucesso! ID do nó: {node_id}")
    else:
        print(f"Falha na conexão: {response['message']}")
