from wrapmail.abstract_sender import Abstract_Sender
from wrapmail.gmail.Google import Create_Service
import base64

class Gmail_Sender(Abstract_Sender):
    def __init__(self):
        super().__init__()

    def start_service(self):
        try:
            self.service = Create_Service(
                "client_secret.json",
                "gmail",
                "v1",
                ["https://mail.google.com/"]
            )
            self.available = True
        except Exception as e:
            print("could not start gmail service")
            print(e)
            self.available = False

    def send(self, mail):
        super().send(mail)
        if self.available == False:
            print("service unavailable")
            return False

        raw_string = base64.urlsafe_b64encode(
            mail.as_bytes()).decode()
        self.service.users().messages().send(
            userId='me', body={'raw': raw_string}).execute()
        print("email successfully sent")
        return True
