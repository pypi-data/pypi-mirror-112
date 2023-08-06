# Wrapmail

## Installation 

pip install wrapmail

## Google Gmail API Wrapper Setup

This module comes with a wrapper for Google's Gmail api.
Google requires authentication for using the Gmail api. In order to use the wrapper, go to google developers console, create project, register Gmail api.
The only required scope is https://mail.google.com/ Then, you need to download the client_secret json file and include it in your directory.

After you include client_secret.json and instantiated the Gmail class and run the main python file, and automatic authentication window will open and ask you
to sign in. After signing in, if your authentication was successful you will be prompted by message "authentication flow has completed" and a pickle file will be created. As long as pickle file does not expire and is included in your working directory, you won't need to complete these steps. Do not share your client secret file, its contents or your pickle file. The authenticated email address will be used to send mails.

Since OAuth is used, you don't need to allow for less secure apps in your gmail account.

