from wrapmail.abstract_sender import Abstract_Sender
import os
import smtplib
import traceback

class SMTP_Sender(Abstract_Sender):
    def __init__(self):
        super().__init__()

    def start_service(self):
        """
        Start service (connect to the SMTP server and login)
        """
        try:
            
            smtp_server = "smtp.gmail.com" 
            if os.environ.get("SMTP_SERVER"): # check if SMTP_SERVER environment variable is present, if not use smtp.gmail.com
                smtp_server = os.environ.get("SMTP_SERVER")
            
            smtp_port = 587
            if os.environ.get("SMTP_PORT"): # check if SMTP_PORT environment variable is present, if not use 587
                smtp_server = int(os.environ.get("SMTP_PORT"))

            self.connection = smtplib.SMTP(smtp_server, smtp_port) #initialize connection
            self.connection.ehlo() #https://docs.python.org/3/library/smtplib.html
            self.connection.starttls() #starts transport layer security
            self.connection.login(os.environ.get("EMAIL"),
                              os.environ.get("PASSWORD")) #logins with environment variables EMAIL and PASSWORD
            self.available = True # set availability to true (api is ready to send mail)
        except Exception as e:
            print("could not start smtp service")
            print(e) 
            self.available = False # set availability to false (api is not ready to send mail)

    def send(self, mail):
        """
        Send mail
        """
        super().send(mail)
        if self.available == False:
            print("service unavailable")
            return False

        try:
            self.start_service()
            self.connection.sendmail(
                os.environ.get("EMAIL"),
                mail["To"],
                mail.as_string()
            )

            self.connection.quit() #quit connection

        except Exception:
            print("could not send the mail")
            traceback.print_exc()
            return False