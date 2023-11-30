

# File Sharing System 
(Instruçôes em Português)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

O File Sharing System é um sistema de partilha de arquivos que permite que vários nós (FS_Nodes) partilhem e consultem a localização de arquivos numa rede distribuída. O sistema é composto por dois componentes principais: FS_Tracker (rastreador) e FS_Node (nó).

## Funcionalidades

- Registo de FS_Nodes no FS_Tracker.
- Atualização periódica das informações dos arquivos nos FS_Nodes.
- Consulta da localização de arquivos por nome.

## Requisitos

- Python 3.8 ou superior.

## Instalação

Clone este repositório:

   ```bash
   git clone https://github.com/josedasilva11/CC.git
```
Navegue até à pasta do projeto:

   ```bash
   cd file-sharing-system
```

Crie um ambiente virtual (opcional, mas recomendado):

   ```bash
   python -m venv venv
```
Ative o ambiente virtual (Linux/Mac):

   ```bash
   source venv/bin/activate
```


Ative o ambiente virtual (Windows):

   ```bash

   .\venv\Scripts\activate
```

Instale as dependências: (temos de fazer o ficheiro)

   ```bash

   pip install -r requirements.txt
```

## Uso
## FS_Tracker
Inicie o servidor FS_Tracker:

  ```bash

python tracker_server.py
```

O FS_Tracker estará a ouvir em localhost:9090 por padrão.

## FS_Node
Configure o endereço do FS_Tracker no arquivo fs_node.py:


  ```bash
tracker_address = ('localhost', 9090)
```
Inicie um nó FS_Node:

```bash
python fs_node.py
```
O nó será registado no FS_Tracker e estará pronto para partilhar arquivos.

# File Sharing System
(English Instructions)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

The File Sharing System is a file sharing system that allows multiple nodes (FS_Nodes) to share and query the location of files in a distributed network. The system consists of two main components: FS_Tracker (tracker) and FS_Node (node).

## Features

- Registration of FS_Nodes with FS_Tracker.
- Periodic updating of file information in FS_Nodes.
- Querying the location of files by name.

## Requirements

- Python 3.8 or higher.

## Installation

Clone this repository:

   ```bash
   git clone https://github.com/josedasilva11/CC.git
```
Navigate to the project directory:

  ```bash
cd file-sharing-system
```
Create a virtual environment (optional but recommended):
```bash
python -m venv venv

```
Activate the virtual environment (Linux/Mac):
```bash
source venv/bin/activate
```

Activate the virtual environment (Windows):
```bash
.\venv\Scripts\activate

```

Install the dependencies:
```bash
pip install -r requirements.txt
```



## Usage
## FS_Tracker
Start the FS_Tracker server:


```bash
python tracker_server.py

```
FS_Tracker will be listening on localhost:9090 by default.

## FS_Node
Configure the FS_Tracker address in the fs_node.py file:

```bash
tracker_address = ('localhost', 9090)

```
Start an FS_Node:
```bash
python fs_node.py

```
The node will register with FS_Tracker and be ready to share files.



