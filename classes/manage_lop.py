import pandas as pd
import numpy as np
import re
import json
import urllib3
from datetime import datetime
urllib3.disable_warnings()

#Classe responsável por realizar consultas na API da plataforma LoP e também por geração de dados

class Lop:
  
  def __init__(self):
    pass
    

  def read_txt(self, path):
    with open(path,'r') as file:
      return file.read()


  #----------------------------------------------------------------------------Funções de Consulta no LoP-------------------------------------


  def lop_consult(self, url):
    #Instancia o urllib3
    http = urllib3.PoolManager()
    #Realização uma requisição GET na url
    req = http.request('GET',url,timeout=7.0)
    #Se for correta, os dados são convertidos em dataframe
    if req.status == 200:
      return pd.read_json(req.data, orient = 'RECORDS', encoding = 'utf-8').copy()
    #Se não, retorna falso      
    else: 
      return False    

  #Modificação em relação a função original, aqui precisar passar por parâmetro o endpoint e a key    
  def lop_question(self, endpoint_question, key):
    #Data do primeiro registro
    date = '2020-01-01'
    #Formação da url
    url_question = endpoint_question + key + '&createdAt=' + date
    df_question = self.lop_consult(url_question)
    df_question.rename(columns = {'id':'id_question','title':'question'}, inplace = True)
    return df_question

  def lop_question_db(self, endpoint_all_questions, key, date):
    #Formação da url
    url_questions = endpoint_all_questions + key + '&createdAt=' + date
    #Consulta na API do LoP
    df_questions = self.lop_consult(url_questions)
    #Renomeando campos
    df_questions.rename(columns = {'id':'id_question','title':'question'}, inplace = True)
    return df_questions

  #Modificação em relação a função original, aqui precisar passar por parâmetro o endpoint e a key  
  def question_data(self, endpoint_question = '', key = '', df_question = pd.DataFrame()):
    #Essa função se passar por cópia o df_question se torna desnecessário fazer a requisição de todas as turmas usando a função lop_question()
    #Dataframes onde serão armazenados todas as questões transformadas
    df_list_data = pd.DataFrame()  
    df_test_data = pd.DataFrame() 
    df_tag_data = pd.DataFrame()  
    df_question_data = pd.DataFrame()  
    if df_question.empty == True:
      df_question = self.lop_question(endpoint_question,key)
    for question,lists,tests,tags,difficulty,createdAt in zip(df_question['question'],df_question['lists'],df_question['tests'],df_question['tags'],df_question['difficulty'],df_question['createdAt']):
      #Cada registro do json pode ficar com mais de uma lista associada a uma questão, por isso a necessidade de extrair
      df_prov_lists  = pd.DataFrame(json.loads(str(lists).replace("'",'"')))
      #Cada registro do json pode ficar com mais de uma lista associada a uma questão, por isso a necessidade de extrair
      df_prov_tests  = pd.DataFrame(json.loads(str(tests).replace("'",'"')))
      #df_prov_lists.rename(columns = {'id':'id_list','title':'list'}, inplace = True)
      #Inserindo a questão associada
      df_prov_lists['question'] = question
      df_prov_lists['difficulty'] = difficulty
      df_prov_lists['createdAt'] = createdAt
      df_list_data = df_list_data.append(df_prov_lists, ignore_index = True).copy()
      #print(df_list_data['question'])
      #print("numero de questoes unicas no df ",len(df_list_data['question'].unique()))
      df_prov_tests['question'] = question
      df_prov_tests['difficulty'] = difficulty
      df_prov_tests['createdAt'] = createdAt
      df_test_data = df_test_data.append(df_prov_tests, ignore_index = True).copy()
      #Extraindo as tags, que vão dizer o conteudo associado
      df_prov_tags = pd.DataFrame(json.loads(str(tags).replace("'",'"'))).T
      #Inserindo a questão associada
      df_prov_tags['question'] = question    
      df_tag_data = df_tag_data.append(df_prov_tags, ignore_index = True).copy()
    
    df_list_data.rename(columns = {'id':'id_list','title':'list'}, inplace = True)
    df_test_data.rename(columns = {'id':'id_test','title':'test'}, inplace = True)
    #print(len(df_list_data['question'].unique()))
    #df_list_data['difficulty'] = df_list_data['difficulty'].astype('int')
    columns_tags = ['question']
    for i in range(len(df_tag_data.columns)-1): columns_tags.append('tag'+str(i+1))
    df_tag_data.columns = columns_tags
    df_list_data = pd.merge(df_list_data, df_tag_data, on = 'question', how = 'outer')#.fillna(0)
    df_test_data = pd.merge(df_test_data, df_tag_data, on = 'question', how = 'outer')#.fillna(0)
    df = pd.concat([df_list_data, df_test_data],axis=0).copy()
    return df.sort_values(by = 'createdAt')


  #Modificação em relação a função original, aqui precisar passar por parâmetro o endpoint e a key    
  def lop_class(self, endpoint_class, endpoint_teacher, key, df_teacher = pd.DataFrame()):
    #Essa função se passar por cópia o df_teacher se torna desnecessário fazer a requisição de todas os professores, e evitando fazer varias consultas
    #Dataframe onde será armazenado todas as turmas
    df_class = pd.DataFrame()
    if df_teacher.empty == True:
      #Formação da url de consulta para saber os professores cadastrados no LoP
      url_teacher = endpoint_teacher + key
      #Realizando a consulta no LoP
      df_teacher = self.lop_consult(url_teacher)#id, email, name
    #O laço faz uma varredura das turmas de cada professor e por fim armazena em um dataframe de turmas
    for id_teacher, name_teacher in zip(df_teacher['id'],df_teacher['name']):
      #O LoP.v2 foi desenvolvido em 2019, então temos que capturar as turmas entre 2019 e o ano atual
      current_year = datetime.now().year
      for year in range(2019, current_year + 1):
        #Por fim precisamos do semestre que deve ser 1 ou 2
        for semester in range(1,3): 
          try:
            #Url de consulta de classes
            url_class = endpoint_class + id_teacher + '?year=' + str(year) + '&semester=' + str(semester) + '&key=' + key 
            #Dataframe provisório necessário para capturar o tamanho e saber quantas turmas esse professor tem que estar associado
            df_prov = self.lop_consult(url_class)
            #Inserindo o id e o nome do professor no dataframe de turmas
            df_prov['id_teacher'] = id_teacher
            df_prov['name_teacher'] = name_teacher
            #Adicionando turmas conforme novas consultas
            df_class = df_class.append(df_prov, ignore_index=True).copy()#id, name, code, year, semester, id_teacher
          except:
            pass
    #Renomeando colunas com nomes semelhantes em todos os DF
    df_class.rename(columns={'id':'id_class','name':'name_class'}, inplace = True)
    return df_class

  def lop_class_db(self, endpoint_all_classes, endpoint_teacher, key, date):
    #Formação da url
    url_classes = endpoint_all_classes + key + '&createdAt=' + date
    #Consultando no LoP
    df_classes = self.lop_consult(url_classes)
    #Renomenado para manter antigo padrão
    df_classes.rename(columns = {'id':'id_class','name':'name_class','author_id':'author'}, inplace = True)
    df = pd.DataFrame()
    for row in df_classes.iterrows():
      for id_teacher in row[1]['teachers']:
        #Insere o prof da turma na série
        row[1]['id_teacher'] = id_teacher
        #Concatena no novo dataframe a turma com o professor
        df = df.append(row[1])
    try:
      if df == False:
        raise ValueError('Connection recused')
    except:
      pass
    try:
      if df.empty:
        return df
      else:
        df.drop(columns='teachers', inplace = True)
        #Formação da url de professor
        url_teacher = endpoint_teacher + key      
        #Coletando na rota de professores o nome do professor
        df_teacher = self.lop_consult(url_teacher)
        #Renomeando
        df_teacher.rename(columns={'id':'id_teacher','name':'name_teacher'}, inplace = True)
        #Pegando apenas os campos de interesse
        #df_teacher = df_teacher[['id_teacher','name_teacher']]
        #Juntando no campo id_teacher a tabela das turmas com o nome do professor
        df = df.merge(df_teacher, on = 'id_teacher', how = 'inner')
        #Ordenando pela data de criação da turma
        df = df.sort_values(by = 'createdAt')
        return df
    except:
      pass


  #Modificação em relação a função original, aqui precisar passar por parâmetro o endpoint e a key  
  def lop_submission(self, endpoint_submission, endpoint_class, endpoint_teacher, key, df_class = pd.DataFrame()):
    #Essa função se passar por cópia o df_class se torna desnecessário fazer a requisição de todas as turmas usando a função lop_class()
    #Dataframe onde serão armazenados todas as submissões 
    df_submission = pd.DataFrame()  
    if df_class.empty == True:
      df_class = self.lop_class(endpoint_class, endpoint_teacher, key)  
    #Obtem todas as submissões da lista de turmas passadas
    for id_class in df_class['id_class']:
      #Url da consulta as submissões
      url_submission = endpoint_submission + id_class + '/submission?key=' + key
      #Dataframe provisório que vai armazenar o resultado da consulta
      df_prov = self.lop_consult(url_submission)
      #Inserindo o id_class no dataframe de consultas
      df_prov['id_class'] = id_class
      #Adicionando submissões conforme consultas
      df_submission = df_submission.append(df_prov, ignore_index=True).copy()
    #Campo user trás matricula e o nome do usuário, vamos separar em 2 colunas distintas
    df_submission[['user','registration']] = df_submission['user'].str.split('-',expand=True)
    return df_submission

  def lop_submission_db(self, endpoint_all_submissions, key, date, date_limit = ''):
    #Date é o parâmetro que informa a última data presente no banco.
    #A função vai pegar dali pra frente
    #Importante: se você estiver usando essa função sem o uso do banco de dados, se 
    #certifique de passar uma data como string
    #Já date_limit é o da máximo que você 
    #Montagem da url
    url_all_submissions = endpoint_all_submissions + key + '&createdAt=' + date
    #Se o campo não estiver vazio
    if date_limit != '':
      #Inseri a data que limita a consulta
      url_all_submissions = url_all_submissions + '&untilAt=' + date_limit
      print(url_all_submissions)
    #Realizando requisição
    df_submissions = self.lop_consult(url_all_submissions)
    #Caso retorne vazio não faz sentido aplicar a ordenação, apenas retorna
    try:
      if df_submissions == False:
        raise ValueError('Connection recused')
    except:
      pass
    try:
      if df_submissions.empty:
        return df_submissions
      else:
        #Os dados estão vindo em ordem decrescente necessita reeordenar
        df_submissions = df_submissions.sort_values(by='createdAt')
        df_submissions.rename(columns={'enrollment':'registration'}, inplace = True)
        return df_submissions
    except:
      return

  def lop_lists(self, endpoint_all_lists, key, data = pd.DataFrame()):#Data é a turma em dataframe
    #Data do primeiro registro
    date = '2020-01-01'
    #Formação da url
    url_lists = endpoint_all_lists + key + '&createdAt=' + date
    #Consultando no LoP todas as listas cadastradas até hoje
    df_lop_lists = self.lop_consult(url_lists)
    #Renomeando campos
    df_lop_lists.rename(columns = {'id':'id_list','title':'list'}, inplace = True)
    #Caso eu não queira listas de somente de uma turma    
    if data.empty:      
      return df_lop_lists
    else: 
      #Retornando apenas as listas cadastradas numa turma
      return df_lop_lists.loc[df_lop_lists['id_class'].str.contains(data.iloc[0,0])].copy()
  
  def lop_lists_db(self, endpoint_all_lists, key, date):
    #Onde date é data que vai servir de início na consulta
    #Montagem da url
    url_lists = endpoint_all_lists + key + '&createdAt=' + date
    #Consultando as listas a partir da data 
    df_lop_lists = self.lop_consult(url_lists)
    try:
      if df_lop_lists == False:
        raise ValueError('Connection recused')
    except:
      pass
    try:
      if df_lop_lists.empty:
        return df_lop_lists
      else:
        #Removendo o author da prova
        df_lop_lists.drop(columns = 'author', inplace = True)
        #Renomeando campos
        df_lop_lists.rename(columns = {'id':'id_list','title':'list'}, inplace = True)
        #Os dados estão vindo em ordem decrescente necessita reeordenar
        df_lop_lists = df_lop_lists.sort_values(by='createdAt')
        return df_lop_lists
    except:
      return

  def lop_tests(self, endpoint_tests, key, data = pd.DataFrame()):#Data é a turma em dataframe
    #Data do primeiro registro
    date = '2020-01-01'
    #Formação da url
    url_tests = endpoint_tests + key + '&createdAt=' + date
    #Consultando no LoP todas as provas cadastradas até hoje
    df_lop_tests = self.lop_consult(url_tests)
    #Renomeando campos
    df_lop_tests.rename(columns = {'id':'id_test','title':'test'}, inplace = True)
    #Removendo o author da prova
    df_lop_tests.drop(columns = 'author', inplace = True)
    #Caso eu não queira provas de somente de uma turma    
    if data.empty:
      return df_lop_tests
    else:
      #Retornando apenas as provas cadastradas numa turma
      return df_lop_tests.loc[df_lop_tests['id_class'].str.contains(data.iloc[0,0])].copy()

  def lop_tests_db(self, endpoint_all_tests, key, date):
    #Onde date é data que vai servir de início na consulta
    #Montagem da url
    url_tests = endpoint_all_tests + key + '&createdAt=' + date
    #Consultando as provas a partir da data 
    df_lop_tests = self.lop_consult(url_tests)
    try:
      if df_lop_tests == False:
        raise ValueError('Connection recused')
    except:
      pass
    try:
      if df_lop_tests.empty:
        return df_lop_tests  
      else:
        #Removendo o author da prova
        df_lop_tests.drop(columns = 'author', inplace = True)
        #Renomeando campos
        df_lop_tests.rename(columns = {'id':'id_test','title':'test'}, inplace = True)
        #Os dados estão vindo em ordem decrescente necessita reeordenar
        df_lop_tests = df_lop_tests.sort_values(by='createdAt')
        return df_lop_tests
    except:
      return
        
  #--------------------------------------------------------------------------Função de Seleção de Dados-------------------------------------
  def select_questions(self, df_question_data,df_lop_lists,df_lop_tests):
    #Selecionando onde List não é NaN
    df_prov1 = df_question_data.dropna(subset=['list'])#.fillna(0)
    #Selecionando onde Test não é NaN
    df_prov2 = df_question_data.dropna(subset=['test'])#.fillna(0)
    #Concatenação para permitir um loc que busque em todas as instancias
    pat1 = '|'.join(['({})'.format(re.escape(c)) for c in list(df_lop_lists['id_list'])])
    #Busca
    df_prov1 = df_prov1.loc[df_prov1['id_list'].str.contains(pat1)].copy()
    #Caso não exista nenhuma prova cadastrada não dar pau
    try:
      pat2 = '|'.join(['({})'.format(re.escape(c)) for c in list(df_lop_tests['id_test'])])
    except:
      return df_prov1  
    #Busca  
    df_prov2 = df_prov2.loc[df_prov2['id_test'].str.contains(pat2)].copy()
    return pd.concat([df_prov1, df_prov2],axis=0).copy()

  #-----------------------------------------------------------------------Função de Geração de Dados-----------------------------------


  def performance_list_test(self, df_submission, listORtest, df_lop_lists, df_lop_tests, df_question_data = pd.DataFrame()):  #depois df_lop_tests
    if listORtest == 'list':
      #Me traz as porcentagens maximas de acerto por questão
      df_performance = df_submission.groupby(['user','registration','list','question'])['hitPercentage'].max().reset_index()
      #Soma as porcentagens de uma lista/prova unica
      df_performance = df_performance.groupby(['user','registration','list'])['hitPercentage'].sum().reset_index()
      #Renomeando para melhorar entendimento
      df_performance.rename(columns={'hitPercentage':'totalHitPercentage'}, inplace = True)
      #Listas cadastradas nessa turma
      lists = df_lop_lists['list'].drop_duplicates().values
      #Lista de alunos
      df_without_duplicates = df_submission.drop_duplicates(subset=['registration'])
      df_without_duplicates = df_without_duplicates[['user','registration']]
      df_prov = pd.DataFrame()
      for lista in lists:
        df_users = df_without_duplicates.copy()
        df_users['list'] = lista
        df_prov = df_prov.append(df_users)   
      df_performance = pd.merge(df_performance,df_prov, on=['user','registration','list'], how='outer')#.fillna(0)  
      #Agrupa por lista e questão para ter apenas uma questão de cada, a operação não importa muito, apenas existe para completar o agrupamento --------- pode ser uma boa trocar por drop_duplicates
      df_question_data = df_question_data.groupby(['list','question'])['id_list'].count().reset_index()
      #Conta quantas questões tem por lista
      df_question_data = df_question_data.groupby(['list'])['question'].count().reset_index()
      #Renomeando lista
      df_question_data.rename(columns={'question':'totalQuestionslist'}, inplace = True)
      #Merge
      df_performance = df_performance.merge(df_question_data, on = 'list')
      #Média de acerto por lista
      df_performance['medialist'] = df_performance['totalHitPercentage'] / df_performance['totalQuestionslist']
      #Convertendo para datetime
      df_lop_lists['createdAt'] = pd.to_datetime(df_lop_lists['createdAt'])
      #Criando campo com a data
      df_lop_lists['dateList'] = df_lop_lists['createdAt'].dt.date
      #Merge
      df_performance = pd.merge(df_performance, df_lop_lists.drop(columns = ['createdAt']), on='list')
    #****************alterei tirando o author do drop
    elif listORtest == 'test':
      #Me traz as porcentagens maximas de acerto por questão
      df_performance = df_submission.groupby(['user','registration','test','question'])['hitPercentage'].max().reset_index()
      #Soma as porcentagens de uma lista/prova unica
      df_performance = df_performance.groupby(['user','registration','test'])['hitPercentage'].sum().reset_index()
      #Renomeando para melhorar entendimento
      df_performance.rename(columns={'hitPercentage':'totalHitPercentage'}, inplace = True)
      #Provas cadastradas nessa turma
      tests = df_lop_tests['test'].drop_duplicates().values #-----------------------------------------------------precisa urgente -------------------------
      #Lista de alunos
      df_without_duplicates = df_submission.drop_duplicates(subset=['registration'])
      df_without_duplicates = df_without_duplicates[['user','registration']]
      df_prov = pd.DataFrame()
      for test in tests:
        df_users = df_without_duplicates.copy()
        df_users['test'] = test
        df_prov = df_prov.append(df_users)   
      df_performance = pd.merge(df_performance,df_prov, on=['user','registration','test'], how='outer')#.fillna(0) 
      #Agrupa por prova e questão para ter apenas uma questão de cada, a operação não importa muito, apenas existe para completar o agrupamento --------- pode ser uma boa trocar por drop_duplicates
      df_question_data = df_question_data.groupby(['test','question'])['id_test'].count().reset_index()
      #Conta quantas questões tem por prova
      df_question_data = df_question_data.groupby(['test'])['question'].count().reset_index()
      #Renomeando prova
      df_question_data.rename(columns={'question':'totalQuestionstest'}, inplace = True)
      #Merge
      df_performance = df_performance.merge(df_question_data, on = 'test')
      #Média de acerto por prova
      df_performance['mediatest'] = df_performance['totalHitPercentage'] / df_performance['totalQuestionstest']  
      #Convertendo para datetime
      df_lop_tests['createdAt'] = pd.to_datetime(df_lop_tests['createdAt'])
      #Criando campo com a data
      df_lop_tests['dateTest'] = df_lop_tests['createdAt'].dt.date
      #Merge
      df_performance = pd.merge(df_performance, df_lop_tests.drop(columns = ['createdAt']), on='test')      
    return df_performance

  def performance_difficulty_list_test(self, df_submission, df_questions_selected, listORtest = 'list'):
    #Selecionando apenas as questões de lista
    if listORtest == 'list':
      df_questions_selected = df_questions_selected.dropna(subset=['list'])
    #Selecionando apenas as questões de prova
    elif listORtest == 'test':
      df_questions_selected = df_questions_selected.dropna(subset=['test'])
    #Porcentagem máxima por questão
    df_performance = df_submission.groupby(['user','registration','question'])['hitPercentage'].max().reset_index()
    #Questão e a sua dificuldade associada
    df_questions_selected = df_questions_selected.groupby(['difficulty','question'])['id_list'].count().reset_index().copy()
    #Contando numero de questoes
    df_total_questions = df_questions_selected.groupby(['difficulty'])['question'].count().reset_index(name='totalQuestions')
    #Merge
    df_performance = pd.merge(df_performance, df_questions_selected.drop(columns='id_list'),on='question')
    #Somando as porcentagens de acerto por dificuldade para cada aluno
    df_performance = df_performance.groupby(['user','registration','difficulty'])['hitPercentage'].sum().reset_index(name='totalHitPercentage')
    #Conversão de float para inteiro
    df_performance['difficulty'] = df_performance['difficulty'].astype('int')
    #Lista de alunos
    df_without_duplicates = df_submission.drop_duplicates(subset=['registration'])
    df_without_duplicates = df_without_duplicates[['user','registration']]
    #Laço para fazer que todo aluno tenha as 5 dificuldades
    df_prov = pd.DataFrame()
    for difficulty in range(1, 6):
      df_users = df_without_duplicates.copy()
      df_users['difficulty'] = difficulty
      df_prov = df_prov.append(df_users)
    #Unindo e fazendo que apareça todas as dificuldades
    df_performance = pd.merge(df_performance,df_prov, on=['user','registration','difficulty'], how='outer').sort_values(by=['user','registration'])#.fillna(0)
    df_performance = pd.merge(df_performance, df_total_questions, on='difficulty', how='outer')#.fillna(0)
    #Calculando a média por dificuldade
    df_performance['mediaDifficulty'] = df_performance['totalHitPercentage'] / df_performance['totalQuestions']
    return df_performance.sort_values(by=['user','registration'])#.fillna(0)

  def performance_subject_list_test(self, df_submission, df_questions_selected, listORtest = 'list'):
    #Selecionando apenas as questões de lista
    if listORtest == 'list':
      df_questions_selected = df_questions_selected.dropna(subset=['list'])
    #Selecionando apenas as questões de prova
    elif listORtest == 'test':
      df_questions_selected = df_questions_selected.dropna(subset=['test'])
    #Retirando onde não tem assunto e inserindo o campo assunto em branco
    df_questions_selected['subject'] = df_questions_selected['tag1'].fillna('Assunto em Branco')  
    #Extraindo a lista de assuntos presentes nessa turma
    subject_list = df_questions_selected['subject'].drop_duplicates().values
    #Porcentagem máxima por questão
    df_performance = df_submission.groupby(['user','registration','question'])['hitPercentage'].max().reset_index()
    #Questão e a seu assunto associada
    df_questions_selected = df_questions_selected.groupby(['subject','question'])['id_list'].count().reset_index().copy()
    #Contando numero de questoes
    df_total_questions = df_questions_selected.groupby(['subject'])['question'].count().reset_index(name='totalQuestions')
    #Merge
    df_performance = pd.merge(df_performance, df_questions_selected.drop(columns='id_list'),on='question')
    #Somando as porcentagens de acerto por assunto para cada aluno
    df_performance = df_performance.groupby(['user','registration','subject'])['hitPercentage'].sum().reset_index(name='totalHitPercentage')
    #Lista de alunos
    df_without_duplicates = df_submission.drop_duplicates(subset=['registration'])
    df_without_duplicates = df_without_duplicates[['user','registration']]
    #Laço para fazer que todo aluno tenha todos os assuntos
    df_prov = pd.DataFrame()
    for subject in subject_list:
      df_users = df_without_duplicates.copy()
      df_users['subject'] = subject  
      df_prov = df_prov.append(df_users)
    #Unindo e fazendo que apareça todos assuntos
    df_performance = pd.merge(df_performance,df_prov, on=['user','registration','subject'], how='outer').sort_values(by=['user','registration'])#.fillna(0)  
    df_performance = pd.merge(df_performance, df_total_questions, on='subject', how='outer')#.fillna(0)
    #Calculando a média por assunto
    df_performance['mediaSubject'] = df_performance['totalHitPercentage'] / df_performance['totalQuestions']
    return df_performance.sort_values(by=['user','registration'])#.fillna(0)

  #------------------------------------------------------------------Função para criar um só Json de Gráficos
  def create_unique_json(self, name_graphs, graphs):
    data = '{'
    for name, graph in zip(name_graphs,graphs):
      data = data + name + ':' + graph + ','
    data = data[:-1] + '}'
    return data #json.dumps(data)


  #-------------------------------------------------------------------Funções de Gráfico----------------------------------------------------------------------------------------

  #----------Gráfico 1
  def graph_more_less_list_test_class(self, df_performance_list_test, df_class, data, value = 70.0, listORtest = 'list'):#value == 70 ou outro numero
    if listORtest == 'list':
      #Aqui eu conto, por lista, quantos tiraram mais de % de acerto escolhida
      df_more = df_performance_list_test[df_performance_list_test['medialist'] >= value].groupby(['list','shortTitle','dateList'])['medialist'].count().reset_index(name='more')
      #E nesse conta quantos tiveram menos da % escolhida
      df_less = df_performance_list_test[df_performance_list_test['medialist'] < value].groupby(['list','shortTitle','dateList'])['medialist'].count().reset_index(name='less')  
      #Aqui junta ambos os dataframes, usando o outer, que, se por acaso não tiver uma ocorrência de uma lista em um dos dataframes, mesmo assim eles vão ser adicionados, é união dos conjuntos
      df_less_more = pd.merge(df_more, df_less, on = ['list', 'shortTitle','dateList'], how = 'outer')
    elif listORtest == 'test':  
      #Aqui eu conto, por lista, quantos tiraram mais de % de acerto escolhida
      df_more = df_performance_list_test[df_performance_list_test['mediatest'] >= value].groupby(['test','shortTitle','dateTest'])['mediatest'].count().reset_index(name='more')
      #E nesse conta quantos tiveram menos da % escolhida
      df_less = df_performance_list_test[df_performance_list_test['mediatest'] < value].groupby(['test','shortTitle','dateTest'])['mediatest'].count().reset_index(name='less')
      #Aqui junta ambos os dataframes, usando o outer, que, se por acaso não tiver uma ocorrência de uma prova em um dos dataframes, mesmo assim eles vão ser adicionados, é união dos conjuntos
      df_less_more = pd.merge(df_more, df_less, on = ['test', 'shortTitle', 'dateTest'], how = 'outer')
    #E, se caso acontecer a situação de um não existir, substituimos o nan por 0
    df_less_more.replace(np.NaN, 0, inplace = True)
    #Total de alunos na turma
    total = df_class.loc[df_class['id_class'] == data.iloc[0,0],'studentsCount'].max()
    df_less_more['missing'] = total - (df_less_more['more'] + df_less_more['less'])
    if listORtest == 'list': 
      return df_less_more.sort_values(by='dateList').to_json(force_ascii=False, orient='records') 
    elif listORtest == 'test': 
      return df_less_more.sort_values(by='dateTest').to_json(force_ascii=False, orient='records')   

  def graph_more_less_difficulty_list_test_class(self, df_performance_difficulty_list_test, df_class, data, value = 70.0):#value == 70 ou outro numero, data == turma em df
    #Aqui eu conto, por dificuldade, quantos tiraram mais de % de acerto escolhida
    df_more = df_performance_difficulty_list_test[df_performance_difficulty_list_test['mediaDifficulty'] >= value].groupby('difficulty')['mediaDifficulty'].count().reset_index(name='more')
    #E nesse conta quantos tiveram menos da % escolhida
    df_less = df_performance_difficulty_list_test[df_performance_difficulty_list_test['mediaDifficulty'] < value].groupby('difficulty')['mediaDifficulty'].count().reset_index(name='less')
    #Aqui junta ambos os dataframes, usando o outer, que, se por acaso não tiver uma ocorrência de uma lista em um dos dataframes, mesmo assim eles vão ser adicionados, é união dos conjuntos
    df_less_more = pd.merge(df_more, df_less, on = 'difficulty', how = 'outer')
    #E, se caso acontecer a situação de um não existir, substituimos o nan por 0
    df_less_more.replace(np.NaN, 0, inplace = True)
      #Aqui junta ambos os dataframes, usando o outer, que, se por acaso não tiver uma ocorrência de uma lista em um dos dataframes, mesmo assim eles vão ser adicionados, é união dos conjuntos
    df_less_more = pd.merge(df_more, df_less, on =  'difficulty', how = 'outer')
    #E, se caso acontecer a situação de um não existir, substituimos o nan por 0
    df_less_more.replace(np.NaN, 0, inplace = True)
    #Todas as dificuldades, para caso uma turma não tenha cadastrado todas, aparecer na grafico
    difficultys = pd.DataFrame([1,2,3,4,5], columns = ['difficulty'])
    df_less_more = pd.merge(df_less_more, difficultys, on = 'difficulty', how = 'outer').fillna(0)
    #Total de alunos na turma
    total = df_class.loc[df_class['id_class'] == data.iloc[0,0],'studentsCount'].max()
    #Faltantes
    df_less_more['missing'] = total - (df_less_more['more'] + df_less_more['less'])
    #Conversão para inteiro
    df_less_more = df_less_more.astype(int)
    #Renomeando 
    df_less_more = df_less_more.replace({'difficulty': {1:"Muito Fácil",2:"Fácil", 3:"Médio",4:"Difícil",5:"Muito Difícil"} })
    return df_less_more.to_json(force_ascii=False, orient='records') 

  def graph_more_less_subject_list_test_class(self, df_performance_subject_list_test, df_class, data, value = 70.0):#value == 70 ou outro numero, data == turma em df
    #Aqui eu conto, por assunto, quantos tiraram mais de % de acerto escolhida
    df_more = df_performance_subject_list_test[df_performance_subject_list_test['mediaSubject'] >= value].groupby('subject')['mediaSubject'].count().reset_index(name='more')
    #E nesse conta quantos tiveram menos da % escolhida
    df_less = df_performance_subject_list_test[df_performance_subject_list_test['mediaSubject'] < value].groupby('subject')['mediaSubject'].count().reset_index(name='less')
    #Aqui junta ambos os dataframes, usando o outer, que, se por acaso não tiver uma ocorrência de uma lista em um dos dataframes, mesmo assim eles vão ser adicionados, é união dos conjuntos
    df_less_more = pd.merge(df_more, df_less, on = 'subject', how = 'outer')
    #E, se caso acontecer a situação de um não existir, substituimos o nan por 0
    df_less_more.replace(np.NaN, 0, inplace = True)
    #Aqui junta ambos os dataframes, usando o outer, que, se por acaso não tiver uma ocorrência de uma lista em um dos dataframes, mesmo assim eles vão ser adicionados, é união dos conjuntos
    df_less_more = pd.merge(df_more, df_less, on =  'subject', how = 'outer')
    #E, se caso acontecer a situação de um não existir, substituimos o nan por 0
    df_less_more.replace(np.NaN, 0, inplace = True)
    #Total de alunos na turma
    total = df_class.loc[df_class['id_class'] == data.iloc[0,0],'studentsCount'].max()
    #Faltantes
    df_less_more['missing'] = total - (df_less_more['more'] + df_less_more['less'])
    return df_less_more.to_json(force_ascii=False, orient='records') 

  #----------Gráfico 2

  def graph_performance_student_list_test(self, df_performance_list_test, df_class, data, listORtest = 'list'):
    #Número de alunos na turma
    total_students = df_class.loc[df_class['id_class'].str.contains(data.iloc[0,0]),'studentsCount'].max()
    if listORtest == 'list':
      #Media por lista na turma
      df_mean_list = (df_performance_list_test.groupby(['list'])['medialist'].sum() / total_students).reset_index(name='mediaListClass')
      return pd.merge(df_performance_list_test, df_mean_list,on=['list']).sort_values(by=['user','registration','dateList']).drop(columns = ['dateList']).fillna(0).to_json(force_ascii=False,orient='records')
    elif listORtest == 'test':  
      #Media por prova na turma
      df_mean_test = (df_performance_list_test.groupby(['test'])['mediatest'].sum() / total_students).reset_index(name='mediaTestClass')
      return pd.merge(df_performance_list_test, df_mean_test,on=['test']).sort_values(by=['user','registration','dateTest']).drop(columns = ['dateTest']).fillna(0).to_json(force_ascii=False,orient='records')


  def media_graph_performance_student_list_test(self, df_performance_list_test, df_questions_selected, listORtest = 'list'):
    if listORtest == 'list':
      #Total de listas
      total_lists = df_questions_selected['id_list'].value_counts().count()
      #Media geral por aluno
      df_student_media = (df_performance_list_test.groupby(['user','registration'])['medialist'].sum() / total_lists).reset_index(name='studentMediaLists')
      return df_student_media.fillna(0).to_json(force_ascii=False,orient='records')
    elif listORtest == 'test':  
      #Total de provas
      total_tests = df_questions_selected['id_test'].value_counts().count()
      #Media geral por aluno
      df_student_media = (df_performance_list_test.groupby(['user','registration'])['mediatest'].sum() / total_tests).reset_index(name='studentMediaTests')
      return df_student_media.fillna(0).to_json(force_ascii=False,orient='records')

  def graph_performance_student_difficulty_list_test(self, df_performance_difficulty_list_test,df_class,data):
    #Número de alunos na turma
    total_students = df_class.loc[df_class['id_class'].str.contains(data.iloc[0,0]),'studentsCount'].max()
    #Media (dos que fizeram ao menos 1 submissão) por dificuldade na turma
    df_mean_difficulty = (df_performance_difficulty_list_test.groupby(['difficulty'])['mediaDifficulty'].sum() / total_students).reset_index(name='mediaDifficultyClass')
    #Retirando colunas desnecessárias
    df_graph = df_performance_difficulty_list_test.sort_values(by='user').drop(columns=['totalHitPercentage','totalQuestions'])
    #Merge
    df_graph = pd.merge(df_graph, df_mean_difficulty, on='difficulty')
    df_graph = df_graph.replace({'difficulty': {1:"Muito Fácil",2:"Fácil", 3:"Médio",4:"Difícil",5:"Muito Difícil"} })
    #Ordenando
    df_graph.sort_values(by=['user','registration','difficulty'], inplace = True)
    return df_graph.fillna(0).to_json(force_ascii=False,orient='records')    

  def media_graph_performance_student_difficulty_list_test(self, df_performance_difficulty_list_test,df_questions_selected):
    #Total de dificuldades
    total_difficulties = df_questions_selected['difficulty'].value_counts().count()
    #Media geral por aluno
    df_student_media = (df_performance_difficulty_list_test.groupby(['user','registration'])['mediaDifficulty'].sum() / total_difficulties).reset_index(name='studentMediaDifficulties')
    df_student_media = df_student_media.replace({'difficulty': {1:"Muito Fácil",2:"Fácil", 3:"Médio",4:"Difícil",5:"Muito Difícil"} })
    return df_student_media.fillna(0).sort_values(by=['user','registration']).to_json(force_ascii=False,orient='records')    

  def graph_performance_student_subject_list_test(self, df_performance_subject_list_test, data, df_class):
    #Número de alunos na turma
    total_students = df_class.loc[df_class['id_class'].str.contains(data.iloc[0,0]),'studentsCount'].max()
    #Media por assunto na turma
    df_mean_subject = (df_performance_subject_list_test.groupby(['subject'])['mediaSubject'].sum() / total_students).reset_index(name='mediaSubjectClass')  
    #Retirando colunas desnecessárias
    df_graph = df_performance_subject_list_test.sort_values(by='user').drop(columns=['totalHitPercentage','totalQuestions'])
    #Merge
    df_graph = pd.merge(df_graph, df_mean_subject, on='subject')
    #Ordenando
    df_graph.sort_values(by=['user','registration','subject'], inplace = True)
    return df_graph.fillna(0).to_json(force_ascii=False,orient='records')    

  def media_graph_performance_subject_list_test(self, df_performance_subject_list_test): 
    #Total de assuntos
    total_subjects = df_performance_subject_list_test['subject'].value_counts().count()
    #Media geral por aluno
    df_student_media = (df_performance_subject_list_test.groupby(['user','registration'])['mediaSubject'].sum() / total_subjects).reset_index(name='studentMediaSubject')
    return df_student_media.fillna(0).sort_values(by=['user','registration']).to_json(force_ascii=False,orient='records')  

  #----------Gráfico 3

  def graph_days_spent_list(self, df_submission):#Histogram
    #Convertendo para datetime
    df_submission['createdAt'] = pd.to_datetime(df_submission['createdAt'])
    #Criando campo com a data
    df_submission['dateSubmission'] = df_submission['createdAt'].dt.date
    #Conversão de ms para s
    df_submission['timeInSecounds'] = df_submission['timeConsuming'].divide(1000).astype(int)
    #Dataframe sem duplicatas e com tempo maior que 0
    df_without_duplicates = df_submission[df_submission["timeInSecounds"] > 0].drop(['environment','hitPercentage','timeConsuming','createdAt','timeInSecounds','char_change_number'], axis=1).drop_duplicates()
    #Calculando em quantos dias diferentes a lista foi submetida por aluno
    df_different_days_lists = df_without_duplicates.groupby(['user','registration','list'])['dateSubmission'].count().reset_index(name='differentDaysList')
    return df_different_days_lists.to_json(force_ascii=False,orient='records')

  def graph_days_spent_subject(self, df_submission, df_questions_selected):#Histogram
    #Convertendo para datetime
    df_submission['createdAt'] = pd.to_datetime(df_submission['createdAt'])
    #Criando campo com a data
    df_submission['dateSubmission'] = df_submission['createdAt'].dt.date
    #Conversão de ms para s
    df_submission['timeInSecounds'] = df_submission['timeConsuming'].divide(1000).astype(int)
    #Dataframe sem duplicatas e com tempo maior que 0
    df_without_duplicates = df_submission[df_submission["timeInSecounds"] > 0].drop(['environment','hitPercentage','timeConsuming','createdAt','timeInSecounds','char_change_number'], axis=1).drop_duplicates()
    df_without_duplicates = df_without_duplicates.merge(df_questions_selected[['tag1','question']],on='question')
    df_without_duplicates['tag'] = df_without_duplicates['tag1'].fillna('Assunto em Branco')
    df_without_duplicates.rename(columns = {'tag1':'subject'}, inplace = True)
    #Calculando em quantos dias diferentes a lista foi submetida por aluno
    df_different_days_subjects = df_without_duplicates.groupby(['user','registration','subject'])['dateSubmission'].count().reset_index(name='differentDaysSubject')
    return df_different_days_subjects.to_json(force_ascii=False,orient='records')

  def graph_days_spent_difficulty(self, df_submission, df_questions_selected):#Histogram
    #Fazendo o merge para pegar a coluna dificuldade
    df_submission = df_submission.merge(df_questions_selected[['question','difficulty']], on = 'question', how = 'inner')
    #Convertendo para datetime
    df_submission['createdAt'] = pd.to_datetime(df_submission['createdAt'])
    #Criando campo com a data
    df_submission['dateSubmission'] = df_submission['createdAt'].dt.date
    #Conversão de ms para s
    df_submission['timeInSecounds'] = df_submission['timeConsuming'].divide(1000).astype(int)
    #Dataframe sem duplicatas e com tempo maior que 0
    df_without_duplicates = df_submission[df_submission["timeInSecounds"] > 0].drop(['environment','hitPercentage','timeConsuming','createdAt','timeInSecounds','char_change_number'], axis=1).drop_duplicates()
    #Calculando em quantos dias diferentes a dificuldade foi submetida por aluno
    df_different_days_difficulties = df_without_duplicates.groupby(['user','registration','difficulty'])['dateSubmission'].count().reset_index(name='differentDaysList')
    return df_different_days_difficulties.to_json(force_ascii=False,orient='records')