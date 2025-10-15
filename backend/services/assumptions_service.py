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
        "value": 20000,
        "format": FORMAT_TYPES["currency"],
        "min": 0,
        "max": 70000
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
    def get_assumptions(self):
        minTheftRisk = 0
        maxTheftRisk = 100
        
        minDebt = defaultAssumptions["Debt"]["min"] if "min" in defaultAssumptions["Debt"] else 0
        maxDebt = defaultAssumptions["Debt"]["max"] if "max" in defaultAssumptions["Debt"] else 100000
        
        minSalary = defaultAssumptions["Salary"]["min"] if "min" in defaultAssumptions["Salary"] else 0
        maxSalary = defaultAssumptions["Salary"]["max"] if "max" in defaultAssumptions["Salary"] else 100000
        
        minFitnessAge = defaultAssumptions["FitnessAge"]["min"] if "min" in defaultAssumptions["FitnessAge"] else 18
        maxFitnessAge = defaultAssumptions["FitnessAge"]["max"] if "max" in defaultAssumptions["FitnessAge"] else 70
        
        defaultAssumptions["School"]["value"] = random.choice(EDUCATION_LEVELS)
        defaultAssumptions["Generation"]["value"] = random.choice(GENERATIONS)
        defaultAssumptions["Weight"]["value"] = random.randint(45, 120)
        defaultAssumptions["CitizenState"]["value"] = random.choice(MARITAL_STATUSES)
        defaultAssumptions["ScreenTime"]["value"] = random.randint(0, 12)
         
        if (defaultAssumptions["School"]["value"] == "Bachelor's degree"):
            maxTheftRisk -= 10
            minDebt += 10000
            minSalary += 5000
            
        elif (defaultAssumptions["School"]["value"] == "Master's degree" or
            defaultAssumptions["School"]["value"] == "PhD"):
            maxTheftRisk -= 20
            minDebt += 20000
            minSalary += 20000
        else:
            minTheftRisk += 30
            maxDebt -= 10000
            maxSalary -= 45000
            
        if (defaultAssumptions["Generation"]["value"] == "Gen Z" or
            defaultAssumptions["Generation"]["value"] == "Gen alpha"
        ):
            maxTheftRisk += 5
            maxDebt -= 20000
            maxSalary -= 50000
            defaultAssumptions["ScreenTime"]["value"] += 2 if defaultAssumptions["ScreenTime"]["value"] <= 10 else 12
            maxFitnessAge -= 40
            defaultAssumptions["CitizenState"]["value"] = "Single"
        elif (defaultAssumptions["Generation"]["value"] == "Millenial"):
            maxDebt -= 10000
            maxSalary -= 20000
            maxFitnessAge -= 20
        elif (defaultAssumptions["Generation"]["value"] == "Gen X"):
            maxFitnessAge -= 10
        elif (defaultAssumptions["Generation"]["value"] == "Boomer" or
              defaultAssumptions["Generation"]["value"] == "Stille generatie"):
            minFitnessAge += 30
        
        defaultAssumptions["Salary"]["value"] = random.randint(minSalary, maxSalary)
        defaultAssumptions["FitnessAge"]["value"] = random.randint(minFitnessAge, maxFitnessAge)
        defaultAssumptions["Debt"]["value"] = random.randint(minDebt, maxDebt)
        defaultAssumptions["TheftRate"]["value"] = random.randint(minTheftRisk, maxTheftRisk)
        
        return defaultAssumptions
    