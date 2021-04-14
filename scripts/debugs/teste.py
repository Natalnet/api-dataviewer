import urllib3
import json


# teste 1 - registrar usuario da api

data = {'username': 'frontend',
		'password': '123',
		'user_api': 'Master',
		'password_user_api': 'root'}
encoded_data = json.dumps(data).encode('utf-8')

http = urllib3.PoolManager()
req = http.request('POST','http://localhost:5050/register_user_api',
					headers={'Content-Type': 'application/json'},					
					body= encoded_data
					)
print(req.status)


# teste 2 - registrar prof

data = {'username': 'orivaldo',
		'password': 'senha-orivaldo',
		'name_teacher' : 'Orivaldo Viera',
		'id_teacher' : 'c0b8b2c2-5709-47e2-ab22-f22e19b7e0b1',
		'email' : 'orivaldo@gmail.com',
		'user_api': 'frontend',
		'password_user_api': '123'}
encoded_data = json.dumps(data).encode('utf-8')

http = urllib3.PoolManager()
req = http.request('POST','http://localhost:5050/register_user_teacher',
					headers={'Content-Type': 'application/json'},					
					body= encoded_data
					)
print(req.status)

# teste 3 - registrar aluno

data = {'user': 'meuusernolop',
		'username': 'joao',	
		'password': 'senha-joao',
		'name' : 'João do LoP',
		'registration' : '20201234',
		'email' : 'joao-do-lop@gmail.com',
		'user_api': 'frontend',
		'password_user_api': '123'}
encoded_data = json.dumps(data).encode('utf-8')

http = urllib3.PoolManager()
req = http.request('POST','http://localhost:5050/register_user_student',
					headers={'Content-Type': 'application/json'},					
					body= encoded_data
					)
print(req.status)

# teste 4 - autenticação prof

data = {'username': 'orivaldo',
		'password': 'senha-orivaldo'}
encoded_data = json.dumps(data).encode('utf-8')

http = urllib3.PoolManager()
req = http.request('POST','http://localhost:5050/authenticate_user_teacher',
					headers={'Content-Type': 'application/json'},					
					body= encoded_data
					)
print(req.status)

# teste 5 - autenticacao aluno


data = {'username': 'joao',
		'password': 'senha-joao'}
		
encoded_data = json.dumps(data).encode('utf-8')

http = urllib3.PoolManager()
req = http.request('POST','http://localhost:5050/authenticate_user_student',
					headers={'Content-Type': 'application/json'},					
					body= encoded_data
					)
print(req.status)

# teste 6 - requisicao de dados

data = {'id_class': 'e3f64e38-4810-4708-ab83-091c0b8791ff',
		'user_api': 'frontend',
		'password_user_api': '123'}

encoded_data = json.dumps(data).encode('utf-8')

http = urllib3.PoolManager()
req = http.request('POST','http://localhost:5000/post_graphs',
					headers={'Content-Type': 'application/json'},					
					body= encoded_data
					)
print(req.data)
print(req.status)
