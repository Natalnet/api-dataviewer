# O objetivo desse dockerfile é de basicamente configurar, em conjunto com o docker-compose.yml na pasta raiz, 
# as condições de inicialização do container updatedb, cuja função principal é de atualizar diariamente 
# nosso banco de dados SQL com os novos dados advindos da plataforma LOP de programação.

# Utiliza uma imagem oficial do python como base
FROM python:3.8

# Expõe a porta pela qual o container vai se comunicar. Nesse caso, escolhemos arbitrariamente a porta 3000
EXPOSE 3000

# Seta um novo diretório padrão para a parte virtualizada (relativa ao container). Caso não exista, o diretório é criado
WORKDIR /app

# Observação: Como no docker-compose setamos 'context: .', a pasta raiz do dockerfile na máquina local passou a ser a pasta raiz desse projeto (api-dataviewer).

# O comando COPY copia um arquivo (ou todos os arquivos dentro de um diretório) local para o nosso diretório virtualizado (relativo ao container)
# Sintaxe: COPY (arquivo/arquivos locais) (diretório virtualizado)

# Copia as dependências (lista de pacotes a serem instalados) para o container
COPY ./requirements.txt /app

# Copia o conteúdo da pasta classes (que são os principais códigos utilizados como base para todas as API's do projeto) para este container
COPY ./classes /app/classes

# Instala os pacotes necessários, listados no documento requirements.txt
RUN pip install -r requirements.txt

# Copia o programa principal (update_db.py) para o diretório padrão (/app)
COPY ./container-update-db-lop/update_lop_db.py /app
# Roda o programa principal do container (update_db.py) do diretório /app quando o container for inicializado.
CMD python update_lop_db.py
