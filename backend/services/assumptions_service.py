import random

from constants.assumptions_constants import (
    EDUCATION_LEVELS, GENERATIONS, MARITAL_STATUSES
)


class AssumptionsService:
    def get_assumptions(self):
        return {
            "Diefstalgevaar": f"{random.randint(0, 100)}%",
            "Opleidingsniveau": random.choice(EDUCATION_LEVELS),
            "Jaarsalaris": f"€{random.randint(20000, 200000)}",
            "Generatie": random.choice(GENERATIONS),
            "Gewicht": f"{random.randint(45, 120)}kg",
            "Burgerlijke staat": random.choice(MARITAL_STATUSES),
            "Schulden": f"€{random.randint(0, 100000)}",
            "Fitnessleeftijd": f"{random.randint(18, 70)} jaar",
            "Schermtijd": f"{random.randint(0, 12)} uur per dag",
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