# API - DataViewer

Seja bem vindo ao repositório da API do nosso projeto de visualização de dados acadêmicos intuitulado de DataViewer. Aqui você irá encontrar os arquivos referentes a API que interliga o nosso banco de dados ao front-end do nosso sistema.

# Meta

Auxiliar professores e alunos na tomada de decisão através de dados. Conseguindo assim minimizar evasões.

## Ambiente de desenvolvimento

Tecnologias utilizadas ao longo do desenvolvimento do projeto

* Python
* Postgres
* Nginx
* Docker
* Git

## Entendendo como funciona a API

### De onde vem os dados?

Nossos dados são obtidos por meio da API da plataforma LoP.

### Quais dados são obtidos?

Hoje coletamos 5 tipos de dados. São eles

* Turmas e seus professores 
* Submissões
* Questões
* Listas
* Provas

### E onde esses dados ficam?

Os dados obtidos são armazenados em um banco da dados Postegres. Nós usamos o conceito de Data Warehouse, ou seja, os dados não são modificados, apenas armazenados e disponíveis pra consulta. Temos um código que realiza a atualização diariamente do nosso banco de dados.

### E como funciona o código de atualização?

O código verifica no banco de dados, para cada tabela, a data do último registro, com ele, fazer uma requisição para cada tabela, a API do LoP vai retornar todos os registros da data em diante da que foi mandada na URL; caso não retorne nada - banco de dados vazio por exemplo, o código vai buscar pela data do primeiro registro no banco de dados da plataforma LoP. O código faz uso da library Schedule do Python, que permite agendamentos de tarefa, dessa maneira, temos de forma automática a atualização conforme uma data e hora escolhida.

### E como funciona a comunicação com o front-end?

O front-end socilita dados de 1 turma. A API faz a consulta no banco de dados, gera os dados dos gráficos e devolve atráves de um JSON.
