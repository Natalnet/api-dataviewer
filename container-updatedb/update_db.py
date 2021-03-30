import schedule
import urllib3
import time
import os
import pandas as pd
from datetime import datetime
from classes.manage_lop import Lop
from classes.manage_db import Manage_db

#Esse arquivo realiza as atualiações no db. Os dados vem da API do LoP
#Se faz uso da lib schedule que permite agendar eventos
#nesse caso vamos agendar a atualização do db em uma hora definida


#Instanciando as classes
lop = Lop()		
psql = Manage_db()

#Endpoints
os.environ['ENDPOINT_ALL_CLASSES'] = 'https://api.lop.natalnet.br:3001/dataScience/class?key='
os.environ['ENDPOINT_ALL_LISTS'] = 'https://api.lop.natalnet.br:3001/dataScience/list?key='
os.environ['ENDPOINT_ALL_QUESTIONS'] = 'https://api.lop.natalnet.br:3001/dataScience/question?key='
os.environ['ENDPOINT_ALL_SUBMISSIONS'] = 'https://api.lop.natalnet.br:3001/dataScience/submission?key='
os.environ['ENDPOINT_ALL_TESTS'] = 'https://api.lop.natalnet.br:3001/dataScience/test?key='
os.environ['ENDPOINT_TEACHER']  = 'https://api.lop.natalnet.br:3001/dataScience/teacher?key='
os.environ['SECRET_KEY'] = 'd41d8cd98f00b204e9800998ecf8427e'


#Essa função verifica a base de dados e definirá a data em que
#será realizada a consulta dessa tabela. Caso a tabela esteja vazia
#o retorno será a primeira data que se tem cadastro no lop
#caso exista dados na tabela, a consulta deve buscar a data do
#ultimo ultimo registro
def verify_database(name_table):
	condition = 'WHERE "createdAt" IS NOT NULL ORDER BY "createdAt" DESC LIMIT 1'
	#Consulta no db
	query = psql.search(table=name_table, columns='"createdAt"', condition=condition)
	if query.empty == True:
		#Retorna a data do primeiro registro no LoP
		return '2020-01-01 00:00:00'
	else:
		#Retorna a ultima data
		return query['createdAt'][0]

#Essa função é responsável por inserir os novos dados no db
def insert_in_db(df, name_table):
	#Se a consulta não retornar nenhum dado então retorne
	if df.empty:
		return
	#Se tiver algum dado
	else:
		#Caso a tabela a inserir os dados seja de questões, aplicar a função de gerar dados de questões antes
		if name_table == 'questions':
			#Transformando os dados antes de inserir
			df = lop.question_data(df_question = df)
		#Caso a tabela for de submissões, trocar os valores NaN por 0
		elif name_table == 'submissions':
			#Removendo valores NaN e trocando por 0
			df = df.fillna(0)
		try:			
			#Tenta inserir no bd
			psql.insert_df(table = name_table, df=df)
			return
		except Exception as e:
			#Caso a inserção não de certo
			#pensar em algo como enviar por email
			#print('Erro em inserir na tabela de ' + name_table + ' ' + str(e))
			return


#Todas as funções de atualização seguiram o mesmo padrão. 
#Irão chamar a função de verificação no banco, onde vai receber uma 
#data, a partir dela é feita uma consulta na API do LoP

def update_questions():
	name_table = 'questions'
	#Coletando a data mais recente dessa tabela no bd
	date = verify_database(name_table)
	#Leitura de variáveis de ambiente
	key = os.environ['SECRET_KEY']
	endpoint_all_questions = os.environ['ENDPOINT_ALL_QUESTIONS']
	#Consulta na API do LoP
	df = lop.lop_question_db(endpoint_all_questions, key, date)
	#Insere os dados novos na tabela respectiva no db
	insert_in_db(df, name_table)
	return

def update_teachers_classes():
	name_table = 'teachers_classes'
	#Coletando a data mais recente dessa tabela no bd
	date = verify_database(name_table)
	#Leitura de variáveis de ambiente
	key = os.environ['SECRET_KEY']
	endpoint_all_classes = os.environ['ENDPOINT_ALL_CLASSES']
	endpoint_teacher = os.environ['ENDPOINT_TEACHER'] 
	#Consulta
	df = lop.lop_class_db(endpoint_all_classes, endpoint_teacher, key, date)
	#Insere os dados novos na tabela respectiva no db
	insert_in_db(df, name_table)
	return
  	
