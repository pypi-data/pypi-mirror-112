from abc import ABC, abstractmethod
from wrapmail.abstract_sender import Abstract_Sender
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
from email import encoders
from email.mime.base import MIMEBase
import os


class Mail(ABC):
    def __init__(self, sender, TO, TITLE="", MSG="", html=None):

        self.html = html
        self.TO = TO
        self.MSG = MSG
        self.TITLE = TITLE
        self.mail = MIMEMultipart()
        self.sender = sender

        self.mail["To"] = self.TO
        self.mail["Subject"] = self.TITLE

        if (html is None):
            body = MIMEText(self.MSG, "plain")
            self.mail.attach(body)
        else:
            with open(self.html, "r") as file:
                message = file.read()
                body = MIMEText(message, 'html')
                self.mail.attach(body)


    def send(self) -> bool:
        """
        Send mail
        """
        self.sender.send(self.mail)


    def add_attachment(self, attach) -> bool:
        """
        attach: the filename of the file you are trying to attach
        """

        content_type, encoding = mimetypes.guess_type(attach)
        main_type, sub_type = content_type.split('/',1)
        file_name = os.path.basename(attach)
        with open(attach, 'rb') as f:
            myFile = MIMEBase(main_type, sub_type)
            myFile.set_payload(f.read())
            myFile.add_header('Content-Disposition','attachment',filename=file_name)
            encoders.encode_base64(myFile)
        self.mail.attach(myFile)
        return True
