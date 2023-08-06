from wrapmail.smtp.Smtp_Sender import SMTP_Sender
from wrapmail.abstract_mail import Mail


class SMTP_mail(Mail):
    def __init__(self, TO, TITLE="", MSG="", html=None):
        sender = SMTP_Sender()
        super().__init__(sender, TO, TITLE, MSG, html)

