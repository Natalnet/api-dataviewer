# API - Users

## A idéia por trás do código

A idéia foi construir uma API que gerencie os usuários. Os usuários estão dividos em 2 classes, os usuários da API e os do frontend. 

O usuário Master é um usuário da API e apenas ele pode cadastrar novos usuários da API.

Os usuários da API podem fazer:
* Cadastrar professores e alunos
* Acessar as rotas que geram dados

Os usuários do frontend, professores e alunos podem:
* Solicitar por meio do frontend os seus dados do LoP

## Funcionamento da API

### Registro

O usuário master pode registrar usuários da API e do frontend. Os dados vem via JSON e são registrados no banco se o username for válido. As senhas de todos os usuários são gravadas com um Hash de 512. Para o registro de professores e alunos é demandado alguns outros dados mas o processo de inserção é igual e pode ser feito apenas por usuários da API.

### Autenticação

A autenticação necessita apenas receber um json com o username e o password, é buscado no banco se o usuário existe, e se existe, ele verifica se a senha que vem no json é a senha que está armazenada no banco em formato de Hash.
