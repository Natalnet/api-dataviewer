FROM python:3.8

# Essa porta será exposta para ser utilizada como comunicação com este container
EXPOSE 5050

# Define o diretório principal do container
WORKDIR /app

# Copiando os arquivos necessários para a construção e funcionamento da api
COPY ./requirements.txt /app
COPY ./classes /app/classes
COPY ./container-api-users/handler_users.py /app

# Instala os pacotes necessários, listados no documento requirements.txt
RUN pip install -r requirements.txt

# Ao ser contruído o container irá rodar o handler da api de users
CMD python handler_users.py


