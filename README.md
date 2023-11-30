markdown
Copy code
# File Sharing System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

O File Sharing System é um sistema de compartilhamento de arquivos que permite que vários nós (FS_Nodes) compartilhem e consultem a localização de arquivos em uma rede distribuída. O sistema é composto por dois componentes principais: FS_Tracker (rastreador) e FS_Node (nó).

## Funcionalidades

- Registro de FS_Nodes no FS_Tracker.
- Atualização periódica das informações dos arquivos nos FS_Nodes.
- Consulta da localização de arquivos por nome.

## Requisitos

- Python 3.8 ou superior.

## Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/seu-usuario/file-sharing-system.git

2. Navegue até o diretório do projeto:

   ```bash
   cd file-sharing-system


3. Crie um ambiente virtual (opcional, mas recomendado):

   ```bash
   python -m venv venv

4.Ative o ambiente virtual (Linux/Mac):

   ```bash
   source venv/bin/activate
```


Ative o ambiente virtual (Windows):

   ```bash

   .\venv\Scripts\activate
```

5. Instale as dependências:

   ```bash

   pip install -r requirements.txt


## Uso
## FS_Tracker
Inicie o servidor FS_Tracker:

  ```bash

python tracker_server.py
```

O FS_Tracker estará ouvindo em localhost:9090 por padrão.

## FS_Node
Configure o endereço do FS_Tracker no arquivo fs_node.py:


  ```bash
tracker_address = ('localhost', 9090)
```
Inicie um nó FS_Node:

```bash
python fs_node.py
```
O nó se registrará no FS_Tracker e estará pronto para compartilhar arquivos.
