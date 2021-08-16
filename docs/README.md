<h1><p align = "center">Documentação Técnica</p></h1>

## Considerações Iniciais

Somado aos comentários nos códigos, e tendo em vista que por se tratar de um projeto universitário existirá alta rotatividade de desenvolvedores iniciantes, aqui entraremos mais a fundo sobre o objetivo e funcionamento de alguns serviços de nosso projeto que merecem uma atenção a mais, bem como iremos compartilhar lições aprendidas e informações essenciais para garantir a reprodutibilidade e pleno funcionamento da aplicação.

---

## Documentações existentes
1. <a href="#1-realizando-o-deploy-do-projeto-em-uma-máquina-unix-like">Realizando o deploy do projeto em uma máquina Unix-like</a> 

2. <a href="#2-docker-manutenção-e-boas-práticas">Docker: manutenção e boas práticas</a>

---

## 1. Realizando o deploy do projeto em uma máquina Unix-like

### 1.1. Contextualização

De um modo geral, a principal demanda do nosso projeto é ter um sistema que rode o Docker. Contudo, como utilizamos o `Cron` da máquina na qual o projeto está hospedado para realizar os agendamentos, a forma como os nossos agendamentos foi estruturado exige que a máquina seja Unix-like, tal qual o CentOS.

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

> A ser construído
