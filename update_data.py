import schedule
import urllib3
import time
import os
import pandas as pd
from classes.psql import Manage_db
from classes.lop import Lop

#Esse arquivo realiza as atualiações no db. Os dados vem da API do LoP
#Se faz uso da lib schedule que permite agendar eventos
#nesse caso vamos agendar a atualização do db em uma hora definida


#Instanciando a classe
lop = Lop()		
psql = Manage_db()

#Essa função verifica a base de dados e definirá a data em que
#será realizada a consulta dessa tabela. Caso a tabela esteja vazia
#o retorno será a primeira data que se tem cadastro no lop
#caso exista dados na tabela, a consulta deve buscar a data do
#ultimo ultimo registro
def verify_database(name_table):
	#Consulta no db
	query = psql.search(table=name_table, columns='createdAt', condition='last data...')
	if query.empty == True:
		#Retorna a data do primeiro registro no LoP
		return ''
	else:
		#Retorna a ultima data
		return query

#Essa função realiza a consulta no LoP a partir de uma URL 
#Caso a consulta seja um sucesso (codigo 200) ele retorna o resultado
#que vem como um dataframe. Enquanto não for retornado com sucesso
#ele vai ficar em loop até dar certo
#********verificar se existe uma abordagem melhor
def query_lop_data(url):
	#Faz a primeira consulta
	query = lop.lop_class(url)
	#Caso a consulta retorne falso ele vai continuar nesse loop
	#até o retorno ser realizado com sucesso
	while query == False:
		query = lop.lop_class(url)
	return query

#Todas as funções de atualização seguiram o mesmo padrão. 
#Irão chamar a função de verificação no banco, onde vai receber uma 
#data, a partir dela é feita uma consulta na API do LoP, e enquanto 
#não for retornado o código 200 (consulta realizada com sucesso)
#o código fica em loop
def update_questions():
	name_table = 'questions'
	#Coletando a data mais recente dessa tabela no bd
	date = verify_database(name_table)
	#Leitura de variáveis de ambiente
	key = os.environ['SECRET_KEY']
	endpoint_question = os.environ['ENDPOINT_ALL_QUESTIONS']
	#Montagem da url
	url = endpoint_question + key + '&createdAt=' + date
	#Consulta
	df = query_lop_data(url)
	#Tenta inserir no bd
	try:
		psql.insert_df(table = name_table, df=df)
		return
	except Exception as e:
		#Caso a inserção não de certo
		#pensar em algo como enviar por email
		print('Erro em inserir na tabela de questões', e)
		return

def update_teachers_classes():
	name_table = 'teachers'
	#Coletando a data mais recente dessa tabela no bd
	date = verify_database(name_table)
	#Leitura de variáveis de ambiente
	key = os.environ['SECRET_KEY']
	endpoint_classes = os.environ['ENDPOINT_ALL_TEACHERS_CLASSES']
	#Montagem da url
	url = endpoint_classes + key + '&createdAt=' + date
	#Consulta
	df = query_lop_data(url)
	#Tenta inserir no bd
	try:
		psql.insert_df(table = name_table, df=df)
		return
	except Exception as e:
		#Caso a inserção não de certo
		#pensar em algo como enviar por email
		print('Erro em inserir na tabela de professores', e)
		return

def update_submissions():
	name_table = 'submissions'
	#Coletando a data mais recente dessa tabela no bd
	date = verify_database(name_table)
	#Leitura de variáveis de ambiente
	key = os.environ['SECRET_KEY']
	endpoint_submissions = os.environ['ENDPOINT_ALL_SUBMISSIONS']
	#Montagem da url
	url = endpoint_submissions + key + '&createdAt=' + date
	#Consulta
	df = query_lop_data(url)
	#Tenta inserir no bd
	try:
		psql.insert_df(table = name_table, df=df)
		return
	except Exception as e:
		#Caso a inserção não de certo
		#pensar em algo como enviar por email
		print('Erro em inserir na tabela de professores', e)
		return

def update_lists():
	name_table = 'lists'
	#Coletando a data mais recente dessa tabela no bd
	date = verify_database(name_table)
	#Leitura de variáveis de ambiente
	key = os.environ['SECRET_KEY']
	endpoint_lists = os.environ['ENDPOINT_ALL_LISTS']
	#Montagem da url
	url = endpoint_lists + key + '&createdAt=' + date
	#Consulta
	df = query_lop_data(url)
	#Tenta inserir no bd
	try:
		psql.insert_df(table = name_table, df=df)
		return
	except Exception as e:
		#Caso a inserção não de certo
		#pensar em algo como enviar por email
		print('Erro em inserir na tabela de listas', e)
		return

def update_tests():
	name_table = 'tests'
	#Coletando a data mais recente dessa tabela no bd
	date = verify_database(name_table)
	#Leitura de variáveis de ambiente
	key = os.environ['SECRET_KEY']
	endpoint_tests = os.environ['ENDPOINT_ALL_TESTS']
	#Montagem da url
	url = endpoint_tests + key + '&createdAt=' + date
	#Consulta
	df = query_lop_data(url)
	#Tenta inserir no bd
	try:
		psql.insert_df(table = name_table, df=df)
		return
	except Exception as e:
		#Caso a inserção não de certo
		#pensar em algo como enviar por email
		print('Erro em inserir na tabela de provas', e)
		return


#Função que atualiza os dados conforme a data e a hora escolhida
def update_data():
	try:
		schedule.every().day.at('03:00').do(update_submissions)
		schedule.every().day.at('03:10').do(update_lists)
		schedule.every().day.at('03:15').do(update_tests)
		schedule.every().day.at('03:20').do(update_teachers_classes)
		schedule.every().day.at('03:25').do(update_questions)		
	except:
		print('Erro na função de update')

while True:
	update_data()
	schedule.run_pending()
	time.sleep(70)

#https://github.com/vilsonrodrigues/AutomacaoPython/blob/master/automacao_tarefas_schedule.py
