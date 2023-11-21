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
        "filename": 'files/file1.txt',
        "timestamp": datetime.now().isoformat()
    }
    return send_request_to_tracker(tracker_address, request_data)

def send_file_to_client(tracker_address, node_id, file_name, files_directory):
    """Envia um arquivo do FS_Tracker para um FS_Node."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(tracker_address)
            request_data = {
                "action": "get",
                "node_id": node_id,
                "filename": file_name,
                "timestamp": datetime.now().isoformat()
            }
            s.sendall(json.dumps(request_data).encode('utf-8'))

            # Receber a resposta do tracker
            response = s.recv(1024)
            data = json.loads(response.decode('utf-8'))

            if data.get("status") == "success":
                file_content = data.get("file_content")
                file_path = os.path.join(files_directory, file_name)

                # Escrever o conteúdo do arquivo recebido
                with open(file_path, 'w') as file:
                    file.write(file_content)

                return f"Arquivo {file_name} recebido com sucesso."

            elif data.get("status") == "error":
                return f"Erro: {data.get('message')}"

    except socket.error as e:
        return f"Erro de conexão: {str(e)}"

if __name__ == "__main__":
    tracker_address = ('localhost', 9090)
    node_id = "seu_node_id"
    file_name = "files/file1.txt"  # Substitua pelo nome do arquivo desejado
    files_directory = 'files'

    result = send_file_to_client(tracker_address, node_id, file_name, files_directory)
    print(result)