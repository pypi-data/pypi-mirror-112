from wrapmail.smtp.Smtp_Sender import SMTP_Sender
from wrapmail.abstract_mail import Mail


class SMTP_mail(Mail):
    def __init__(self, TO, TITLE="", MSG="", html=None):
        """
        TO: mail address of the person who will receive the mail
        TITLE: the title of the mail
        MSG: text message for the mail (optional)
        html: directory of the html file (optional)

        These parameters can be accessed and modified using the same variable names

        EMAIL and PASSWORD environment variables are also necessary
        """
        sender = SMTP_Sender()
        super().__init__(sender, TO, TITLE, MSG, html)

