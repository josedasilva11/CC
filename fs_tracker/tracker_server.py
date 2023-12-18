import socket
import threading
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Importar as funções do tracker_handler.py
from tracker_handler import process_request

# Dicionário para armazenar a informação dos nodos e ficheiros 
nodes_info = {}

# Lock para sincronização de acesso ao dicionário
nodes_lock = threading.Lock()

def handle_client(conn, addr):
    with conn:
        logging.info(f"Conexão estabelecida com {addr}")
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                logging.info(f"Dados recebidos de {addr}: {data}")

                # Tentativa de decodificar a mensagem JSON
                try:
                    message = json.loads(data.decode('utf-8'))
                except json.JSONDecodeError:
                    logging.error("JSON inválido recebido.")
                    break

                # Processar a requisição com a função do tracker_handler.py
                response_data = process_request(message)
                response = json.dumps(response_data).encode('utf-8')
                conn.sendall(response)
                logging.info(f"Resposta enviada para {addr}")

                # Condição para continuar ou interromper a espera por comandos
                if message.get("action") not in ["register", "update", "query"]:
                    break

        except Exception as e:
            logging.error(f"Erro ao processar a solicitação de {addr}: {e}")
        finally:
            logging.info(f"Conexão fechada com {addr}")

def start_server():
    host = 'localhost'
    port = 9091
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    logging.info(f"FS_Tracker à escuta em {host}:{port}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
