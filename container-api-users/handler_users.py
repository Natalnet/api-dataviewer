from flask import Flask, request
from flask_cors import CORS
import pandas as pd
import os
from classes.manage_lop import Lop
from classes.manage_db import Manage_db
from classes.manage_authentication import Authentication
import urllib3
import json
import warnings
warnings.filterwarnings("ignore")
urllib3.disable_warnings()

#Instanciando classes
lop = Lop()
psql = Manage_db(database = 'dataviewer_users')

#Variavel de teste
os.environ['PASSWORD_MASTER_USER'] = 'mymasterpassword'

#Instanciate Flask
app = Flask(__name__)

api_cors_config = {
  'origins':'*',
  'methods':['POST','GET','OPTIONS'],
  'allow_headers':['Authorization','Content-Type']
}
cors = CORS(app, resource={r'/*':api_cors_config})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def home():
    return 'API de users do Data Viewer'

#Função que verifica se o usuário master que autoriza os cadastros
#foi inserido. Se não, ele vai ser criado
def verify_master_user():
	#Instanciando a autenticação da tabela de usuários da api
	auth = Authentication(table = 'users_api')
	#Verifica se o usuário master existe na tabela de usuários da api
	username = 'Master'
	query = auth.verify_user(username)
	if query.empty == True:
		list_datas = [username]
		list_labels = ['username','password']
		#Lendo a senha que foi passada como variável de ambiente
		password = os.environ['PASSWORD_MASTER_USER']
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
	auth = Authentication(table = 'users_students')
	try:
		user = request.json['user']
		username = request.json['username']
		password = request.json['password']
		name = request.json['name']
		registration = request.json['registration']
		email = request.json['email']
		user_master = request.json['user_master']
		password_master = request.json['password_master']
	except Exception as e:
		raise ValueError('Error: read json. ' + str(e))
	#Verifica se o usuário mestre passado no post é o que permite
	#cadastro no banco de dados, se for correto, o cadastro do usuário 
	#prossegue
	try:
		auth.authenticate_user(user_master, password_master)
	except Exception as e:
		raise ValueError(str(e))		
	list_datas = [username, user, name, registration, email]
	list_labels = ['username','user', 'name', 'registration', 'email','password']
	try:
		auth.insert_new_user(username_json = username,
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
	auth = Authentication(table = 'users_teachers')
	try:
		username = request.json['username']
		password = request.json['password']
		name_teacher = request.json['name_teacher']
		id_teacher = request.json['id_teacher']
		email = request.json['email']
		user_master = request.json['user_master']
		password_master = request.json['password_master']
	except Exception as e:
		raise ValueError('Error: read json. ' + str(e))
	#Verifica se o usuário mestre passado no post é o que permite
	#cadastro no banco de dados, se for correto, o cadastro do usuário 
	#prossegue
	try:
		auth.authenticate_user(user_master, password_master)
	except Exception as e:
		raise ValueError(str(e))
	list_datas = [username, name_teacher, id_teacher, email]
	list_labels = ['username','name_teacher', 'id_teacher', 'email', 'password']
	try:
		auth.insert_new_user(username_json = username,
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
	auth = Authentication(table = 'users_api')
	try:
	   	username = request.json['username']
	   	password = request.json['password']
	   	user_master = request.json['user_master']
	   	password_master = request.json['password_master']
	except Exception as e:
		raise ValueError('Error: read json. ' + str(e))
	#Verifica se o usuário mestre passado no post é o que permite
	#cadastro no banco de dados, se for correto, o cadastro do usuário 
	#prossegue
	try:
		auth.authenticate_user(user_master, password_master)
	except Exception as e:
		raise ValueError(str(e))
	list_datas = [username]
	list_labels = ['username','password']
	try:
		auth.insert_new_user(username_json = username,
		  					 password_json = password,
		  					 list_datas = list_datas,
		  					 list_labels = list_labels
		  					 )
		return 'New user api successfully inserted.'
	except Exception as e:
		raise ValueError(str(e))

@app.route('/authenticate_user_student', methods = ['POST'])
def authenticate_user_student():
	auth = Authentication(table = 'users_students')
	try:
		username = request.json['username']
		password = request.json['password']
	except Exception as e:
		raise ValueError('Error: read json. ' + str(e))
	try:
		auth.authenticate_user(username, password)
		return 'Successful authentication.'
	except Exception as e:
		raise ValueError(str(e))

@app.route('/authenticate_user_teacher', methods = ['POST']) 
def authenticate_user_teacher():
	auth = Authentication(table = 'users_teachers')
	try:
		username = request.json['username']
		password = request.json['password']
	except Exception as e:	
		raise ValueError('Error: read json. ' + str(e))
	try:
		auth.authenticate_user(username, password)
		return 'Successful authentication.'
	except Exception as e:
		raise ValueError(str(e))


def main():
 	port = int(os.environ.get('PORT', 5050))
 	app.run(host = '0.0.0.0', port = port,debug=True)   

if __name__ == '__main__':
	verify_master_user()
	main()