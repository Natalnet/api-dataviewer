<h1><p align = "center">Documentação Técnica</p></h1>

## Considerações Iniciais

Somado aos comentários nos códigos, e tendo em vista que por se tratar de um projeto universitário existirá alta rotatividade de desenvolvedores iniciantes, aqui entraremos mais a fundo sobre o objetivo e funcionamento de alguns serviços de nosso projeto que merecem uma atenção a mais, bem como iremos compartilhar lições aprendidas e informações essenciais para garantir a reprodutibilidade e pleno funcionamento da aplicação.

---

## Documentações presentes neste arquivo
1. <a href="#1-realizando-o-deploy-do-projeto-em-uma-máquina-unix-like">Realizando o deploy do projeto em uma máquina Unix-like</a> 

2. <a href="#2-docker-manutenção-e-boas-práticas">Docker: manutenção e boas práticas</a>

## Documentações adicionais do projeto
> A ser construído

---

## 1. Realizando o deploy do projeto em uma máquina Unix-like

### 1.1. Contextualização

De um modo geral, a principal demanda do nosso projeto é ter um sistema que rode o Docker. Contudo, como utilizamos o `Cron` da máquina na qual o projeto está hospedado para realizar os agendamentos, a forma como os nossos agendamentos foram estruturados exigem que a máquina seja Unix-like, tal qual o CentOS.

Uma das facilidades do Docker está no fato de que conseguimos subir uma aplicação existente com apenas um comando. Contudo, algumas particularidades desse projeto exigem que certos passos sejam feitos manualmente, os quais serão descritos a seguir.

### 1.2. Deploy do projeto

Uma vez em uma máquina seguindo as configurações especificadas anteriormente, devemos garantir que o *Git*, o *Docker* e o *Docker-compose* estejam devidamente instalados na máquina.

#### 1.2.1. Preparação do ambiente

Em seguida, devemos clonar este repositório para a pasta `/home/admin/api-dataviewer`.

```bash
cd /home/admin/api-dataviewer
git clone git@github.com:Natalnet/api-dataviewer.git .
```

Na pasta api-dataviewer, nós criaremos um arquivo .env o qual irá conter informações sensíveis a respeito do projeto, que serão lidas no momento do build do Docker.

```bash
nano .env
```

Então, colamos no editor *nano* o conteúdo do arquivo *.env* (Ctrl + Shift + V), que está sob posse dos desenvolvedores. Salvamos e saímos o arquivo (Ctrl + X -> Enter).

#### 1.2.2. Preparação do Certbot

Agora, iremos criar alguns arquivos necessários para o funcionamento da autenticação do serviço chamado `certbot`. Como o projeto já está em pleno funcionamento, caso você siga os passos abaixo e encontre algum erro, sugerimos que visite <a href="https://www.digitalocean.com/community/tutorials/how-to-secure-a-containerized-node-js-application-with-nginx-let-s-encrypt-and-docker-compose">esse tutorial.</a>

Para esse passo, basta criarmos uma pasta chamada *dhparam*,

```bash
mkdir /home/admin/api-dataviewer/dhparam
```
E executar o comando abaixo para criar uma chave randomizada.

```bash
sudo openssl dhparam -out /home/admin/api-dataviewer/dhparam/dhparam-2048.pem 2048
```

#### 1.2.3. Agendamento com o Cron

Como última etapa antes de subir o nosso projeto com o Docker, devemos criar o nosso arquivo de agendamento `raiz` do sistema, isso é, o agendamento será feito pelo *Cron* da máquina local e estará executando dois scripts `.sh` que contém comandos de inicializar diariamente o serviço `update-db-lop` e checar diariamente com o `certbot` se o certificado SSL está próximo de expirar.

Devemos tornar os dois arquivos `.sh` do projeto executáveis, através dos comandos abaixo

```bash
chmod +x ssl_renew.sh
chmod +x daily_updatedb.sh
```

Abrimos o crontab raiz do sistema,

```bash
sudo crontab -e
```

E colamos o seguinte conteúdo:

```bash
0 3 * * * /home/admin/api-dataviewer/daily_updatedb.sh >> /var/log/cron.log 2>&1
1 12 * * * /home/admin/api-dataviewer/ssl_renew.sh >> /var/log/cron.log 2>&1

```

Salvamos e fechamos. Para mudar a periodicidade das atualizações, basta editar as 5 posições no começo de cada linha. <a href="https://crontab.guru/examples.html">Esse site</a> pode ser útil para isso.

#### 1.2.4. Executando o projeto com o Docker

