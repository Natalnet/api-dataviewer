from flask import Flask, request
from flask_cors import CORS
import numpy as np
import pandas as pd
import os
import re
from datetime import datetime
from classes.manage_lop import Lop
from classes.manage_db import Manage_db
from classes.manage_authentication import Authentication
import urllib3
import json
import time
import warnings
warnings.filterwarnings('ignore')
urllib3.disable_warnings()
#import sklearn

#Lendo variáveis de ambiente
PASSWORD_DB = os.getenv('PASSWORD_DB')
USER_DB = os.getenv('USER_DB')

#Instanciando classes
lop = Lop()
psql = Manage_db(database = 'dataviewer_lop', port = '5432', host = 'db-lop', 
                 user = USER_DB, password = PASSWORD_DB)

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
    return 'REST API do DataViewer'

#get classes
@app.route('/get_classes', methods = ['GET'])  
def get_classes():
  try:
    df_class = psql.search(table='teachers_classes')
    json_classes = df_class.to_json(force_ascii = False, orient = 'records')
    return json_classes
  except Exception as e:
    raise ValueError('Error: reading table classes, ' + str(e))

@app.route('/get_questions', methods = ['GET'])  
def get_questions():
  try:
    df_question_data = psql.search(table='questions')
    json_questions = df_question_data.to_json(force_ascii = False, orient = 'records')
    return json_questions
  except Exception as e:
    raise ValueError('Error: reading table questions, ' + str(e))

@app.route('/get_lists', methods = ['GET'])  
def get_lists():
  try:
    df_lists = psql.search(table='lists')
    json_lists = df_lists.to_json(force_ascii = False, orient = 'records')
    return json_lists
  except Exception as e:
    raise ValueError('Error: reading table lists, ' + str(e))

@app.route('/get_tests', methods = ['GET'])  
def get_tests():
  try:
    df_tests = psql.search(table='tests')
    json_lists = df_lists.to_json(force_ascii = False, orient = 'records')
    return json_lists
  except Exception as e:
    raise ValueError('Error: reading table lists, ' + str(e))

@app.route('/get_submissions/<id_class>', methods = ['GET'])
def get_submissions(id_class):
  #collect data
  data = pd.DataFrame([id_class], columns = ['id_class'])
  try:
    condition = "WHERE id_class = '" + data.iloc[0,0] + "'"
    df_submission = psql.search(table='submissions', condition=condition)
    json_submission = df_submission.to_json(force_ascii = False, orient = 'records')
    return json_submission
  except Exception as e:
    raise ValueError('Error: reading table submissions')
        
