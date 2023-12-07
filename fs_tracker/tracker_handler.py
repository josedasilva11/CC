import threading

# Dicionário para armazenar a informação dos nodos e ficheiros 
nodes_info = {}

# Lock para sincronização de acesso ao dicionário
nodes_lock = threading.Lock()

def process_request(request_data):
    # Processa a requisição recebida do FS_Node.
    # Args:
    #     request_data (dict): Um dicionário contendo os dados da requisição.
    # Returns:
    #     dict: Um dicionário com a resposta para a requisição

    action = request_data.get("action")
    node_name = request_data.get("node_name")  # Usando nome do nodo em vez de ID
    node_address = request_data.get("node_address")
    files = request_data.get("files", [])

    with nodes_lock:
        if action == "register":
            nodes_info[node_name] = {"node_address": node_address, "files": files}
            return {"status": "success", "message": "Node registered successfully"}

        elif action == "update":
            if node_name in nodes_info:
                nodes_info[node_name]["files"] = files
                return {"status": "success", "message": "Node updated successfully"}
            else:
                return {"status": "error", "message": "Node not found"}

        elif action == "query":
            file_name = request_data.get("filename")
            nodes_with_file = [
                {'name': name, 'address': data['node_address']} 
                for name, data in nodes_info.items() 
                if any(f["filename"] == file_name for f in data["files"])
            ]
            if nodes_with_file:
                return {"status": "success", "nodes": nodes_with_file}
            else:
                return {"status": "error", "message": "File not found"}

        else:
            return {"status": "error", "message": "Unrecognized action"}

    return {"status": "error", "message": "Invalid request"}
