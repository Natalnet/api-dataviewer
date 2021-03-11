import sqlalchemy as sql
import pandas as pd
import psycopg2 
import os

#Esta classe possibilita manipular o banco de dados postgresql, seja fazendo querys ou inserções no banco

#Classe com parâmetros de configuração da conexão
class Config:
	def __init__(self):
		self.conn_params_dic = {
		    'host'      : 'localhost',
		    'database'  : 'dataview_bd',
		    'user'      : 'postgres',
		    'port'      : '5432',
		    'password'  : 'root'

		    ''' pronta pra utilizar variaveis de ambiente
		    'host'      : os.environ['HOST_DB'],
		    'database'  : os.environ['DATABASE_DB'],
		    'user'      : os.environ['USER_DB'],
		    'port'      : os.environ['PORT_DB'],
		    'password'  : os.environ['PASSWORD_DB']
		    '''
		}
		#'postgresql+psycopg2://usuario:senha@ip-servidor:porta/banco-de-dados'
		self.connect_alchemy = "postgresql+psycopg2://%s:%s@%s:%s/%s" % (
		    self.conn_params_dic['user'],
		    self.conn_params_dic['password'],
		    self.conn_params_dic['host'],
		    self.conn_params_dic['port'],
		    self.conn_params_dic['database']
		)	

class Manage_db(Config):
	def __init__(self):
		Config.__init__(self)
		try:
			#Estabelece a conexão com os dados da classe config
			self.engine = sql.create_engine(self.connect_alchemy, convert_unicode=True, client_encoding='utf8')
		except Exception as e:
			print('Connection error', e)

	def search(self, table, columns = '*', condition = None):
		#Selecionamos sempre todas as colunas pois demandamos de todas elas
		try:
			#Se a query vem com uma condição específica de consulta
			if condition:#mudei removi a condicao where q tava como string
				query = f'SELECT {columns} FROM {table} {condition}'
			else:	
				query = f'SELECT {columns} FROM {table}' 
			return pd.read_sql_query(query, self.engine)
		except Exception as e:
			print('Query error', e)

	def insert_df(self, table, df):
		try:
			#Insere no banco de dados os dados a partir de um dataframe
			df.to_sql(
				name      =  table,
				con       =  self.engine,
				index     =  False,
				if_exists = 'append'
				)
		except Exception as e:
			print('Insert error', e)

'''	
psql = Manage_db()
data={'cod_cliente': [5], 'nome_cliente': ['Rogerio'], 'sobrenome_cliente':['Ceni']}
df = pd.DataFrame(data)
psql.insert_df(table = 'clientes', df=df)
print(psql.search(table='clientes'))
'''
