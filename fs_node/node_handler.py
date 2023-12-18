import socket
import json
import sys
from datetime import datetime
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import utilities

nodes_info = {} 

def get_file_info(directory):
    files = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            blocks = utilities.get_file_blocks(filepath)
            files.append({
                "filename": filename,
                "filesize": os.path.getsize(filepath),
                "blocks": [{"index": i, "hash": block_hash} for i, (block_hash) in enumerate(blocks)]
            })
    return files

def send_request_to_tracker(tracker_address, request_data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Conectando ao FS_Tracker...")
        s.connect(tracker_address)

        print("A enviar solicitação...")
        s.sendall(json.dumps(request_data).encode('utf-8'))
        print("A esperar pela resposta...")
        response = s.recv(1024)
        print("Resposta recebida:", response)
        s.sendall(json.dumps(request_data).encode('utf-8'))
        response = s.recv(1024)
    return json.loads(response.decode('utf-8'))

def register_node(tracker_address, node_name, node_address, directory):
    files = get_file_info(directory)
    request_data = {
        "action": "register",
        "node_name": node_name,
        "node_address": node_address,
        "files": files,
        "timestamp": datetime.now().isoformat()
    }
    print(f"Registo enviado ao tracker: {request_data}")
    response = send_request_to_tracker(tracker_address, request_data)
    print(f"Resposta do tracker: {response}")
    return response

def update_node_info(tracker_address, node_name, node_address, directory):
    files = get_file_info(directory)
    request_data = {
        "action": "update",
        "node_name": node_name,
        "node_address": node_address,
        "files": files,
        "timestamp": datetime.now().isoformat()
    }
    return send_request_to_tracker(tracker_address, request_data)

def query_file_location(tracker_address, node_name, file_name):
    request_data = {
        "action": "query",
        "node_name": node_name,
        "filename": file_name,
        "timestamp": datetime.now().isoformat()
    }
    return send_request_to_tracker(tracker_address, request_data)


def register_files_at_tracker(tracker_address, node_name, node_address, shared_directory):
    files_info = get_file_info(shared_directory)
    request_data = {
        "action": "register",
        "node_name": node_name,
        "node_address": node_address,
        "files": files_info,
        "timestamp": datetime.now().isoformat()
    }
    response = send_request_to_tracker(tracker_address, request_data)
    return response
    

def find_file_location(tracker_address, node_name, file_name):
    request_data = {
        "action": "query",
        "node_name": node_name,
        "filename": file_name,
        "timestamp": datetime.now().isoformat()
    }
    response = send_request_to_tracker(tracker_address, request_data)
    return response

def process_registration_request(request_data):
    node_name = request_data["node_name"]
    node_address = request_data["node_address"]
    files = request_data["files"]
    
    nodes_info[node_name] = {
        "address": node_address,
        "files": files
    }
    
    
def process_query_request(request_data):
    file_name = request_data["filename"]
    nodes_with_file = [
        {"name": node, "address": info["address"]} 
        for node, info in nodes_info.items() 
        if file_name in [f["filename"] for f in info["files"]]
    ]
    return {"nodes": nodes_with_file}
