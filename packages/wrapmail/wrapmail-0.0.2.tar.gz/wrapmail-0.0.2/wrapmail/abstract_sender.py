from abc import ABC, abstractmethod

class Abstract_Sender(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def start_service(self):
        pass
    
    @abstractmethod
    def send(self, mail):
        self.start_service()