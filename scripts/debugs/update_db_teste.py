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


#Lendo variáveis de ambiente
PASSWORD_DB = os.getenv('PASSWORD_DB')
USER_DB = os.getenv('USER_DB')

#Instanciando as classes
lop = Lop()		
psql = Manage_db(database = 'dataviewer_lop', port = '5432', host = 'db-lop', user = USER_DB, password = PASSWORD_DB)

#Essa função verifica a base de dados e definirá a data em que
#será realizada a consulta dessa tabela. Caso a tabela esteja vazia
#o retorno será a primeira data que se tem cadastro no lop
#caso exista dados na tabela, a consulta deve buscar a data do
#ultimo ultimo registro
def verify_database(name_table):
	print('Verificando a última data da tabela ' + name_table)
	condition = 'WHERE "createdAt" IS NOT NULL ORDER BY "createdAt" DESC LIMIT 1'
	#Consulta no db
	query = psql.search(table=name_table, columns='"createdAt"', condition=condition)
	if query.empty == True:
		#Retorna a data do primeiro registro no LoP
		print('A tabela se encontra vazia')
		return '2020-01-01 00:00:00'
	else:
		print('A tabela ' + name_table + ' possui registros, sendo o último deles ' +  query['createdAt'][0])
		#Retorna a ultima data
		return query['createdAt'][0]

#Essa função é responsável por inserir os novos dados no db
def insert_in_db(df, name_table):
	#Se a consulta não retornar nenhum dado então retorne
	if df.empty:
		print('A consulta retornou sem nenhum dado novo, retornando')
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
			print('Inserindo novos dados no banco')
			#Tenta inserir no bd
			psql.insert_df(table = name_table, df=df)
			print('Inserção realizada com sucesso na tabela ' + name_table)
			return
		except Exception as e:
			#Caso a inserção não de certo
			#pensar em algo como enviar por email
			print('Erro em inserir na tabela de ' + name_table + ' ' + str(e))
			return


#Todas as funções de atualização seguiram o mesmo padrão. 
#Irão chamar a função de verificação no banco, onde vai receber uma 
#data, a partir dela é feita uma consulta na API do LoP

def update_questions():
	name_table = 'questions'
	print('Inicializando função de update de ' + name_table)
	#Coletando a data mais recente dessa tabela no bd
	date = verify_database(name_table)
	#Leitura de variáveis de ambiente
	key = os.getenv('SECRET_KEY')
	endpoint_all_questions = os.getenv('ENDPOINT_ALL_QUESTIONS')
	print('Realizando consulta na API')
	#Consulta na API do LoP
	df = lop.lop_question_db(endpoint_all_questions, key, date)
	#Insere os dados novos na tabela respectiva no db
	insert_in_db(df, name_table)
	return

def update_teachers_classes():
	name_table = 'teachers_classes'
	print('Inicializando função de update de ' + name_table)
	#Coletando a data mais recente dessa tabela no bd
	date = verify_database(name_table)
	#Leitura de variáveis de ambiente
	key = os.getenv('SECRET_KEY')
	endpoint_all_classes = os.getenv('ENDPOINT_ALL_CLASSES')
	endpoint_teacher = os.getenv('ENDPOINT_TEACHER')
	print('Realizando consulta na API')
	try:
		#Consulta
		df = lop.lop_class_db(endpoint_all_classes, endpoint_teacher, key, date)
	except Exception as e:
		raise ValueError('Error: consult in lop. ' + str(e))
	try:
		#Insere os dados novos na tabela respectiva no db
		insert_in_db(df, name_table)
	except Exception as e:
		raise ValueError('Error: insert in db. ' + str(e))
  	
def update_submissions():
	name_table = 'submissions'
	print('Inicializando função de update de ' + name_table)
	#Coletando a data mais recente dessa tabela no bd
	date = verify_database(name_table)
	#Leitura de variáveis de ambiente
	key = os.getenv('SECRET_KEY')
	endpoint_all_submissions = os.getenv('ENDPOINT_ALL_SUBMISSIONS')
	#Coletando a data atual para usar como limite
	actual_date = datetime.now()
	#Retira problemas para a conversão de data
	date = date.replace('T',' ').split('.')[0]
	#Converte para o formato
	date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
	#Condição para impedir que a função faça consulta na API quando o intervalo de tempo é menor que 0 dias
	#Já que o range de datas está configurado pra gerar intervalo de 1 dia, deixar passar menos que isso 
	#o código da erro
	#O if verifica se o intervalo de tempo for igual a 0 dias, se for, retorne
	if (actual_date - date).days == 0:
		print('Intervalo de tempo menor que 1 dia.')
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
  				print('Realizando consulta na API com as datas entre ' + date + ' e ' + date_limit)
  				#Consulta na API
  				df = lop.lop_submission_db(endpoint_all_submissions, key, date, date_limit)
  				print('Requisição aceita. Os dados são:')
  				print(df)
  				#Insere os dados novos na tabela respectiva no db
  				insert_in_db(df, name_table)
  				#Se funcionar o iterador recebe 5 que é o valor que sai do laço de tentativas
  				j = 5
  				#Mudamos o estado da flag pra mostrar que a consulta foi realizada com sucesso
  				requisition_accepted = True  					
  			except Exception as e:
  				print('erro foi ' + str(e))
  				#Incrementador que limita o número de tentativas
  				j = j + 1
  		#Se a consulta não foi aceita		
  		if requisition_accepted == False:
  			#***** local de futuro envio de email
  			print('Requisição recusada entre ' + date + ' e ' + date_limit)
  			return
  		else:		
  			print('Requisição realizada com sucesso')

def update_lists():
	name_table = 'lists'
	print('Inicializando função de update de ' + name_table)
	#Coletando a data mais recente dessa tabela no bd
	date = verify_database(name_table)
	#Leitura de variáveis de ambiente
	key = os.getenv('SECRET_KEY')
	endpoint_all_lists = os.getenv('ENDPOINT_ALL_LISTS')
	print('Realizando consulta na API')
	#Consulta
	df = lop.lop_lists_db(endpoint_all_lists, key, date)
	#Insere os dados novos na tabela respectiva no db
	insert_in_db(df, name_table)
	return

def update_tests():
	name_table = 'tests'
	print('Inicializando função de update de ' + name_table)
	#Coletando a data mais recente dessa tabela no bd
	date = verify_database(name_table)
	#Leitura de variáveis de ambiente
	key = os.getenv('SECRET_KEY')
	endpoint_tests = os.getenv('ENDPOINT_ALL_TESTS')
	print('Realizando consulta na API')
	#Consulta
	df = lop.lop_tests_db(endpoint_tests, key, date)
	#Insere os dados novos na tabela respectiva no db
	insert_in_db(df, name_table)
	return
  	
#Função que atualiza os dados conforme a data e a hora escolhida
def update_db():
	try:
		print('Na função enquanto não é chegada a hora da tarefa programada')
		schedule.every().day.at('11:42').do(update_lists)
		schedule.every().day.at('11:43').do(update_tests)
		schedule.every().day.at('11:44').do(update_teachers_classes)
		schedule.every().day.at('22:17').do(update_questions)		
		schedule.every().day.at('04:00').do(update_submissions)
		#Para não chamar a função mais uma vez, é inserido um intervalo de tempo
		#para a próxima chamada de função
		time.sleep(20)
	except Exception as e:
	    return 'Error: update function' + str(e)

while True:
	update_db()
	schedule.run_pending()
	time.sleep(1)
