from enum import Enum

EDUCATION_LEVELS = [
    "Dropout", "Middle school", "High school", "Bachelor's degree", "Master's degree", "PhD"
]
GENERATIONS = [
    "Stille generatie", "Boomer", "Gen X", "Millenial", "Gen Z", "Gen alpha"
]
MARITAL_STATUSES = [
    "Married", "Living together / Cohabiting", "Single"
]

# Enumeration for different format types used in assumptions
class FormatType(Enum):
    PERCENTAGE = "percentage"
    CURRENCY = "currency"
    NUMBER = "number"
    WEIGHT = "weight"
    YEARS = "years"
    HOURS_DAY = "hours_per_day"
    TEXT = "text"
    
