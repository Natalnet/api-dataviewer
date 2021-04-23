import smtplib
from email.mime.text import MIMEText
import os

os.environ['EMAIL_PROJECT'] = 'erros.dataviewer@gmail.com'
os.environ['PASSWORD_EMAIL'] = 'd@t@v13w3r'

class Email:
    def __init__(self):
        '''
        O iniciador da classe recebe como parâmetros de entrada um email e uma senha, referente ao email.
        Ele também faz a conexão com os servidores da google e seta a porta.
        '''
        self.smtp_ssl_host = 'smtp.gmail.com'
        self.smtp_ssl_port = 465

        self.__email_project = os.getenv('EMAIL_PROJECT')
        self.__password = os.getenv('PASSWORD_EMAIL')

    def send_email(self, type_message, subject, name_addressee = None, token = None, error_message = None, email_address = None):
        '''
        O método send_email() recebe como parâmetro uma mensagem e um título, subject, ele faz a conexão
        com o servidor e logo após ele loga na sua conta de email. Detalhe que vale ressaltar, as contas do google 
        tem uma proteção de não aceitar acesso de aplicativos menos seguros como por exemplo o google colab, por isso
        é necessário autorizar que o seu email faça login por meio de aplicativos menos seguros a partir deste link:
        https://accounts.google.com/DisplayUnlockCaptcha.
        Após fazer login na conta do email, ele vai mandar um email do próprio email para ele mesmo e depois fecha o 
        servidor.
        '''
        #Verificando qual tipo de mensagem
        if type_message == 'forgot_password':
            message = 'Olá ' + str(name_addressee) + ', seu token para realizar a autenticação é: ' + str(token) + '. Ele tem validade de 5 minutos.'
        elif type_message == 'errors':
            message = str(error_message)
            email_address = self.__email_project
        else:
            return

        message = MIMEText(message)
        message['subject'] = subject

        message['from'] = self.__email_project
        message['to'] = email_address

        server = smtplib.SMTP_SSL(self.smtp_ssl_host, self.smtp_ssl_port)

        server.login(self.__email_project, self.__password)
        server.sendemail(self.__email_project, self.__email_project, message.as_string())
        server.quit()
        return
