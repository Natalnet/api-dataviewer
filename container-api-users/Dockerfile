FROM python:3.9.6

# Define o diretório principal do container
WORKDIR /app
 
# Copiando os arquivos necessários para a construção e funcionamento da api
COPY ./container-api-users/requirements.txt /app
# Copia o conteúdo da pasta classes (que são os principais códigos utilizados como base para todas as API's do projeto) para este container
COPY ./classes /app/classes
COPY ./container-api-users/handler_users.py /app

# Instala os pacotes necessários, listados no documento requirements.txt
RUN pip install -r requirements.txt

# Ao ser contruído o container irá rodar o handler da api de users
CMD python handler_users.py


