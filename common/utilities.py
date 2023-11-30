
import hashlib

def calculate_file_hash(filename):
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Exemplo de uso
file_hash = calculate_file_hash('path/to/your/file.txt')
print("File Hash:", file_hash)