def update_submissions():
	name_table = 'submissions'
	#Coletando a data mais recente dessa tabela no bd
	date = verify_database(name_table)
	#Leitura de variáveis de ambiente
	key = os.environ['SECRET_KEY']
	endpoint_all_submissions = os.environ['ENDPOINT_ALL_SUBMISSIONS']
	#Coletando a data atual para usar como limite
	actual_date = datetime.now()
	#Convertendo para o formato americano de datas
	actual_date = actual_date.strftime('%Y-%m-%d %H:%M:%S')
	#Condição para impedir que a função faça consulta na API quando o intervalo de tempo é menor que 0 dias
	#Já que o range de datas está configurado pra gerar intervalo de 1 dia, deixar passar menos que isso 
	#o código da erro
	#O if verifica se o intervalo de tempo for igual a 0 dias, se for, retorne
	if (actual_date - datetime.strptime(date, '%Y-%m-%d  %H:%M:%S')).days == 0:
		return
	#Gerando intervalo de tempo de 3 dias em dataframes
	df_dates = pd.date_range(start = date, end = actual_date, freq = 'D', closed = None)
	#Itera no intervalo das datas
	for i in range (len(df_dates) - 1):
		#Data de início
  		date = str(df_dates[i])
  		#Data limite
  		date_limit = str(df_dates[i+1])
  		#Flag, iterador que limita as 5 tentativas
  		j = 1
  		#Flag, indica que a consulta deu certo
  		requisition_accepted = False
  		while j != 5:
  			try:  			
  				#Consulta na API
  				df = lop.lop_submission_db(endpoint_all_submissions, key, date, date_limit)
  				#Insere os dados novos na tabela respectiva no db
  				insert_in_db(df, name_table)
  				#Se funcionar o iterador recebe 5 que é o valor que sai do laço de tentativas
  				j = 5
  				#Mudamos o estado da flag pra mostrar que a consulta foi realizada com sucesso
  				requisition_accepted = True  					
  			except Exception as e:
  				#print('erro foi ' + str(e))
  				#Incrementador que limita o número de tentativas
  				j = j + 1
  		#Se a consulta não foi aceita		
  		if requisition_accepted == False:
  			#***** local de futuro envio de email  		
  			return
  		else:		
  			print('Requisição realizada com sucesso')

def update_lists():
	name_table = 'lists'
	#Coletando a data mais recente dessa tabela no bd
	date = verify_database(name_table)
	#Leitura de variáveis de ambiente
	key = os.environ['SECRET_KEY']
	endpoint_all_lists = os.environ['ENDPOINT_ALL_LISTS']
	#Consulta
	df = lop.lop_lists_db(endpoint_all_lists, key, date)
	#Insere os dados novos na tabela respectiva no db
	insert_in_db(df, name_table)
	return

def update_tests():
	name_table = 'tests'
	#Coletando a data mais recente dessa tabela no bd
	date = verify_database(name_table)
	#Leitura de variáveis de ambiente
	key = os.environ['SECRET_KEY']
	endpoint_tests = os.environ['ENDPOINT_ALL_TESTS']
	#Consulta
	df = lop.lop_tests_db(endpoint_tests, key, date)
	#Insere os dados novos na tabela respectiva no db
	insert_in_db(df, name_table)
	return
  	
#Função que atualiza os dados conforme a data e a hora escolhida
def update_db():
	try:
		schedule.every().day.at('11:42').do(update_lists)
		schedule.every().day.at('11:43').do(update_tests)
		schedule.every().day.at('11:44').do(update_teachers_classes)
		schedule.every().day.at('12:17').do(update_questions)		
		schedule.every().day.at('15:47').do(update_submissions)
		#Para não chamar a função mais uma vez, é inserido um intervalo de tempo
		#para a próxima chamada de função
		time.sleep(20)
	except Exception as e:
	    return 'Error: update function' + str(e)

while True:
	update_db()
	schedule.run_pending()
	time.sleep(1)