Por fim, chegou a hora de subir o nosso projeto para produção. Garantindo que estamos na pasta raiz do projeto (api-dataviewer), devemos ter em mente que essa etapa deverá ser executada **única e exclusivamente** para o primeiro build do projeto. Para realizar a manutenção da estrutura do Docker com os *containers* já criados, por favor consultar a sessão de Docker deste documento.

Rode o código abaixo,

```bash
docker-compose up
```

E o Docker dará início à construção e execução de todos os containers. Para mais informações sobre a manutenção da estrutura do Docker, consulte a sessão a seguir.

## 2. Docker: manutenção e boas práticas

### 2.1. Contextualização

O Docker é uma ferramenta de *containerização* de serviços que tem ganhado bastante notoriedade entre os desenvolvedores, dado que possibilita a criação de aplicações de forma mais leve, segura e eficiente. De um modo geral, uma aplicação nada mais é do que um conjunto de containers atuando de forma colaborativa, e cada container representa um serviço em específico a ser executado, tal qual um script em Python, um sistema operacional, um banco de dados, entre diversas outras possibilidades. 

### 2.2. Arquivos Dockerfile e docker-compose.yml

Nosso objetivo final com o Docker é criar uma aplicação composta de containers os quais executam *serviços* específicos. Para definir o serviço que cada container irá prestar, podemos utilizar dois tipos de arquivos diferentes: o `docker-compose.yml` e/ou o `Dockerfile`.

O **Dockerfile** nada mais é do que um arquivo que contém as instruções que o Docker deverá executar para construir e inicializar um único container, tais quais a *imagem* base a ser utilizada, arquivos locais a serem copiados, entre outros. Tendo em vista que um Dockerfile é referente a um único container, um mesmo projeto que apresenta múltiplos containers poderá apresentar mais de um Dockerfile. Esse arquivo se mostra muito útil quando o desenvolvedor deseja criar um container com muitas particularidades. 

O **docker-compose.yml** é um arquivo que possibilita o Docker a criar e inicializar *múltiplos* containers pertencentes a um mesmo projeto de forma simultânea, permitindo ao desenvolvedor a configuração da estrutura do projeto de uma forma mais centralizada. Para cada container, suas respectivas instruções de criação e inicialização deverão ser especificadas, e isso pode ser feito de duas formas: 

1. Especificando um Dockerfile: Nesse caso, basta o docker-compose evidenciar a localização do Dockerfile relativo a um container específico. Nesse caso, o Docker estará *criando uma nova imagem* com base nas instruções especificadas. Vale salientar que o docker-compose.yml permite que o desenvolvedor realize configurações adicionais à parte do Dockerfile.

2. Utilizando apenas o docker-compose.yml: Alguns *serviços* não possuem a necessidade de serem muito destrinchados, tendo em vista que a *imagem* que eles utilizam como base já é bem estruturada e não existe a necessidade de criar uma nova imagem, como por exemplo um banco de dados PostgreSQL. Resta ao desenvolvedor apenas realizar configurações pontuais no próprio docker-compose.yml.

### 2.3. Conceitos principais

Para garantir a execução de todos os comandos relativos ao Docker, é importante estar no modo de super-usuário, através do comando `sudo su`. Para sair desse modo, basta executar o comando `exit`.

#### 2.3.1. Serviço x Container

Quando falamos em Serviço, estamos nos referindo aos primeiros blocos definidos abaixo de `services:` no docker-compose.yml, enquanto que ao falarmos de Container, estamos nos referindo ao nome do container que foi definido dentro do serviço. Exemplo: temos um serviço denominado *api-lop*, mas o nome do container relativo a esse serviço foi definido como *container-api-lop*. Essa diferença é importante de ser evidenciada para que alguns comandos funcionem corretamente.

Podemos listar todos os containers **ativos** através do seguinte comando:

```bash
docker ps
```

E podemos listar todos os containers ativos e inativos adicionado a flag -a ao final.

```bash
docker ps -a
```

Essas listagens nos permitem visualizar de uma forma mais fácil informações relativas aos containers, tal qual seus nomes, definidos na coluna NAMES. 

Para inicializar um container inativo (exemplo: container-testing):

```bash
docker start container-testing
```

E para tornar o container inativo:

```bash
docker stop container-testing
```

#### 2.3.2. Imagem

> A ser construído

#### 2.3.3. Volume

> A ser construído

### 2.4. Principais comandos a serem utilizados

> A ser detalhado

```bash
docker-compose rm -s -v testing
docker image rm api-dataviewer_testing
docker-compose up -d --force-recreate --no-deps testing
```