from passlib.hash import pbkdf2_sha512
from classes.manage_db import Manage_db

psql = Manage_db(database = 'dataviewer_users')

class Authentication:

	def __init__(self, table):
		self.table = table

	#Gera uma senha em hash
	def generate_hash(self, password):
		return pbkdf2_sha512.hash(password)

	#Verifica se as senhas hash que vem do json e do banco são iguais
	def verify_hash(self, password_json, password_db):
		return pbkdf2_sha512.verify(password_db, password_json)

	#Insere novo usuário no banco de dados
	def insert_new_user(self, user_json, password_json):
		condition = f'WHERE "user" = {user_json}'
		#Consulta no banco de dados se o usuário existe
		query = psql.search(table = self.table, columns = '"password_hash"', condition = condition)
		#Se o retorno for vazio então o usuário não existe no banco
		if query.empty == True:
			#Gera um hash correspondente a senha
			password_hash = self.generate_hash(password_json)
			#Cria o dataframe com os dados
			df = pd.DataFrame([user_json, password_hash], columns = ['user','password_hash'])
			try:
				#Insere na tabela
				pqsl.insert_df(table = self.table, df = df)
				return True
			except Exception as e:
				raise ValueError('Error: insert df in table. ' + str(e))
		else:
			raise ValueError('Error: username already exists in database')

	#Verifica se esse usuário com esse nome e senha existe no banco
	def verify_user(self, user_json, password_json):
		try:
			condition = f'WHERE "user" = {user_json}'
			#Consulta no banco de dados se o usuário existe
			query = psql.search(table = self.table, columns = '"password_hash"', condition = condition)
			#Se o retorno for vazio então o usuário não existe no banco
			if query.empty == True:
				raise ValueError('Error: User does not exist.')
			else:
				#Lendo a password correspondente 
				password_db = query['password_hash'][0]
				#Verifica se as senhas são iguais
				if self.verify_hash(password_json, password_db):
					return True
				else:
					raise ValueError('Error: different passwords. '  + str(e))
		except:
			raisa ValueError('Error: user not found. ' + str(e))

'''
auth = Authentication(table = 'users')

auth.insert_new_user(user_json, password_json)
auth.verify_user(user_json, password_json)
'''

