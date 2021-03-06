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
	condition = 'where.....'
	#Consulta no db
	query = psql.search(table=name_table, columns='createdAt', condition=condition)
	if query.empty == True:
		#Retorna a data do primeiro registro no LoP
		return '2020-01-01'
	else:
		#Retorna a ultima data
		return query

#Todas as funções de atualização seguiram o mesmo padrão. 
#Irão chamar a função de verificação no banco, onde vai receber uma 
#data, a partir dela é feita uma consulta na API do LoP

def update_questions():
	name_table = 'questions'
	#Coletando a data mais recente dessa tabela no bd
	date = verify_database(name_table)
	#Leitura de variáveis de ambiente
	key = os.environ['SECRET_KEY']
	endpoint_question = os.environ['ENDPOINT_ALL_QUESTIONS']
	#Consulta na API do LoP
	df = lop.lop_question(endpoint_question, key)
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
	#Consulta
	df = lop_submission_db(self, endpoint_submissions, key, date)
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
	#Consulta
	df = lop_lists_db(endpoint_lists, key, date)
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
	#Consulta
	df = lop_tests_db(endpoint_tests, key, date)
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
def update_df():
	try:
		schedule.every().day.at('03:00').do(update_submissions)
		schedule.every().day.at('03:10').do(update_lists)
		schedule.every().day.at('03:15').do(update_tests)
		schedule.every().day.at('03:20').do(update_teachers_classes)
		schedule.every().day.at('03:25').do(update_questions)		
	except:
		print('Erro na função de update')

while True:
	update_df()
	schedule.run_pending()
	time.sleep(70)

#https://github.com/vilsonrodrigues/AutomacaoPython/blob/master/automacao_tarefas_schedule.py
