

# File Sharing System 
(Instruções em Português)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

O File Sharing System é um sistema de partilha de arquivos que permite que vários nós (FS_Nodes) partilhem e consultem a localização de arquivos numa rede distribuída. O sistema é composto por dois componentes principais: FS_Tracker (rastreador) e FS_Node (nó).

## Funcionalidades

- Registo de FS_Nodes no FS_Tracker.
- Atualização periódica das informações dos ficheiros nos FS_Nodes.
- Consulta da localização de ficheiros por nome.
- Aceitação de pedidos de blocos, em paralelo, de diversos outros FS_Nodes.
- Pedido, em paralelo, de blocos do mesmo ficheiro a diversos FS_Nodes.
- Suporte a cenários de perda de blocos, garantindo uma entrega fiável.

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


## Iniciar um Nó FS_Node
Antes de iniciar um nó FS_Node, verifique se o ficheiro fs_node.py foi configurado corretamente com o endereço do FS_Tracker. Abra o ficheiro e encontre a seguinte linha:

```python
tracker_address = ('localhost', 9090)
```
Aqui, você pode então configurar o endereço do FS_Tracker conforme necessário.

Agora, inicie um nó FS_Node com o seguinte comando:

```bash

python fs_node.py
```
O nó será registado no FS_Tracker e estará pronto para partilhar arquivos.

## Registrar Múltiplos FS_Nodes
Você pode registar vários FS_Nodes na rede. Basta seguir as etapas acima para iniciar cada nó numa máquina diferente. Certifique-se de que todos os nós estejam configurados com o mesmo endereço do FS_Tracker.

## Consultar a Localização de um Arquivo
Para consultar a localização de um arquivo pelo nome, você pode usar um cliente para se conectar ao FS_Tracker e enviar uma consulta. Pode então implementar um cliente personalizado ou usar ferramentas de rede para enviar solicitações ao FS_Tracker na porta 9090.

A consulta deve incluir o nome do arquivo que você deseja localizar. O FS_Tracker responderá com uma lista de FS_Nodes que possuem o arquivo e os blocos disponíveis neles.

