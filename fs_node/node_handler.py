import socket
import json
from datetime import datetime
import os

def get_file_info(directory):
    """Gerar a lista de informações dos arquivos para registro."""
    files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            filepath = os.path.join(directory, filename)
            files.append({
                "filename": filename,
                "filesize": os.path.getsize(filepath),
                "filehash": "hash_placeholder"  # Substitua com o cálculo de hash real
            })
    return files

def send_request_to_tracker(tracker_address, request_data):
    """Envia uma requisição para o FS_Tracker e recebe a resposta."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(tracker_address)
        s.sendall(json.dumps(request_data).encode('utf-8'))
        response = s.recv(1024)
    return json.loads(response.decode('utf-8'))

def register_node(tracker_address, node_id, node_address, directory):
    """Registra o nó no FS_Tracker com a lista de arquivos."""
    files = get_file_info(directory)
    request_data = {
        "action": "register",
        "node_id": node_id,
        "node_address": node_address,
        "files": files,
        "timestamp": datetime.now().isoformat()
    }
    return send_request_to_tracker(tracker_address, request_data)

def update_node_info(tracker_address, node_id, node_address, directory):
    """Atualiza as informações do nó no FS_Tracker."""
    files = get_file_info(directory)
    request_data = {
        "action": "update",
        "node_id": node_id,
        "node_address": node_address,
        "files": files,
        "timestamp": datetime.now().isoformat()
    }
    return send_request_to_tracker(tracker_address, request_data)

def query_file_location(tracker_address, node_id, file_name):
    """Consulta a localização de um arquivo no FS_Tracker."""
    request_data = {
        "action": "query",
        "node_id": node_id,
        "filename": file_name,
        "timestamp": datetime.now().isoformat()
    }
    return send_request_to_tracker(tracker_address, request_data)
