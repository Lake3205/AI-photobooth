import random

from constants.assumptions_constants import (
    EDUCATION_LEVELS, GENERATIONS, MARITAL_STATUSES
)


class AssumptionsService:
    def get_assumptions(self):
        return {
            "TheftRate": random.randint(0, 100),
            "School": random.choice(EDUCATION_LEVELS),
            "Salary": random.randint(20000, 200000),
            "Generation": random.choice(GENERATIONS),
            "Weight": random.randint(45, 120),
            "CitizenState": random.choice(MARITAL_STATUSES),
            "Dept": random.randint(0, 100000),
            "FitnessAge": random.randint(18, 70),
            "ScreenTime": random.randint(0, 12),
        }
    
    def get_assumptions_with_defaults(self):
        assumptions = self.get_assumptions()
        
        defaults = {
            "TheftRate": 50,
            "School": "havo",
            "Salary": 50000,
            "Generation": "Millenial",
            "Weight": 70,
            "CitizenState": "Single",
            "Dept": 10000,
            "FitnessAge": 30,
            "ScreenTime": 6
        }
        
        for key, default_value in defaults.items():
            if key not in assumptions or assumptions[key] is None:
                assumptions[key] = default_value
        
        return assumptions