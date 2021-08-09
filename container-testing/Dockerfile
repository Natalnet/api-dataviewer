FROM python:3.8

WORKDIR /app

COPY ./container-testing/testing-requirements.txt /app

# Copia o conteúdo da pasta classes (que são os principais códigos utilizados como base para todas as API's do projeto) para este container
#COPY ./classes /app/classes

# Instala os pacotes necessários, listados no documento requirements.txt
RUN pip install -r testing-requirements.txt

# Copia o programa principal (handler_lop.py) para o diretório padrão (/app)
COPY ./container-testing/testing-code.py /app
# Roda o programa principal do container (handler_lop.py) do diretório /app quando o container for inicializado.
CMD python testing-code.py
