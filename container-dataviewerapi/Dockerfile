# O objetivo desse dockerfile é de basicamente configurar, em conjunto com o docker-compose.yml na pasta raiz, 
# as condições de inicialização do container dataviewerapi, cuja função principal é de formar uma API em Flask
# a qual, mediante requisição, manipula os dados advindos do banco de dados SQL e os retorna.

# Utiliza uma imagem oficial do python como base
FROM python:3.8

# Expõe a porta pela qual o container vai se comunicar. Nesse caso, escolhemos a porta padrão do Flask, que é a 5000
EXPOSE 5000

# Seta um novo diretório padrão para a parte virtualizada (relativa ao container). Caso não exista, o diretório é criado
WORKDIR /app

# Observação: Como no docker-compose setamos 'context: .', a pasta raiz do dockerfile na máquina local passou a ser a pasta raiz desse projeto (api-dataviewer)

# O comando COPY copia um arquivo (ou todos os arquivos dentro de um diretório) local para o nosso diretório virtualizado (relativo ao container)
# Sintaxe: COPY (arquivo/arquivos locais) (diretório virtualizado)

# Copia as dependências (lista de pacotes a serem instalados) para o container
COPY ./requirements.txt /app

# Copia o conteúdo da pasta classes (que são os principais códigos utilizados como base para todas as API's do projeto) para este container
COPY ./classes /app/classes

# Instala os pacotes necessários, listados no documento requirements.txt
RUN pip install -r requirements.txt

# Copia o programa principal (handler_lop.py) para o diretório padrão (/app)
COPY ./container-dataviewerapi/handler_lop.py /app
# Roda o programa principal do container (handler_lop.py) do diretório /app quando o container for inicializado.
CMD python handler_lop.py
