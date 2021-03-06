from flask import Flask, request
from flask_cors import CORS
import numpy as np
import pandas as pd
import os
import re
from datetime import datetime
from classes.lop import Lop
from classes.psql import Manage_db
import urllib3
import json
import time
urllib3.disable_warnings()
#import sklearn

#Instanciando classes
lop = Lop()
psql = Manage_db()

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
    return 'REST API do DataView'

#get classes
@app.route('/get_class', methods = ['GET'])  
def get_class():
  try:
    df_class = psql.search(table='teacher', condition=None)
    json_classes = df_class.to_json(force_ascii = False, orient = 'records')
    return json_classes
  except:
    return 'Error: reading df class'

@app.route('/get_question_data', methods = ['GET'])  
def get_question_data():
  try:
    df_question_data = psql.search(table='question', condition=None)
    json_questions = df_question_data.to_json(force_ascii = False, orient = 'records')
    return json_questions
  except:
    return 'Error: reading df question data'

@app.route('/get_graphs/<id_class>', methods = ['GET'])
def get_graphs(id_class):
  #collect data
  data = pd.DataFrame([id_class], columns = ['id_class'])
  key = lop.read_txt('key/key.txt')
  endpoint_lists_tests = lop.read_txt('endpoints/endpoint_lists_tests.txt')
  try:
    condition = "id_class = '" + data.iloc[0,0] + "'"
    df_submission = psql.search(table='submission', condition=condition)
    df_lop_lists = lop.lop_lists(endpoint_lists_tests, data, key)
    df_lop_tests = lop.lop_tests(endpoint_lists_tests, data, key)    
  except:
    return 'Error: connection refused by server'
  #Se não tiver nenhuma submissão na turma
  if df_submission.empty:
    return 'Error: class without data'
  df_question_data = psql.search(table='question', condition=None)
  df_questions_selected = lop.select_questions(df_question_data, df_lop_lists, df_lop_tests)
  df_class = psql.search(table='teacher', condition=None)
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
  except:
    return 'Error: generate data lists'
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
      return 'Error: insert empty in data tests'
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
      return 'Error: generate data tests'
  #Histograma do dias gastos para concluir uma lista/assunto/dificuldade
  try:
    GTDGL = lop.graph_days_spent_list(df_submission)
    GTDGA = lop.graph_days_spent_subject(df_submission, df_questions_selected)
    GTDGD = lop.graph_days_spent_difficulty(df_submission, df_questions_selected)
  except:
    return 'Error: generate graph days spent per list/subject/difficulty' 
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

def main():
  port = int(os.environ.get('PORT', 5000))
  app.run(host = '0.0.0.0', port = port,debug=True)   

if __name__ == '__main__':
  main()