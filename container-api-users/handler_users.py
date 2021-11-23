from flask import Flask, request
from flask_cors import CORS
import pandas as pd
import os
from classes.manage_lop import Lop
from classes.manage_db import Manage_db
from classes.manage_authentication import Authentication
from classes.manage_email import Email
from datetime import datetime, timedelta
import urllib3
import json
import warnings
warnings.filterwarnings('ignore')
urllib3.disable_warnings()


#Lendo variáveis de ambiente
PASSWORD_DB = 'postgres'
USER_DB = 'postgres'

#Instanciando classes
lop = Lop()
psql = Manage_db(database = 'db-users', port = '5432', host = 'db-lop',
				 user = USER_DB, password = PASSWORD_DB)
#psql = Manage_db(database = 'dataviewer_users', port = '5432', host = 'localhost')
email = Email()

#Instanciate Flask
app = Flask(__name__)

api_cors_config = {
  'origins':'*',
  'methods':['POST','GET'],
  'allow_headers':['Authorization','Content-Type']
}
cors = CORS(app, resource={r'/*':api_cors_config})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def home():
    return 'Data Viewer API-users'

#Função que verifica se o usuário master que autoriza os cadastros
#foi inserido. Se não, ele vai ser criado
def verify_master_user():
	#Instanciando a autenticação da tabela de usuários da api
	auth = Authentication(table = 'users_api')
	#Verifica se o usuário master existe na tabela de usuários da api
	username = 'Master'
	query = auth.verify_user(username)
	#Data da criação do usuário
	createdAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	if query.empty == True:
		list_datas = [username, createdAt]
		list_labels = ['username','createdAt','password']
		#Lendo a senha que foi passada como variável de ambiente
		password = os.getenv('PASSWORD_MASTER_USER')
		try:
			#Inserindo o usuário master
			auth.insert_new_user(username_json = username,
			  					 password_json = password,
			  					 list_datas = list_datas,
			  					 list_labels = list_labels
			  					 )
			return 'Successful authentication.'
		except Exception as e:
			raise ValueError(str(e))

#Rotas de registro de usuário
@app.route('/register_user_student', methods = ['POST'])
def register_user_student():
	#Instanciando a autenticação da tabela de estudantes do frontend
	auth_users_api = Authentication(table = 'users_api')
	auth_users_students = Authentication(table = 'users_students')
	try:
		user = request.json['user']
		username = request.json['username']
		password = request.json['password']
		name = request.json['name']
		registration = request.json['registration']
		email = request.json['email']
		user_api = request.json['user_api']
		password_user_api = request.json['password_user_api']
	except Exception as e:
		raise ValueError('Error: read json. ' + str(e))
	#Data da criação do usuário
	createdAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	#Verifica se o usuário mestre passado no post é o que permite
	#cadastro no banco de dados, se for correto, o cadastro do usuário 
	#prossegue
	try:
		auth_users_api.authenticate_user(user_api, password_user_api)
	except Exception as e:
		raise ValueError(str(e))		
	list_datas = [username, user, name, registration, email, createdAt]
	list_labels = ['username','user', 'name', 'registration', 'email','createdAt','password']
	try:
		auth_users_students.insert_new_user(username_json = username,
				   	  					    password_json = password,
						  					list_datas = list_datas,
						  				    list_labels = list_labels
						  					)
		return 'New user student successfully inserted.'
	except Exception as e:
		raise ValueError(e)		

@app.route('/register_user_teacher', methods = ['POST'])
def register_user_teacher():
	#Instanciando a autenticação da tabela de professores do frontend
	auth_users_api = Authentication(table = 'users_api')
	auth_users_teachers = Authentication(table = 'users_teachers')
	try:
		username = request.json['username']
		password = request.json['password']
		name_teacher = request.json['name_teacher']
		id_teacher = request.json['id_teacher']
		email = request.json['email']
		user_api = request.json['user_api']
		password_user_api = request.json['password_user_api']
	except Exception as e:
		raise ValueError('Error: read json. ' + str(e))
	#Data da criação do usuário
	createdAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	#Verifica se o usuário mestre passado no post é o que permite
	#cadastro no banco de dados, se for correto, o cadastro do usuário 
	#prossegue
	try:
		#Faz a varredura na banco de usuarios da api
		auth_users_api.authenticate_user(user_api, password_user_api)
	except Exception as e:
		raise ValueError(str(e))
	list_datas = [username, name_teacher, id_teacher, email, createdAt]
	list_labels = ['username','name_teacher', 'id_teacher', 'email', 'createdAt', 'password']
	try:
		auth_users_teachers.insert_new_user(username_json = username,
						  				    password_json = password,
						  				    list_datas = list_datas,
						  					list_labels = list_labels
						  					)
		return 'New user teacher successfully inserted.'
	except Exception as e:
		raise ValueError(e)

