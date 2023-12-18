import hashlib
import os


def get_file_blocks(filename, block_size=4096):
    """
    Divide um arquivo em blocos de tamanho fixo e calcula o hash de cada bloco.

    Args:
        filename (str): Caminho do arquivo.
        block_size (int): Tamanho do bloco em bytes.

    Returns:
        list: Lista de tuplas, cada uma contendo os dados do bloco e seu hash SHA-256.
    """
    blocks = []
    with open(filename, 'rb') as file:
        while True:
            block = file.read(block_size)
            if not block:
                break
            block_hash = hashlib.sha256(block).hexdigest()
            blocks.append((block, block_hash))
    return blocks

def get_file_info(directory, block_size=4096):
    """
    Lista todos os arquivos em um diretório e calcula o hash de cada bloco de cada arquivo.

    Args:
        directory (str): Caminho do diretório a ser examinado.
        block_size (int): Tamanho do bloco em bytes para a divisão dos arquivos.

    Returns:
        list: Lista de dicionários, cada um contendo o nome do arquivo, seu tamanho total
              e a lista de hashes de seus blocos.
    """
    files_info = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            file_size = os.path.getsize(filepath)
            blocks = get_file_blocks(filepath, block_size)
            files_info.append({
                "filename": filename,
                "filesize": file_size,
                "blocks": [block_hash for _, block_hash in blocks]
            })
    return files_info

def get_file_block(filename, block_id, block_size=4096):
   
#    Lê e retorna um bloco específico de um arquivo.Essencial para o servidor para responder às solicitações de blocos dos clientes.
#
#    Args:
#        filename (str): Caminho do arquivo.
#        block_id (int): Identificador do bloco a ser lido.
#        block_size (int): Tamanho do bloco em bytes.
#
#    Returns:
#        bytes: O bloco de dados, ou None se houver erro.
  
    try:
        with open(filename, 'rb') as file:
            file.seek(block_id * block_size)
            return file.read(block_size)
    except IOError as e:
        print(f"Erro ao ler o arquivo {filename}: {e}")
        return None

def reconstruct_file_from_blocks(blocks, output_filename):
   
#    Reconstrói um arquivo a partir de uma sequência de blocos de dados. Útil no cliente para montar o arquivo final após todos os blocos serem recebidos.
#
#    Args:
#        blocks (list of bytes): Lista de blocos de dados que formarão o arquivo.
#        output_filename (str): Caminho do arquivo de saída.
  
    try:
        with open(output_filename, 'wb') as file:
            for block in blocks:
                file.write(block)
    except IOError as e:
        print(f"Erro ao escrever no arquivo {output_filename}: {e}")

