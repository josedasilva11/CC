import socket
import json
from datetime import datetime
import os


# get_file_info função:
# Esta função é usada para obter informações sobre os ficheiros presentes em uma diretoria especificada.
# Cria uma lista vazia chamada files para armazenar informações sobre os ficheiros.
# Em seguida, itera pelos ficheiros na diretória especificada através do os.listdir(directory).
# Para cada ficheiro que é realmente um ficheiro (não uma pasta), ele cria um dicionário com o nome do ficheiro
# e potencialmente outras informações, como tamanho e hash (embora a parte de tamanho e hash esteja comentada).
# Esses dicionários são adicionados à lista files, que é retornada quando a função é concluída.


def get_file_info(directory):
    """Gerar a lista de informações dos arquivos para registro."""
    files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            # londe vamos ter logicas do tamanho
            files.append({
                "filename": filename,
                # "filesize": os.path.getsize(os.path.join(directory, filename)),
                # "filehash": "hash_do_arquivo"
            })
    return files


# register_with_tracker função:
# Esta função é usada para registrar as informações do nodo com um rastreador (tracker) de rede.
# Ela recebe dois argumentos: tracker_address (um tuplo com o endereço IP e a porta do tracker)
# e node_info (um dicionário que contem informações sobre o nodo).
# A função cria um socket usando socket.socket com a família de endereços IPv4 (AF_INET)
# e o tipo de socket TCP (SOCK_STREAM).
# Em seguida, ela tenta estabelecer uma conexão com o tracker usando s.connect(tracker_address).
# Ela converte as informações do nodo para o formato JSON e as codifica em UTF-8 antes de enviá-las
# para o tracker através do s.sendall.
# Depois de enviar as informações, a função aguarda uma resposta (até 1024 bytes) do tracker 
# utlizando s.recv(1024).
# A resposta recebida é gravada na saída padrão.
# Em caso de erros de socket, como a falha na conexão, a função captura a exceção e imprime uma mensagem de erro.

def register_with_tracker(tracker_address, node_info):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(tracker_address)
            message = json.dumps(node_info).encode('utf-8')
            s.sendall(message)
            data = s.recv(1024)
        print(f"Received {data.decode('utf-8')}")
    except socket.error as e:
        print(f"Socket error occurred: {e}")


# Bloco if __name__ == "__main__":
# Este bloco é executado quando o script é executado diretamente 
# (não quando é importado como um módulo).
# Ele define o endereço do tracker (tracker_address) como 'localhost' na porta 9090.
# Em seguida, cria um dicionário node_info com informações sobre o nodo, como a ação ("register"),
# um identificador do nodo, endereço do nodo, lista de informações sobre os ficheiros 
# (obtidos pela função get_file_info), e um registo da data e hora ISO.
# Finalmente, chama a função register_with_tracker para registrar as informações do no com o tracker.


if __name__ == "__main__":
    tracker_address = ('localhost', 9090)
    node_info = {
        #"action": "register",
        #"node_id": "",
        #"node_address": "",
        #"files": get_file_info('/pastas dos ficheiros'), 
        #"timestamp": datetime.now().isoformat() + 'Z'
    }
    register_with_tracker(tracker_address, node_info)