from wrapmail.abstract_sender import Abstract_Sender
from wrapmail.gmail.Google import Create_Service
import base64
import os

class Gmail_Sender(Abstract_Sender):
    def __init__(self):
        super().__init__()

    def start_service(self):
        """
        Initialize the Google service 
        """
        
        if (os.environ.get("CLIENT_SECRET")): 
            #check if CLIENT_SECRET environment variable is present, if so use that directory and name;
            #if not look for the default name and directory
            client_secret = os.environ.get("CLIENT_SECRET")
        else:
            client_secret =  "client_secret.json"

        try:
            self.service = Create_Service(
                client_secret, # client secret file
                "gmail", # which api is being used
                "v1", # version 
                ["https://mail.google.com/"] # scope(s)
            )
            self.available = True # set availability to true (api is ready to send mail)
        except Exception as e:
            print("could not start gmail service")
            print(e)
            self.available = False # set availability to false (api is not ready to send mail)

    def send(self, mail):
        """
        Send mail
        """
        super().send(mail)
        if self.available == False: # check if service is available
            print("service unavailable")
            return False

        raw_string = base64.urlsafe_b64encode(
            mail.as_bytes()).decode() # turn mail into raw_seting
        self.service.users().messages().send(
            userId='me', body={'raw': raw_string}).execute()
        print("email successfully sent")
        return True
