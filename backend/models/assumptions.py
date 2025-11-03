class AssumptionsModel:
    def __init__(self, model: str = None, version: str = None, assumptions: dict = None):
        self.model = model
        self.version = version
        self.assumptions = assumptions
    
    def to_dict(self):
        return {
            "model": self.model,
            "version": self.version,
            "assumptions": self.assumptions
        }
        
    def set_assumption_value(self, key: str, value):
        self.assumptions[key]['value'] = value
        
    