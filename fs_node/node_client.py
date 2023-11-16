import socket
import json
from datetime import datetime
import os
import hashlib

def get_file_hash(filepath):
    """Calcula o hash SHA-256 de um arquivo."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def get_file_info(directory):
    """Gera a lista de informações dos arquivos para registro."""
    files = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            files.append({
                "filename": filename,
                "filesize": os.path.getsize(filepath),
                "filehash": get_file_hash(filepath)
            })
    return files

def register_with_tracker(tracker_address, node_info):
    """Registra as informações do nodo com o tracker."""
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
    tracker_address = ('localhost', 9090)
    node_id = "seu_node_id"
    node_address = "seu_endereco_ip:porta"
    files_directory = '/caminho/para/sua/pasta/de/arquivos'

    node_info = {
        "action": "register",
        "node_id": node_id,
        "node_address": node_address,
        "files": get_file_info(files_directory), 
        "timestamp": datetime.now().isoformat() + 'Z'
    }

    response = register_with_tracker(tracker_address, node_info)
    print(f"Resposta do Tracker: {response}")