@app.route('/post_graphs', methods = ['POST'])
def post_graphs():
  try:
    id_class = request.json['id_class']
    user_api = request.json['user_api']
    password_user_api = request.json['password_user_api']
  except Exception as e:
    raise ValueError('Error: read json. ' + str(e))
  #Verifica se o usuário mestre passado no post é o que permite
  #cadastro no banco de dados, se for correto, o cadastro do usuário 
  #prossegue
  try:
    auth_users_api = Authentication(table = 'users_api')
    auth_users_api.authenticate_user(user_api, password_user_api)
  except Exception as e:
    raise ValueError(str(e))
  #Cria o dataframe com a turma informada
  data = pd.DataFrame([id_class], columns = ['id_class'])
  try:
    condition = "WHERE id_class = '" + data.iloc[0,0] + "'"
    df_submission = psql.search(table='submissions', condition = condition)
    df_lop_lists = psql.search(table='lists', condition = condition)
    df_lop_tests = psql.search(table='tests', condition = condition) 
    df_question_data = psql.search(table='questions')
    df_class = psql.search(table='teachers_classes')
  except Exception as e:
    raise ValueError('Error: consult at database. ' + str(e))
  #Se não tiver nenhuma submissão na turma
  if df_submission.empty:
    raise ValueError('Error: class without data')
  #Selecionando apenas as questões dessa turma
  df_questions_selected = lop.select_questions(df_question_data, df_lop_lists, df_lop_tests)
  #Dados de lista
  try:
    #Dados de performance
    df_performance_list = lop.performance_list_test(df_submission, 'list', df_lop_lists, df_lop_tests, df_question_data)
    df_performance_difficulty_list = lop.performance_difficulty_list_test(df_submission, df_questions_selected,'list')
    df_performance_subject_list = lop.performance_subject_list_test(df_submission, df_questions_selected, 'list')
    #Grafico 1, desempenho por turma analisando notas
    GENL = lop.graph_more_less_list_test_class(df_performance_list, df_class, data, 70.0, 'list')
    GTDL = lop.graph_more_less_difficulty_list_test_class(df_performance_difficulty_list, df_class, data, 70.0)
    GTAL = lop.graph_more_less_subject_list_test_class(df_performance_subject_list, df_class, data, 70.0)
    #Grafico 2, desempenho por aluno analisando notas
    GTNL = lop.graph_performance_student_list_test(df_performance_list, df_class, data, 'list')
    GEDL = lop.graph_performance_student_difficulty_list_test(df_performance_difficulty_list, df_class, data)
    GEAL = lop.graph_performance_student_subject_list_test(df_performance_subject_list, data, df_class)
    #Média geral dos alunos 
    media_GTNL = lop.media_graph_performance_student_list_test(df_performance_list, df_questions_selected, 'list')
    media_GEDL = lop.media_graph_performance_student_difficulty_list_test(df_performance_difficulty_list, df_questions_selected)
    media_GEAL = lop.media_graph_performance_subject_list_test(df_performance_subject_list)
  except Exception as e:
    raise ValueError('Error: generate data lists. ' + str(e))
  #Se não tiver nenhuma prova cadastrada  
  if df_lop_tests.empty:
    #Insere vazio e não realiza a geração dos dados
    try:
      #Grafico 1, desempenho por turma analisando notas
      GENP = json.dumps([{}])
      GTDP = json.dumps([{}])
      GTAP = json.dumps([{}])
      #Grafico 2, desempenho por aluno analisando notas
      GTNP = json.dumps([{}])
      GEDP = json.dumps([{}])
      GEAP = json.dumps([{}])
      #Média geral dos alunos 
      media_GTNP = json.dumps([{}])
      media_GEDP = json.dumps([{}])
      media_GEAP = json.dumps([{}])
    except:
      raise ValueError('Error: insert empty in data tests')
  #Se existe provas cadastradas, gera os dados normalmente      
  else:
    try:
      df_performance_test = lop.performance_list_test(df_submission, 'test', df_lop_lists, df_lop_tests, df_question_data)
      df_performance_difficulty_test = lop.performance_difficulty_list_test(df_submission, df_questions_selected,'test')
      df_performance_subject_test = lop.performance_subject_list_test(df_submission, df_questions_selected, 'test')
      #Grafico 1, desempenho por turma analisando notas
      GENP = lop.graph_more_less_list_test_class(df_performance_test, df_class, data, 70.0, 'test')
      GTDP = lop.graph_more_less_difficulty_list_test_class(df_performance_difficulty_test, df_class, data, 70.0)
      GTAP = lop.graph_more_less_subject_list_test_class(df_performance_subject_test, df_class, data, 70.0)
      #Grafico 2, desempenho por aluno analisando notas
      GTNP = lop.graph_performance_student_list_test(df_performance_test, df_class, data, 'test')
      GEDP = lop.graph_performance_student_difficulty_list_test(df_performance_difficulty_test, df_class, data)
      GEAP = lop.graph_performance_student_subject_list_test(df_performance_subject_test, data, df_class)
      #Média geral dos alunos 
      media_GTNP = lop.media_graph_performance_student_list_test(df_performance_test, df_questions_selected, 'test')
      media_GEDP = lop.media_graph_performance_student_difficulty_list_test(df_performance_difficulty_test, df_questions_selected)
      media_GEAP = lop.media_graph_performance_subject_list_test(df_performance_subject_test)
    except:
      raise ValueError('Error: generate data tests')
  #Histograma do dias gastos para concluir uma lista/assunto/dificuldade
  try:
    GTDGL = lop.graph_days_spent_list(df_submission)
    GTDGA = lop.graph_days_spent_subject(df_submission, df_questions_selected)
    GTDGD = lop.graph_days_spent_difficulty(df_submission, df_questions_selected)
  except:
    raise ValueError('Error: generate graph days spent per list/subject/difficulty')
  #Transformando em um só json
  name_graphs = ['"GENL"','"GENP"','"GTDL"','"GTDP"','"GTAL"','"GTAP"',
                 '"GTNL"','"GTNP"','"GEDL"','"GEDP"','"GEAL"','"GEAP"',
                 '"media_GTNL"','"media_GTNP"','"media_GEDL"','"media_GEDP"','"media_GEAL"','"media_GEAP"',
                 '"GTDGL"','"GTDGA"','"GTDGD"']
  graphs =      [GENL,GENP,GTDL,GTDP,GTAL,GTAP,
                 GTNL,GTNP,GEDL,GEDP,GEAL,GEAP,
                 media_GTNL,media_GTNP,media_GEDL,media_GEDP,media_GEAL,media_GEAP,
                 GTDGL,GTDGA,GTDGD]
  return lop.create_unique_json(name_graphs, graphs)



