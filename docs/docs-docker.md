# Documentação - Backend do Docker

## Motivação

A maior parte do nosso projeto gira em torno da manipulação de dados sigilosos e sensíveis, os quais requerem da nossa parte a garantia de segurança e estabilidade. Levando em consideração que contamos com total parceria da UFRN, era certo que teríamos à nossa disposição uma máquina física dentro da universidade para garantir o funcionamento do nosso projeto.

Como forma de garantir um ambiente isolado do restante da máquina física, uma máquina virtual nos vem a mente. Contudo, o Docker se mostra uma ferramenta mais leve, customizada, que nos permite utilizar e instalar apenas o essencial para garantir que o nosso sistema funcione, separando cada serviço do projeto por 'containers', que por sua vez são ambientes isolados mas que conseguem trocar informações essenciais entre si, garantindo assim um funcionamento enxuto e eficiente do projeto.

## Informações gerais do Docker

Sabemos que o Docker funciona isolando serviços por meio de containers. Mas como isso é feito?

Um container é criado ao rodarmos uma *imagem* do Docker. Essa imagem pode ser:
* Baixada: por exemplo, podemos baixar diretamente do repositório do Docker (Dockerhub) a imagem do banco de dados postgres, e a partir dessa imagem teríamos o nosso banco de dados "em branco", porém já pronto para ser acessado e manipulado.
* Construída: por meio de um arquivo chamado Dockerfile, nós podemos utilizar uma imagem para criar uma nova imagem. Por exemplo, a partir de uma imagem em Python baixada do Dockerhub, nós podemos instalar várias dependências necessárias para a execução de um código, e por fim criar uma imagem que estará executando uma API.

Contudo, a medida que o projeto vai tomando maiores proporções, estar utilizando apenas a linha de comando ou executando várias imagens acabam se tornando exaustivos e impraticáveis. Como forma de garantir um funcionamento adequado, entra uma ferramenta do Docker chamada *Docker Compose*. Por meio dessa ferramenta, podemos criar um arquivo chamado docker-compose.yml na pasta raiz de um projeto e especificar as condições de inicialização de múltiplos containers. Para a criação das imagens, podemos em determinados containers optar por baixar diretamente uma imagem e executar, e em outros casos podemos associar a um Dockerfile.

## O Docker no projeto Dataviewer

Conforme especificado na arquitetura do projeto (fornecer link), o backend consiste em diariamente requisitar os dados da plataforma LOP, inserir esses novos dados em nosso banco de dados, e mediante requisição do front, os manipular e disponibilizar via API. Tudo isso é feito a partir dos seguintes serviços:
* sqldb: É o nosso banco de dados. Para a criação de sua imagem, utilizamos diretamente a imagem do postgres do Dockerhub, o configurando apenas no arquivo do docker-compose. Ele está conectado aos containers updatedb-container e dataviewerapi-container.
* updatedb: Está responsável por diariamente atualizar o nosso banco de dados. Para a criação de sua imagem, utilizamos um Dockerfile, o qual a partir de uma imagem em Python, instala dependências e executa o código principal (manage_db.py).
* dataviewerapi: É a API que, mediante solicitação, consulta nosso banco de dados, manipula os dados e os retorna. Assim como o updatedb, sua imagem é construída por meio de um Dockerfile bastante semelhante, no qual a partir de uma imagem em Python, instala dependências e executa o código principal (manage_lop.py).

Todos os parâmetros de inicialização podem ser vistos no arquivo docker-compose.yml, assim como nos Dockerfiles associados.

## Informações Essenciais

Para garantir o funcionamento do projeto, alguns detalhes não podem passar despercebidos:

1. Associação da bibliteca psycopg2 com um banco de dados: Localmente, utilizamos o host "localhost". Contudo, ao passarmos a utilizar o Docker, é essencial que o host seja o serviço ao qual estamos nos conectando. Isso atualmente é definido no arquivo manage_db.py na pasta no diretório /classe.
2. Como garantia de segurança, o SECRET_KEY utilizado para receber os dados da plataforma LOP, em associação aos endpoints, deve ser inserido manualmente para evitar o acesso por pessoas não autorizadas.
