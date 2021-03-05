# API - DataViewer

Seja bem vindo ao repositório da API do nosso projeto de visualização de dados acadêmicos intuitulado de DataViewer. Aqui você irá encontrar os arquivos referentes a API que interliga o nosso banco de dados ao front-end do nosso sistema.

# Meta
Fornecer um acompanhamento contínuo e personalizado dos alunos. De fato, essa acompanhamento, em tempo real, auxiliará os professores e os alunos nas suas tomadas de decisões estratégicas para aprimorar o seu processo de ensino e a apredizagem. Por tanto, esperamos um melhor redimentos dos alunos e um minimização de reprovações e evasões.

## Ambiente de desenvolvimento

Tecnologias utilizadas ao longo do desenvolvimento do projeto

* Python
* Postgres
* Nginx
* Docker
* Git

## Entendendo como funciona a API

### De onde vem os dados?

Nossos dados são obtidos por meio da API da plataforma LoP. Visto que, o Lop, é uma plataforma de gerenciamento de exercícios para a disciplina de lógica de programação da UFRN. Se você quiser testar a plataforma é só acessar o seguinte link <a src= http://lop.ect.ufrn.br>http://lop.ect.ufrn.br</a> e se cadastrar.

### Quais dados são obtidos?

Hoje, coletamos 5 tipos de dados. São eles

* Turmas e seus professores 
* Submissões
* Questões
* Listas
* Provas

### E onde esses dados ficam?

Os dados obtidos são armazenados em um banco da dados Postegres. Nós usamos o conceito de Data Warehouse, ou seja, os dados não são modificados, apenas armazenados e disponíveis pra consulta. Temos um código que realiza a atualização diariamente do nosso banco de dados.

### E como funciona o código de atualização?

A atualização é realizada baseando-se na data do último registro, de cada tabela, armazenada no nosso banco de dados. Assim, faz-se uma requisição, passando a data de cada tabela pela URL, à API do Lop. Desse modo, será retornado todos os registros dessa data em diante. Caso não haja dados para atualizar, é feita a busca da data do primeiro registro no banco de dados da plataforma LOP. Para implementar essa atividade, utilizamos a library Schedule do Python. Essa, por sua vez, permite agendamentos de tarefa, dessa maneira, temos de forma automática a atualização conforme uma data e hora específica.

### E como funciona a comunicação com o front-end?

O front-end socilita a nossa API os dados de uma turma em específico. Em seguida, essa requisição é recebida, e é feita a consulta no banco de dados. Por fim, retornado em, formato JOSN, os dados dos gráficos para vizualização.
