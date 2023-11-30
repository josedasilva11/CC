import hashlib
import os

def calculate_file_hash(filename):
    
#    Calcula o hash SHA-256 de um arquivo inteiro.É útil para verificar a integridade de um arquivo.
#
#    Args:
#        filename (str): Caminho do arquivo cujo hash será calculado.
#
#    Returns:
#        str: Hash SHA-256 do arquivo.
    
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as file:
        # Lê o arquivo em blocos de 4096 bytes para economizar memória.
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

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

# Exemplo de uso
file_hash = calculate_file_hash('path/to/your/file.txt')
print("File Hash:", file_hash)

# Outros exemplos
block = get_file_block('path/to/your/file.txt', 0)  # Pega o primeiro bloco
if block:
    print("Block Data:", block)

blocks = [b'Hello', b' ', b'World!']  # Exemplo de blocos de dados
reconstruct_file_from_blocks(blocks, 'path/to/output/file.txt')
