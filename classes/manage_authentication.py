from passlib.hash import pbkdf2_sha512
from classes.manage_db import Manage_db
import pandas as pd

#psql = Manage_db(database = 'dataviewer_users', port = '5431', host = 'db-lop')
psql = Manage_db(database = 'dataviewer_users', port = '5432', host = 'localhost')

class Authentication:

	def __init__(self, table):
		self.table = table

	#Gera um hash para a senha
	def generate_hash(self, password):
		return pbkdf2_sha512.hash(password)

	#Verifica se as senhas hash que vem do json e do banco são iguais
	def verify_hash(self, password_json, password_db):
		return pbkdf2_sha512.verify(password_json, password_db)

	#Insere novo usuário no banco de dados
	def insert_new_user(self, username_json, password_json, list_datas, list_labels):
		#Verifica se esse usuário existe no banco
		query = self.verify_user(username_json)
		#Se o usuário não existir no banco
		if query.empty == True:
			#Gera um hash correspondente a senha
			password_hash = self.generate_hash(password_json)
			#Insere a senha na lista
			list_datas.append(password_hash)
			#Cria um dataframe a partir das listas
			df = pd.DataFrame([list_datas], columns = list_labels)	
			#Insere no banco de dados
			psql.insert_df(table = self.table, df = df)
			return
		else:
			raise ValueError('Error: insert df in table. ' + str(e))

	#Verifica se esse usuário existe no banco
	def verify_user(self, username_json):
		#Insere aspas
		username_string = "'" + username_json + "'"
		#Monta query
		condition = f'WHERE "username" = {username_string} '
		#Consulta no banco de dados se o usuário existe
		query = psql.search(table = self.table, condition = condition)
		return query		

	#Essa função autentica um usuário. Ela verifica primeiro se o usuário existe no banco
	#e em seguida verifica se a senha que está no banco de dados corresponde a senha
	#que veio no json
	def authenticate_user(self, username_json, password_json):
		#Verifica a existência do usuário
		query = self.verify_user(username_json)
		#Se o retorno for vazio então o usuário não existe no banco
		if query.empty == True:
			raise ValueError('Error: User does not exist.')
		else:
			#Lendo a password correspondente 
			password_db = query['password'][0]
			#Verifica se as senhas são iguais
			if self.verify_hash(password_json, password_db):
				return
			else:
				raise ValueError('Error: different passwords. '  + str(e))

	#Função para atualizar a senha do usuário a partir do username dele
	#Onde os campos com _reference são onde ele vai fazer a busca
	#e os com new são os novos dados
	def update_user(self, table, column_new_data, column_reference, new_data, data_reference):
		new_data = "'" + new_data + "'"
		data_reference = "'" + data_reference + "'"
		#Atualiza senha do usuário
		psql.update(table, column_new_data, column_reference, new_data, data_reference)
		return
		
'''
auth = Authentication(table = 'users')

auth.insert_new_user(user_json, password_json)
auth.verify_user(user_json, password_json)
'''

