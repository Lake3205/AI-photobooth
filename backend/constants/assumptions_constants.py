from enum import Enum

# Enumeration for different format types used in assumptions
class FormatType(Enum):
    PERCENTAGE = "percentage"
    CURRENCY = "currency"
    NUMBER = "number"
    WEIGHT = "weight"
    YEARS = "years"
    HOURS_DAY = "hours_per_day"
    TEXT = "text"
    
