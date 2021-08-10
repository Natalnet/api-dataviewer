<p align="center">
  <img src="https://raw.githubusercontent.com/Natalnet/api-dataviewer/main/container-front/public/marca.png" width="100">
</p>

<h1><p align = "center">API - Dataviewer</p></h1>

Seja bem vindo ao repositório da API do nosso projeto de visualização de dados acadêmicos! 

Nosso projeto se chama `DataViewer`, e aqui, você irá encontrar os arquivos referentes a API que interliga o nosso banco de dados ao Front-end do nosso sistema.

---

<p align="center">
  <a href="#1-visão">Visão</a> •
  <a href="#2-tecnologias-utilizadas">Tecnologias Utilizadas</a> •
  <a href="#3-funcionamento-da-api">Funcionamento da API</a> •
  <a href="#4-documentação-do-projeto">Documentação do Projeto</a> •
  <a href="#5-licença">MIT</a>
</p>

---

## 1. Visão

> O Dataviewer promoverá a **maximização do rendimento dos alunos** e a **minimização de reprovações e evasões**. 

A plataforma fornecerá um meio de ***acompanhamento contínuo e personalizado*** dos alunos, em tempo real, o qual auxiliará professores e alunos a realizar tomadas de decisões estratégicas embasadas. Consequentemente, contribuirá para o ***aprimoramento de processos de ensino e apredizagem***.

## 2. Tecnologias Utilizadas:

* `Python` - realiza toda a lógica por trás da API Dataviewer
* `PostgreSQL` - armazena os dados utilizando o conceito de Data Warehouse
* `Docker` - realiza a containerização dos serviços
* `Nginx` - realiza a função de proxy reverso
* `Certbot` - nos fornece a certificação SSL para o proxy reverso
* `Git` - auxilia no versionamento do projeto
* `CentOS` - distribuição Linux na qual o projeto se encontra em funcionamento
* `Cron` - realiza tarefas agendadas recorrentes

## 3. Funcionamento da API

### 3.1. Qual a origem dos dados?

Nossos dados são obtidos por meio da API da `plataforma LoP`. O LoP é uma *plataforma de gerenciamento de exercícios* para a disciplina de lógica de programação da UFRN. Se você quiser testar a plataforma, é só acessar o seguinte link <a src= http://lop.ect.ufrn.br>http://lop.ect.ufrn.br</a> e se cadastrar.

### 3.2. Que tipo de dados são obtidos?

Hoje, coletamos 5 tipos de dados. São eles:

1. Professores e suas respectivas turmas
2. Submissões de questões por usuário
3. Questões cadastradas
4. Listas cadastradas
5. Provas cadastradas

### 3.3. Onde os dados são armazenados?

Os dados obtidos são armazenados em um banco da dados PostgreSQL. Nós usamos o conceito de *Data Warehouse*, ou seja, os dados não são modificados, apenas armazenados e disponibilizados para consulta. Temos um código que realiza a atualização diária do nosso banco de dados.

### 3.4. Como funciona o código de atualização?

Utilizamos o agendador de tarefas recorrentes *Cron* dos sistemas Unix, o qual está programado para executar o código de atualização diariamente às 03:00 BRT.

A atualização é realizada levando em consideração a *data do último registro de cada tabela* armazenada no nosso banco de dados. Assim, faz-se uma requisição passando a data de cada tabela à API do LoP, via URL. Desse modo, o LoP nos retorna todos os registros dessa data em diante. Caso não haja dados para atualizar, é feita a busca da data do primeiro registro no banco de dados da plataforma LoP.

### 3.5. E como funciona a comunicação com o Front-end?

O Front-end realiza uma solicitação dos dados de uma turma em específico à API do Dataviewer. Uma vez recebida a requisição, seguimos para a consulta do nosso banco de dados. Processamos os dados, e retornamos em formato *JSON* todos os dados necessários para o Front-end gerar todos os gráficos projetados.

## 4. Documentação do projeto

Tendo em vista que o funcionamento da API exige que uma série de serviços estejam sendo executados em sincronia, a manutenção do código exige conhecimentos básicos de Docker como criar containers, remover imagens, utilizar variáveis de ambiente e realizar tarefas agendadas com o Cron. 

Desse modo, com o objetivo de promover a gestão do conhecimento, mais informações acerca dos comentários acima podem ser encontradas na <a href="https://github.com/Natalnet/api-dataviewer/tree/main/docs">pasta de documentação</a>.

## 5. Licença

<a href="https://github.com/Natalnet/api-dataviewer/blob/main/LICENSE">MIT</a>

---
