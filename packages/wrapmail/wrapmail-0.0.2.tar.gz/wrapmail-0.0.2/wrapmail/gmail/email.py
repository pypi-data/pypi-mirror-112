from wrapmail.gmail.Gmail_Sender import Gmail_Sender
from wrapmail.abstract_mail import Mail


class Gmail(Mail):
    def __init__(self, TO, TITLE="", MSG="", html=None):
        """
        TO: mail address of the person who will receive the mail
        TITLE: the title of the mail
        MSG: text message for the mail (optional)
        html: directory of the html file (optional)

        These parameters can be accessed and modified using the same variable names

        Make sure you have included client_secret.json in your working directory,
        if the client secret file is named differently or is located in another directory
        specify that using CLIENT_SECRET environment variable
        """
        sender = Gmail_Sender()
        super().__init__(sender, TO, TITLE, MSG, html)


