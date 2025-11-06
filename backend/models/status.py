from constants.clients import Clients
from constants.status import Status

class AIStatusModel:
    def __init__(self):
        self.clients_status = {}
        for client in Clients:
            self.clients_status[client] = {
                "status": Status.UNKNOWN,
                "details": ""
            }
    
    def set_status(self, client: Clients, status: Status, details: str = ""):
        self.clients_status[client]["status"] = status
        self.clients_status[client]["details"] = details
            