import sqlalchemy as sql
import pandas as pd
import psycopg2 
import os

#Esta classe possibilita manipular o banco de dados postgresql, seja fazendo querys ou inserções no banco

#Classe com parâmetros de configuração da conexão

os.environ['USER_DB'] = 'postgres'
os.environ['PASSWORD_DB'] = 'root'

class Config:
	def __init__(self, database, host, port):
		self.conn_params_dic = {
		    'host'      :  host,
		    'database'  :  database,
		    'user'      :  os.environ['USER_DB'],
		    'port'      :  port,
		    'password'  :  os.environ['PASSWORD_DB']

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
	def __init__(self, database, host, port):
		Config.__init__(self, database, host, port)
		try:
			#Estabelece a conexão com os dados da classe config
			self.engine = sql.create_engine(self.connect_alchemy, convert_unicode=True, client_encoding='utf8')
		except Exception as e:
			raise ValueError('Error: failed to establish connection. ' + str(e))

	def search(self, table, columns = '*', condition = None):
		#Selecionamos sempre todas as colunas pois demandamos de todas elas
		try:
			#Se a query vem com uma condição específica de consulta
			if condition:
				query = f'SELECT {columns} FROM {table} {condition}'
			else:	
				query = f'SELECT {columns} FROM {table}' 
			return pd.read_sql_query(query, self.engine)
		except Exception as e:
			raise ValueError('Error: consult recused. ' + str(e))

	def insert_df(self, table, df):
		try:
			#Insere no banco de dados os dados a partir de um dataframe
			df.to_sql(
				name      =  table,
				con       =  self.engine,
				index     =  False,
				if_exists = 'append'
			)
			return True
		except Exception as e:
			raise ValueError('Error: inserting dataframe. ' + str(e))

	#Função para atualizar um cadastro com base em uma condição
	#Se o novo dado for string necessita inserir aspas simples no dado
	#Ex: cachorro, uma string, terá que vir como 'cachorro'
	def update(self, table, column_new_data, column_reference, new_data, data_reference):
		connect = self.engine
		#Insere aspas
		column_new_data = '"' + column_new_data + '"'
		column_reference = '"' + column_reference + '"'
		query = f'UPDATE {table} SET {column} = {new_data} WHERE {column_reference} = {data_reference}'
		try:
			with connect.begin() as conn:
				conn.execute(query)
		except Exception as e:
			raise ValueError('Error: update. ' + str(e))

	#Deleta registros a partir de uma condição
	#Mesmo caso da de update, se for string necessita vir entre aspas simples
	def delete(self, table, column, data_reference):
		connect = self.engine
		query = f'DELETE FROM {table} WHERE {column} = {data_reference}'
		try:
			with connect.begin() as conn:
				conn.execute(query)		    
		except Exception as e:
			raise ValueError('Error: delete. ' + str(e))