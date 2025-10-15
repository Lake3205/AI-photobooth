import random
import copy

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
        "value": 20000,
        "format": FORMAT_TYPES["currency"],
        "min": 0,
        "max": 100000
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
    },
    "FitnessAge": {
        "name": "Fitness age",
        "value": 30,
        "format": FORMAT_TYPES["years"],
        "min": 18,
        "max": 70,
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
    def __init__(self):
        pass
    
    def safe_randint(self, min_val, max_val):
        if min_val >= max_val:
            return min_val
        return random.randint(min_val, max_val)
    
    def get_assumptions(self):
        assumptions = copy.deepcopy(defaultAssumptions)
        
        minTheftRisk = 0
        maxTheftRisk = 100
        
        minDebt = assumptions["Debt"]["min"] if "min" in assumptions["Debt"] else 0
        maxDebt = assumptions["Debt"]["max"] if "max" in assumptions["Debt"] else 100000
        
        minSalary = assumptions["Salary"]["min"] if "min" in assumptions["Salary"] else 0
        maxSalary = assumptions["Salary"]["max"] if "max" in assumptions["Salary"] else 100000
        
        maxSalary -= 30000 # general deduction for graph scaling
        
        minFitnessAge = assumptions["FitnessAge"]["min"] if "min" in assumptions["FitnessAge"] else 18
        maxFitnessAge = assumptions["FitnessAge"]["max"] if "max" in assumptions["FitnessAge"] else 70
        
        generations = copy.deepcopy(GENERATIONS)
        
        assumptions["School"]["value"] = random.choice(EDUCATION_LEVELS)
        assumptions["Weight"]["value"] = random.randint(45, 120)
        assumptions["CitizenState"]["value"] = random.choice(MARITAL_STATUSES)
        assumptions["ScreenTime"]["value"] = random.randint(0, 12)
         
        if (assumptions["School"]["value"] == "Bachelor's degree"):
            maxTheftRisk -= 10
            minDebt += 10000
            minSalary += 10000
            generations.remove("Gen Z")
            generations.remove("Gen alpha")
        elif (assumptions["School"]["value"] == "Master's degree" or
            assumptions["School"]["value"] == "PhD"):
            maxTheftRisk -= 20
            minDebt += 20000
            minSalary += 30000
            generations.remove("Gen Z")
            generations.remove("Gen alpha")
        else:
            minTheftRisk += 30
            maxDebt -= 10000
            maxSalary -= 30000
        
        assumptions["Generation"]["value"] = random.choice(generations)
            
        if (assumptions["Generation"]["value"] == "Gen Z" or
            assumptions["Generation"]["value"] == "Gen alpha"
        ):
            maxTheftRisk += 5
            maxDebt -= 20000
            maxSalary -= 30000
            assumptions["ScreenTime"]["value"] += 2 if assumptions["ScreenTime"]["value"] <= 10 else 12
            maxFitnessAge -= 40
            assumptions["CitizenState"]["value"] = "Single"
        elif (assumptions["Generation"]["value"] == "Millenial"):
            maxDebt -= 10000
            maxSalary -= 20000
            maxFitnessAge -= 20
        elif (assumptions["Generation"]["value"] == "Gen X"):
            maxFitnessAge -= 10
        elif (assumptions["Generation"]["value"] == "Boomer" or
              assumptions["Generation"]["value"] == "Stille generatie"):
            minFitnessAge += 30
        
        assumptions["Salary"]["value"] = self.safe_randint(minSalary, maxSalary)
        assumptions["FitnessAge"]["value"] = self.safe_randint(minFitnessAge, maxFitnessAge)
        assumptions["Debt"]["value"] = self.safe_randint(minDebt, maxDebt)
        assumptions["TheftRate"]["value"] = self.safe_randint(minTheftRisk, maxTheftRisk)
        
        return assumptions
    