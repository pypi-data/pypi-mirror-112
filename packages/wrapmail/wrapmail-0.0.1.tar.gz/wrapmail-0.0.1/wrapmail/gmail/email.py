from wrapmail.gmail.Gmail_Sender import Gmail_Sender
from wrapmail.abstract_mail import Mail


class Gmail(Mail):
    def __init__(self, TO, TITLE="", MSG="", html=None):
        sender = Gmail_Sender()
        super().__init__(sender, TO, TITLE, MSG, html)


