import smtplib
from email.mime.text import MIMEText
import os

class Email:
    def __init__(self, email_adress, password):
        '''
        O iniciador da classe recebe como parâmetros de entrada um email e uma senha, referente ao email.
        Ele também faz a conexão com os servidores da google e seta a porta.
        '''
        self.smtp_ssl_host = 'smtp.gmail.com'
        self.smtp_ssl_port = 465

        self.__email_adress = os.environ['EMAIL_ADRESS']
        self.__password = os.environ['PASSWORD_EMAIL']

    def send_email(self, message, message_subject):
        '''
        O método send_email() recebe como parâmetro uma mensagem e um título, message_subject, ele faz a conexão
        com o servidor e logo após ele loga na sua conta de email. Detalhe que vale ressaltar, as contas do google 
        tem uma proteção de não aceitar acesso de aplicativos menos seguros como por exemplo o google colab, por isso
        é necessário autorizar que o seu email faça login por meio de aplicativos menos seguros a partir deste link:
        https://accounts.google.com/DisplayUnlockCaptcha.
        Após fazer login na conta do email, ele vai mandar um email do próprio email para ele mesmo e depois fecha o 
        servidor.
        '''
        message = MIMEText(message)
        message['subject'] = message_subject

        message['from'] = self.__email_adress
        message['to'] = self.__email_adress

        sever = smtplib.SMTP_SSL(self.smtp_ssl_host, self.smtp_ssl_port)

        server.login(self.__email_adress, self.__password)
        server.sendemail(self.__email_adress, self.__email_adress, message.as_string())
        server.quit()
        return