@app.route('/register_user_api', methods = ['POST'])
def register_user_api():
	#Instanciando a autenticação da tabela de usuários da api
	auth_users_api = Authentication(table = 'users_api')
	try:
	   	username = request.json['username']
	   	password = request.json['password']
	   	user_api = request.json['user_api']
	   	password_user_api = request.json['password_user_api']
	except Exception as e:
		raise ValueError('Error: read json. ' + str(e))
	#Data da criação do usuário
	createdAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	#Verifica se o usuário mestre passado no post é o que permite
	#cadastro no banco de dados, se for correto, o cadastro do usuário 
	#prossegue
	try:
		if user_api == 'Master':
			auth_users_api.authenticate_user(user_api, password_user_api)
	except Exception as e:
		raise ValueError(str(e))
	list_datas = [username, createdAt]
	list_labels = ['username', 'createdAt', 'password']
	try:
		auth_users_api.insert_new_user(username_json = username,
					  				   password_json = password,
					  				   list_datas = list_datas,
					  				   list_labels = list_labels
					  				   )
		return 'New user api successfully inserted.'
	except Exception as e:
		raise ValueError(str(e))

@app.route('/authenticate_user_student', methods = ['POST'])
def authenticate_user_student():
	#Instancia a autenticação na tabela de alunos
	auth_users_students = Authentication(table = 'users_students')
	try:
		username = request.json['username']
		password = request.json['password']
	except Exception as e:
		raise ValueError('Error: read json. ' + str(e))
	try:
		#Verifica se usuario existe na tabela
		auth_users_students.authenticate_user(username, password)
		return 'Successful authentication.'
	except Exception as e:
		raise ValueError(str(e))

@app.route('/authenticate_user_teacher', methods = ['POST']) 
def authenticate_user_teacher():
	#Instancia a autenticação na tabela de professores
	auth_users_teachers = Authentication(table = 'users_teachers')
	try:
		username = request.json['username']
		password = request.json['password']
	except Exception as e:	
		raise ValueError('Error: read json. ' + str(e))
	try:
		#Verifica se usuario existe na tabela
		auth_users_teachers.authenticate_user(username, password)
		return 'Successful authentication.'
	except Exception as e:
		raise ValueError(str(e))


@app.route('/forgot_password', methods = ['POST'])
def forgot_password():
	#Lê o username do usuário que quer ser alterado e os dados do usuário da api
	try:
	    user_api = request.json['user_api']
	    password_user_api = request.json['password_user_api']
	    username = request.json['username']
	    table = request.json['table']
	except Exception as e:
	    raise ValueError('Error: read json. ' + str(e))
	try:
		#Instancia a classe de autenticação na tabela que o front passar
		auth = Authentication(table = table)
		auth.authenticate_user(user_api, password_user_api)
	except Exception as e:
	    raise ValueError(str(e))
	try:
		#Coletando dados desse usuário
		query = auth.verify_user(username)
		#Coletando email do usuário
		email_user = query['email']
		#Envia email do usuário
		email.send_email(type_message = 'forgot_password', 
						 subject = email_user,
						 name_addressee = username,
						 token = '123',
						 email_address = email_user
						 )
		return 'Successful send email.'
	except Exception as e:
	    raise ValueError('Error: user does not exist. ' + str(e))

#Atualiza a senha do usuário
@app.route('/update_user', methods = ['POST'])
def update_user():
	try:
		user_api = request.json['user_api']
		password_user_api = request.json['password_user_api']
		username = request.json['username']
		new_password = request.json['new_password']
		table = request.json['table']
	except Exception as e:
	    raise ValueError('Error: read json. ' + str(e))
	try:
		#Instancia a classe de autenticação na tabela que o front passar
		auth = Authentication(table = table)
		auth.authenticate_user(user_api, password_user_api)
	except Exception as e:
	    raise ValueError(str(e))
	new_password = auth.generate_hash(password)
	try:
		auth.update_user(table = table, 
						 column_new_data = 'password',
						 column_reference = 'username',
						 new_data = username, 
						 data_reference = new_password)
		return 'Successful update user.'
	except Exception as e:
	    raise ValueError('Error: update password. ' + str(e))

def main():
 	port = int(os.environ.get('PORT', 5050))
 	app.run(host = '0.0.0.0', port = port)   

if __name__ == '__main__':
	verify_master_user()
	main()
