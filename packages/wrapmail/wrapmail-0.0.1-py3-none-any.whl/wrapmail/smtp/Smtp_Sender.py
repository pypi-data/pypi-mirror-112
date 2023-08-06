from wrapmail.abstract_sender import Abstract_Sender
import os
import smtplib
import traceback

class SMTP_Sender(Abstract_Sender):
    def __init__(self):
        super().__init__()

    def start_service(self):
        try:
            self.connection = smtplib.SMTP("smtp.gmail.com", 587)
            self.connection.ehlo()
            self.connection.starttls()
            self.connection.login(os.environ.get("EMAIL"),
                              os.environ.get("PASSWORD"))
            self.available = True
        except Exception as e:
            print("could not start smtp service")
            print(e) 
            self.available = False

    def send(self, mail):
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

            self.connection.quit()

        except Exception:
            print("could not send the mail")
            traceback.print_exc()
            return False