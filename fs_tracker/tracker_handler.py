import threading

# Dicionário para armazenar a informação dos nodos e ficheiros 
nodes_info = {}

# Lock para sincronização de acesso ao dicionário
nodes_lock = threading.Lock()

def process_request(request_data):
    """Processa a requisição recebida do FS_Node."""
    action = request_data.get("action")
    node_id = request_data.get("node_id")
    node_address = request_data.get("node_address")
    files = request_data.get("files", [])
    
    with nodes_lock:
        if action == "register":
            nodes_info[node_id] = {"node_address": node_address, "files": files}
            return {"status": "success", "message": "Node registered successfully"}

        elif action == "update":
            if node_id in nodes_info:
                nodes_info[node_id]["files"] = files
                return {"status": "success", "message": "Node updated successfully"}
            else:
                return {"status": "error", "message": "Node not found"}

        elif action == "query":
            file_name = request_data.get("filename")
            nodes_with_file = [
                nid for nid, data in nodes_info.items() if any(f["filename"] == file_name for f in data["files"])
            ]
            if nodes_with_file:
                return {"status": "success", "nodes": nodes_with_file}
            else:
                return {"status": "error", "message": "File not found"}

        else:
            return {"status": "error", "message": "Unrecognized action"}

    return {"status": "error", "message": "Invalid request"}