@app.route('/get_graphs_teacher/<id_class>', methods = ['GET'])
def get_graphs(id_class):
  #collect data
  data = pd.DataFrame([id_class], columns = ['id_class'])
  try:
    condition = "WHERE id_class = '" + data.iloc[0,0] + "'"
    df_submission = psql.search(table='submissions', condition=condition)
    df_lop_lists = psql.search(table='lists', condition=condition)
    df_lop_tests = psql.search(table='tests', condition=condition) 
    df_question_data = psql.search(table='questions')
    df_class = psql.search(table='teachers_classes')
  except Exception as e:
    raise ValueError('Error: consult at database. ' + str(e))
  #Se não tiver nenhuma submissão na turma
  if df_submission.empty:
    raise ValueError('Error: class without data')
  #Selecionando apenas as questões dessa turma
  df_questions_selected = lop.select_questions(df_question_data, df_lop_lists, df_lop_tests)
  #Dados de lista
  try:
    #Dados de performance
    df_performance_list = lop.performance_list_test(df_submission, 'list', df_lop_lists, df_lop_tests, df_question_data)
    df_performance_difficulty_list = lop.performance_difficulty_list_test(df_submission, df_questions_selected,'list')
    df_performance_subject_list = lop.performance_subject_list_test(df_submission, df_questions_selected, 'list')
    #Grafico 1, desempenho por turma analisando notas
    GENL = lop.graph_more_less_list_test_class(df_performance_list, df_class, data, 70.0, 'list')
    GTDL = lop.graph_more_less_difficulty_list_test_class(df_performance_difficulty_list, df_class, data, 70.0)
    GTAL = lop.graph_more_less_subject_list_test_class(df_performance_subject_list, df_class, data, 70.0)
    #Grafico 2, desempenho por aluno analisando notas
    GTNL = lop.graph_performance_student_list_test(df_performance_list, df_class, data, 'list')
    GEDL = lop.graph_performance_student_difficulty_list_test(df_performance_difficulty_list, df_class, data)
    GEAL = lop.graph_performance_student_subject_list_test(df_performance_subject_list, data, df_class)
    #Média geral dos alunos 
    media_GTNL = lop.media_graph_performance_student_list_test(df_performance_list, df_questions_selected, 'list')
    media_GEDL = lop.media_graph_performance_student_difficulty_list_test(df_performance_difficulty_list, df_questions_selected)
    media_GEAL = lop.media_graph_performance_subject_list_test(df_performance_subject_list)
    #Gráfico 4, analise de questões e listas por tempo pra turma e alunos
    GTTMQQMDD = lop.graph_max_different_days_time(df_submission)
    GTTMDDL = lop.max_day_time(df_submission)
    GATGQTDD = lop.df_user_secounds_days(df_submission)
    GTTGQSQ = lop.df_questions_secounds(df_submission)    
  except Exception as e:
    raise ValueError('Error: generate data lists. ' + str(e))
  #Se não tiver nenhuma prova cadastrada  
  if df_lop_tests.empty:
    #Insere vazio e não realiza a geração dos dados
    try:
      #Grafico 1, desempenho por turma analisando notas
      GENP = json.dumps([{}])
      GTDP = json.dumps([{}])
      GTAP = json.dumps([{}])
      #Grafico 2, desempenho por aluno analisando notas
      GTNP = json.dumps([{}])
      GEDP = json.dumps([{}])
      GEAP = json.dumps([{}])
      #Média geral dos alunos 
      media_GTNP = json.dumps([{}])
      media_GEDP = json.dumps([{}])
      media_GEAP = json.dumps([{}])
      #Gráfico 4, analise de questões e listas por tempo pra turma e alunos
      GTTMQQMDD = json.dumps([{}])
      GTTMDDL = json.dumps([{}])
      GATGQTDD = json.dumps([{}])
      GTTGQSQ = json.dumps([{}])
    except:
      raise ValueError('Error: insert empty in data tests')
  #Se existe provas cadastradas, gera os dados normalmente      
  else:
    try:
      df_performance_test = lop.performance_list_test(df_submission, 'test', df_lop_lists, df_lop_tests, df_question_data)
      df_performance_difficulty_test = lop.performance_difficulty_list_test(df_submission, df_questions_selected,'test')
      df_performance_subject_test = lop.performance_subject_list_test(df_submission, df_questions_selected, 'test')
      #Grafico 1, desempenho por turma analisando notas
      GENP = lop.graph_more_less_list_test_class(df_performance_test, df_class, data, 70.0, 'test')
      GTDP = lop.graph_more_less_difficulty_list_test_class(df_performance_difficulty_test, df_class, data, 70.0)
      GTAP = lop.graph_more_less_subject_list_test_class(df_performance_subject_test, df_class, data, 70.0)
      #Grafico 2, desempenho por aluno analisando notas
      GTNP = lop.graph_performance_student_list_test(df_performance_test, df_class, data, 'test')
      GEDP = lop.graph_performance_student_difficulty_list_test(df_performance_difficulty_test, df_class, data)
      GEAP = lop.graph_performance_student_subject_list_test(df_performance_subject_test, data, df_class)
      #Média geral dos alunos 
      media_GTNP = lop.media_graph_performance_student_list_test(df_performance_test, df_questions_selected, 'test')
      media_GEDP = lop.media_graph_performance_student_difficulty_list_test(df_performance_difficulty_test, df_questions_selected)
      media_GEAP = lop.media_graph_performance_subject_list_test(df_performance_subject_test)
    except:
      raise ValueError('Error: generate data tests')
  #Histograma do dias gastos para concluir uma lista/assunto/dificuldade
  try:
    GTDGL = lop.graph_days_spent_list(df_submission)
    GTDGA = lop.graph_days_spent_subject(df_submission, df_questions_selected)
    GTDGD = lop.graph_days_spent_difficulty(df_submission, df_questions_selected)
  except:
    raise ValueError('Error: generate graph days spent per list/subject/difficulty')
  #Transformando em um só json
  name_graphs = ['"GENL"','"GENP"','"GTDL"','"GTDP"','"GTAL"','"GTAP"',
                 '"GTNL"','"GTNP"','"GEDL"','"GEDP"','"GEAL"','"GEAP"',
                 '"media_GTNL"','"media_GTNP"','"media_GEDL"','"media_GEDP"','"media_GEAL"','"media_GEAP"',
                 '"GTDGL"','"GTDGA"','"GTDGD"',
                 '"GTTMQQMDD"','"GTTMDDL"','"GATGQTDD"','"GTTGQSQ"']
  graphs =      [GENL,GENP,GTDL,GTDP,GTAL,GTAP,
                 GTNL,GTNP,GEDL,GEDP,GEAL,GEAP,
                 media_GTNL,media_GTNP,media_GEDL,media_GEDP,media_GEAL,media_GEAP,
                 GTDGL,GTDGA,GTDGD,
                 GTTMQQMDD,GTTMDDL,GATGQTDD,GTTGQSQ]
  return lop.create_unique_json(name_graphs, graphs)

def main():
  port = int(os.environ.get('PORT', 5000))
  app.run(host = '0.0.0.0', port = port)   

if __name__ == '__main__':
  main()
