def get_file_info(directory):
    """Gera a lista de informações dos arquivos para registro."""
    files = []

    # Exemplo: criar arquivos fictícios no diretório, se não existirem
    for i in range(1, 6):
        filename = f"file{i}.txt"
        filepath = os.path.join(directory, filename)

    # Criação de arquivos fictícios (substitua isso pelo seu caso real)
        try:
            with open(filepath, 'x') as file:
                file.write(f"Conteúdo do arquivo {i}")
        except FileExistsError:
            # Se o arquivo já existir, apenas continue
            pass

    # Adiciona informações do arquivo à lista
        files.append({
            "filename": filename,
            "filesize": os.path.getsize(filepath),
            "filehash": get_file_hash(filepath)
    })

    return files
