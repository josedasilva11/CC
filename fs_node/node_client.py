import socket
import json
from datetime import datetime
import sys
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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python node_client.py [caminho do diretório compartilhado]")
        sys.exit(1)

    shared_directory = sys.argv[1]
    tracker_address = ('localhost', 9090)  # Endereço e porta do tracker
    node_name = "Node1"  # Nome deste nodo

    node_info = {
        "action": "register",
        "node_name": node_name,
        "node_address": "seu_endereco_ip:porta",
        "files_directory": shared_directory,  # Adicione esta linha
        "timestamp": datetime.now().isoformat() + 'Z'
    }
    response = register_with_tracker(tracker_address, node_info)

    # Verificar a resposta do tracker e imprimir uma mensagem de sucesso ou falha
    if response['status'] == 'success':
        print(f"Conectado com sucesso! Nome do nó: {node_name}")
    else:
        print(f"Falha na conexão: {response['message']}")