import socket
import threading
import json
from datetime import datetime


#Variáveis Globais:
# nodes_info: dicionário para armazenar informações sobre os nodos e ficheiros. 
# Neste contexto, um nodo pode ser um cliente 
# ou servidor na rede que armazena ou requer dados.
# nodes_lock: um Lock que será usado para sincronizar 
# o acesso ao dicionário nodes_info 
# e evitar conflito de threads, i.e, que não ocorram em simultâneo.





# Dicionário para armazenar a informação dos nodos e ficheiros 
nodes_info = {}

# Lock para sincronização de acesso ao dicionário
nodes_lock = threading.Lock() #se uma thread tentar aceder ao mesmo ficheiro ao mesmo tempo o lock impede que o faça 
#se outra thread tentar aceder ao mesmo lock tem de esperar que a outra termine.





# Função handle_client:
# É chamada para lidar com a conexão de um cliente.
# Recebe dados do cliente, os descodifica de JSON, e 
# em função da ação ('register', 'update', 'query'), 
# manipula o dicionário nodes_info dentro de um bloco with 
# Envia uma resposta codificada em JSON de volta ao cliente.


def handle_client(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = json.loads(data.decode('utf-8'))
                action = message.get('action')

                if action == 'register':
                    with nodes_lock:
                        # Atualiza nodes_info com a nova informação do nodo
                        pass
                elif action == 'update':
                    with nodes_lock:
                        # Atualiza a informação existente do nodo
                        pass
                elif action == 'query':
                    with nodes_lock:
                        # Procura a informação solicitada e prepara a resposta
                        pass
                else:
                    raise ValueError(f"Unrecognized action {action}")

                # Responder ao nodo
                response = json.dumps({'status': 'success', 'timestamp': datetime.now().isoformat()}).encode('utf-8')
                conn.sendall(response)

        except json.JSONDecodeError:
            print("Received invalid JSON.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print(f"Connection closed with {addr}")


# Função start_server:
# Configura o socket do servidor para escutar por conexões
# em todas as interfaces disponíveis na porta 9090.
# Aceita conexões e inicia uma nova thread com a 
# função handle_client para lidar com cada conexão de cliente, 
# permitindo que múltiplas conexões sejam gerenciadas simultaneamente.


def start_server():
    host = ''  # Endereço IP em branco significa escutar em todas as interfaces disponíveis
    port = 9090
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"FS_Tracker listening on {host}:{port}")