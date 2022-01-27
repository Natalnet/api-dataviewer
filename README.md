# Versão de Developer do DATAVIEWER

Esta branch contém os arquivos necessários para rodar a versão atual de desenvolvimento do Dataviewer.

## 1. Conceitos

### 1.1. Docker Compose

O `docker-compose.yml` consiste em um arquivo que define as condições de criação e execução de múltiplas imagens pertencentes a um mesmo projeto. As imagens podem tanto ser criadas exclusivamente por ele (ao baixar uma imagem, pelo parâmetro image), como podem ser criadas em conjunto com o `Dockerfile`, sendo este utilizado quando desejamos criar nossa própria imagem de forma mais maleável (mesmo que para isso precisemos utilizar outra imagem como base)

> :exclamation: Algumas observações
> - Uma vez que determinado parâmetro tenha sido comentado, ele só será comentado novamente caso apresente alguma particularidade
> - Caso o sistema precise ser instalado em uma nova máquina, será necessário revisitar o [Tutorial da Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-secure-a-containerized-node-js-application-with-nginx-let-s-encrypt-and-docker-compose) para garantir o funcionamento do nginx e do certbot. 
## 2. Containers

O `docker-compose.yml` possui os seguintes containers

### 2.1. api-lop

Contem a API REST do LOP encontrada em [API Dataviewer](https://lop.api.dataviewer.natalnet.br/).

> :warning: Nesse site, que é o oficial, ela não está funcionando pois uma vez que fazemos requisições ao DB, é retornado "Internal Server Error". Por outro lado, no nosso container de desenvolvimento, ao configurar o container com o DB, ela funciona tranquilamente. Acesse-a localmente por [http://localhost:5000/](http://localhost:5050/)
  

### 2.2. api-users

Por estar em desenvolvimento, a API deste container não retorna nada. Para fazer este container ser criado, basta adicioná-lo com 

```compose
api-users:
    build:
      context: . 
      dockerfile: ./container-api-users/Dockerfile 
    container_name: container-api-users  
    depends_on: 
      - db-lop 
    ports:
      - "5050:5050"
    networks:
      - backend
```

Podemos futuramente acessar ele por [http://localhost:5050/](http://localhost:5000/)

### 2.3. app

Container utilizado para administrar o front. O front fará requests para as API's as quais retornarão arquivos `.json` no intuito de formar as páginas do front.

> :warning: Por enquanto ele não funciona porque não tem uma conexão com as API's feitas, ele ainda está conectado só com a api do natalnet que não funciona. Ainda está sendo organizada a conexão do front com as API's dos containers. Será acessado por [http://localhost:3000/](http://localhost:3000/)
### 2.4. db-lop

Container onde criamos um banco de dados PostgreSQL para ser conectado com o sistema. 

> :warning: Ele é criado vazio sem nenhum dado, então para adicionar os dados a serem consumidos nas apis, temos que adicionar uma cópia do nosso db nele (próximo tópico).

### 2.5. pgadmin-compose

Container onde podemos acessar uma interface gráfica de gerenciamento de banco de dados do PostgreSQL.

> :warning: Este container não existirá nos arquivos de produção pois é apenas uma forma de manusearmos o postgres com mais facilidade. Conseguimos acessar ele por [http://localhost:15432/](http://localhost:15432/). Utilizando essa interface conseguimos criar um server e também criar nosso db com base numa cópia que o desenvolvedor tem acesso.

### 2.6. api-node

Contem a API desenvolvida em NodeJS. A sua rota principal é a `graphs` em que o professor (client) faz uma requisição com o `id_class` da turma e, ao fazer uma seleção de dados já previamente inseridos pela `api-lop` no MongoDB, ela retorna todas as entidades com dados estatísticos referentes a esta turma.

A arquitetura utilizada para a implementação do código foi a MVC (Model View Controller): o client faz uma requisição para a camada de Controller, o Controller aplica a regra de negócio (services) nesta requisição, a camada de Services interage com as entidades do banco de dados a partir do mapeamento delas por meio do Model, o Model envia um response desses dados para o Controller que por sua fez retorna-os para o client por meio de uma interface, a View.  

## 3. Rodando o serviço

### 3.1.  Preparando o ambiente

Antes de rodar os serviços, é necessário o Docker instalado em sua maquina, caso não tenha pode baixar [aqui](https://www.docker.com/products/docker-desktop). Com ele instalado, siga os seguintes passos

Clone este repositório na sua maquina com

```bash
git clone https://github.com/Natalnet/api-dataviewer.git
```

Entre na pasta do repositório utilizando 

```bash
cd api-dataviewer
```

Alterne para a branch da Versão-Dev com o comando 

```bash 
git checkout Versao-Dev
```

Suba os containers

```bash
docker-compose up -d
``` 

> :warning: A primeira vez tende a demorar um pouco para fazer o build de todas as imagens

### 3.2.  Preenchendo o PostgresSQL

Acesse [http://localhost:15432/](http://localhost:15432/) e utilize as credenciais

| Email              | Username | Password |
|--------------------|----------|----------|
| postgres@email.com | postgres | postgres |


Em Add New Server, crie um novo server com o nome de `Dataviewer` e, na aba Connection, no campo host colocamos `db-lop`. Em username e password, colocamos as mesmas credenciais anteriores. Clique em save para criar o servidor.

Com o botão direito na aba do menu esquerda do server criado, criamos um novo DB chamado `db-lop` em Database após passar o mouse em Create.

Para fazer o restore do banco de dados, clicamos com botão direito em cima do banco de dados e selecionamos o restore. Em file, damos o upload da cópia do db que os desenvolvedores tem disponivel. Após fazer seguir esses passos, ja da para ver o sistema funcionando acessando o front-end em [http://localhost:3000/](http://localhost:3000/).

### 3.2. MongoDB

Acesse a interface gráfica do MongoDB em [http://localhost:8081/](http://localhost:8081/) por meio dessas credenciais

| Username | Password |
|----------|----------|
| admin    | mongodb  |

O banco de dados que você deverá visualizar está nomeado como `apinode`. Com o botão direito, clique em `view`e veja as entidades cadastradas nele.
