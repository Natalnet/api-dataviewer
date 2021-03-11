import schedule
import urllib3
import time
import os
import pandas as pd
from classes.manage_lop import Lop
from classes.manage_db import Manage_db

#Esse arquivo realiza as atualiações no db. Os dados vem da API do LoP
#Se faz uso da lib schedule que permite agendar eventos
#nesse caso vamos agendar a atualização do db em uma hora definida


#Instanciando as classes
lop = Lop()		
psql = Manage_db()

#Essa função verifica a base de dados e definirá a data em que
#será realizada a consulta dessa tabela. Caso a tabela esteja vazia
#o retorno será a primeira data que se tem cadastro no lop
#caso exista dados na tabela, a consulta deve buscar a data do
#ultimo ultimo registro
def verify_database(name_table):
	condition = 'ORDER BY "createdAt" DESC LIMIT 1'
	#Consulta no db
	query = psql.search(table=name_table, columns='"createdAt"', condition=condition)
	if query.empty == True:
		#Retorna a data do primeiro registro no LoP
		return '2020-01-01'
	else:
		#Retorna a ultima data
		return query['createdAt'][0]

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
	#Se a consulta não retornar nenhum dado então retorne
	if df.empty:
		return
	#Se tiver algum dado
	else:
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
	name_table = 'teachers_classes'
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
	print('iniciando a coleta dos dados')
	name_table = 'submissions'
	#Coletando a data mais recente dessa tabela no bd
	#date = verify_database(name_table)
	date = '2021-03-11'
	#Leitura de variáveis de ambiente
	#key = os.environ['SECRET_KEY']
	key = 'd41d8cd98f00b204e9800998ecf8427e'
	#endpoint_submissions = os.environ['ENDPOINT_ALL_SUBMISSIONS']
	endpoint_submissions = 'https://api.lop.natalnet.br:3001/dataScience/submission?key='
	#Consulta
	df = lop.lop_submission_db(endpoint_submissions, key, date)
	#Removendo valores NaN e trocando por 0
	df = df.fillna(0)
	#Se a consulta não retornar nenhum dado então retorne
	if df.empty:
		return
	#Se tiver algum dado
	else:
		#Tenta inserir no bd
		try:
			print('inserindo')
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
	#Se a consulta não retornar nenhum dado então retorne
	if df.empty:
		return
	#Se tiver algum dado
	else:	
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
	#Se a consulta não retornar nenhum dado então retorne
	if df.empty:
		return
	#Se tiver algum dado
	else:
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
def update_db():
	try:
		#Para não chamar a função mais uma vez, é inserido um intervalo de tempo
		#para a próxima chamada de função
		schedule.every().day.at('03:00').do(update_submissions)
		time.sleep(60)
		schedule.every().day.at('03:10').do(update_lists)
		time.sleep(60)
		schedule.every().day.at('03:15').do(update_tests)
		time.sleep(60)
		schedule.every().day.at('03:20').do(update_teachers_classes)
		time.sleep(60)
		schedule.every().day.at('03:25').do(update_questions)		
		time.sleep(60)
	except:
		print('Erro na função de update')

while True:
	update_dbd()
	schedule.run_pending()
	time.sleep(1)

#https://github.com/vilsonrodrigues/AutomacaoPython/blob/master/automacao_tarefas_schedule.py
