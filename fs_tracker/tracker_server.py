import socket
import threading
import json
from datetime import datetime

# Importar as funções do tracker_handler.py
from tracker_handler import process_request

# Dicionário para armazenar a informação dos nodos e ficheiros 
nodes_info = {}

# Lock para sincronização de acesso ao dicionário
nodes_lock = threading.Lock()

def handle_client(conn, addr):
    
#    Lida com as requisições de um cliente (FS_Node).
#
#    Args:
#        conn (socket.socket): O objeto de soquete para comunicação com o cliente.
#        addr (tuple): A tupla contendo o endereço IP e a porta do cliente.
        
        
    with conn:
        print(f"Connected by {addr}")
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = json.loads(data.decode('utf-8'))

                # Processar a requisição com a função do tracker_handler.py
                response_data = process_request(message)
                
                # Responder ao nodo
                response = json.dumps(response_data).encode('utf-8')
                conn.sendall(response)

                # Se a ação for "register", "update" ou "query", continue aguardando comandos do nó
                if message.get("action") in ["register", "update", "query"]:
                    continue
                else:
                    break  # Encerrar a conexão após um comando diferente de "register", "update" ou "query"

        except json.JSONDecodeError:
            print("Received invalid JSON.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print(f"Connection closed with {addr}")

def start_server():
    
    #Inicia o servidor FS_Tracker para lidar com as conexões dos FS_Nodes.
    
    host = ''  # Endereço IP em branco significa escutar em todas as interfaces disponíveis
    port = 9090
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"FS_Tracker listening on {host}:{port}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()