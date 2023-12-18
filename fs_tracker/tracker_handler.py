import threading
import logging

# Configuração do sistema de registro de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    logging.info(f"A processar ação: {action}")
    node_name = request_data.get("node_name")  # Usando nome do nodo em vez de ID
    node_address = request_data.get("node_address")
    files = request_data.get("files", [])

    with nodes_lock:
        if action == "register":
            # Extraia o nome do nodo e o endereço do nodo da solicitação
            node_name = request_data.get("node_name")
            node_address = request_data.get("node_address")

            # Verifique se o nome do nodo e o endereço foram fornecidos
            if not node_name or not node_address:
                logging.error(f"Dados incompletos na solicitação de registro: Nome do nodo: {node_name}, Endereço: {node_address}")
                return {"status": "error", "message": "Dados incompletos para registro"}

            # Atualize nodes_info com as informações do novo nodo
            nodes_info[node_name] = {"node_address": node_address, "files": files}
            logging.info(f"Servidor {node_name} registrado com sucesso. Endereço: {node_address}, Arquivos: {files}")
            return {"status": "success", "message": "Node registered successfully"}


        elif action == "update":
            if node_name in nodes_info:
                nodes_info[node_name]["files"] = files
                logging.info(f"Servidor {node_name} atualizado com sucesso. Novos arquivos: {files}")
                return {"status": "success", "message": "Node updated successfully"}
            else:
                return {"status": "error", "message": "Node not found"}

        with nodes_lock:
            if action == "query":
                file_name = request_data.get("filename")
                logging.info(f"Processando query para o arquivo: {file_name}")
                nodes_with_file = [
                    {'name': name, 'address': data['node_address']} 
                    for name, data in nodes_info.items() 
                    if any(f["filename"] == file_name for f in data["files"])
                ]
                if nodes_with_file:
                    response = {"status": "success", "nodes": nodes_with_file}
                    logging.info(f"Enviando resposta para query: {response}")
                    return response
                else:
                    return {"status": "error", "message": "File not found"}

            else:
                return {"status": "error", "message": "Unrecognized action"}
