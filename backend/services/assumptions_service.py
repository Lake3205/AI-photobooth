import random

from constants.assumptions_constants import (
    EDUCATION_LEVELS, GENERATIONS, MARITAL_STATUSES, FORMAT_TYPES
)

defaultAssumptions = {
    "TheftRate": {
        "name": "Theft risk",
        "value": 50,
        "format": FORMAT_TYPES["percentage"]    
    },
    "School": {
        "name": "Education level",
        "value": "hbo",
        "format": FORMAT_TYPES["text"]
    },
    "Salary": {
        "name": "Annual salary",
        "value": 50000,
        "format": FORMAT_TYPES["currency"],
        "min": 20000,
        "max": 200000
    },
    "Generation": {
        "name": "Generation",
        "value": "Millenial",
        "format": FORMAT_TYPES["text"]
    },
    "Weight": {
        "name": "Weight",
        "value": 70,
        "format": FORMAT_TYPES["weight"],
        "min": 45,
        "max": 120
    },
    "CitizenState": {
        "name": "Marital status",
        "value": "Single",
        "format": FORMAT_TYPES["text"]
    },
    "Debt": {
        "name": "Debt",
        "value": 10000,
        "format": FORMAT_TYPES["currency"],
        "min": 0,
        "max": 100000,
        "ideal": 0
    },
    "FitnessAge": {
        "name": "Fitness age",
        "value": 30,
        "format": FORMAT_TYPES["years"],
        "min": 18,
        "max": 70
    },
    "ScreenTime": {
        "name": "Screen time",
        "value": 3,
        "format": FORMAT_TYPES["hoursPerDay"],
        "min": 0,
        "max": 12
    }
}


class AssumptionsService:
    def get_assumptions(self):
        defaultAssumptions["TheftRate"]["value"] = random.randint(0, 100)
        defaultAssumptions["School"]["value"] = random.choice(EDUCATION_LEVELS)
        defaultAssumptions["Salary"]["value"] = random.randint(20000, 200000)
        defaultAssumptions["Generation"]["value"] = random.choice(GENERATIONS)
        defaultAssumptions["Weight"]["value"] = random.randint(45, 120)
        defaultAssumptions["CitizenState"]["value"] = random.choice(MARITAL_STATUSES)
        defaultAssumptions["Debt"]["value"] = random.randint(0, 100000)
        defaultAssumptions["FitnessAge"]["value"] = random.randint(18, 70)
        defaultAssumptions["ScreenTime"]["value"] = random.randint(0, 12)
        
        return defaultAssumptions
    