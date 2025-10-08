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