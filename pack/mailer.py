import smtplib
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

FROM = os.environ['FROM']
TO = os.environ['TO']
PASSWORD = os.environ['PASSWORD']


class Mail:
    def __init__(self):
        self.smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        self.smtp_server.starttls()
        self.smtp_server.login(FROM, PASSWORD)

    @staticmethod
    def create_message(subject, text):
        msg = MIMEMultipart()
        msg['From'] = FROM
        msg['To'] = TO
        msg['Subject'] = subject
        msg.attach(MIMEText(text, 'plain'))
        return msg

    def send_message(self, subject, text):
        msg = self.create_message(subject, text)

        try:
            response = self.smtp_server.sendmail(from_addr=FROM, to_addrs=TO, msg=msg.as_string())
            return bool(response)
        except smtplib.SMTPResponseException as e:
            return True

    def quit_server(self):
        self.smtp_server.quit()


def one_send_mail(subject, text):
    mail = Mail()
    mail.send_message(subject, text)
    mail.quit_server()
