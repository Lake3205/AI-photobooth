from constants.clients import Clients
from constants.status import Status
from models.status import AIStatusModel
from requests import get as request_get

class StatusService: 
    def __init__(self):
        self.model_status = AIStatusModel()
        
    def check_status(self, ai_model: Clients):
        match ai_model:
            case Clients.CLAUDE:
                self.check_claude_status()
            case Clients.OPENAI:
                return "OpenAI client is operational."
            case Clients.GEMINI:
                return "Gemini client is operational."
            case _:
                return "Unknown AI model."
            
        return self.model_status.clients_status[ai_model]
            
    def check_claude_status(self):
        try:
            request = request_get("https://status.anthropic.com/api/v2/status.json", timeout=5)
            data = request.json()
            
            if data["status"]["indicator"] == "none":
                self.model_status.set_status(Clients.CLAUDE, Status.OPERATIONAL, str(data["status"]["description"]))
            else:
                self.model_status.set_status(Clients.CLAUDE, Status.OFFLINE, str(data["status"]["description"]))
        except Exception as e:
            self.model_status.set_status(Clients.CLAUDE, Status.OFFLINE, str(e))
            return
        return