from typing import Literal, Annotated

from pydantic import BaseModel, Field
from constants.assumptions_constants import FormatType

class AssumptionsResponse(BaseModel):
    ethnicity: str = Field(description="Ethnicity of the person in the image, e.g., Caucasian, African, Asian, etc. In case of mixed, use the most dominant")
    religion: Literal["Christianity", "Islam", "Hinduism", "Buddhism", "Judaism", "Atheism", "Other"]
    political_opinion: Literal["Left", "Center", "Right", "Libertarian", "Authoritarian", "Other"]
    theft_risk: Annotated[float, Field(ge=0, le=100, description="Percentage risk the person might engage in theft based on profile and facial features")]
    age: Annotated[int, Field(ge=0, le=120)]
    weight: Annotated[int, Field(ge=0, description="Weight in kilograms")]
    school_level: Literal["Dropout", "Primary", "Secondary", "High School", "Vocational", "Bachelor's", "Master's", "PhD"]
    salary: Annotated[int, Field(ge=0, description="Annual salary in EUR")]
    debt: Annotated[int, Field(ge=0, description="Total debt in EUR")]

class AssumptionsModel:
    def __init__(self, model: str = None, version: str = None):
        self.model = model
        self.version = version
        self.assumptions = {
            "ethnicity": {
                "name": "Ethnicity",
                "format": FormatType.TEXT.value
            },
            "religion": {
                "name": "Religion",
                "format": FormatType.TEXT.value,
            },
            "political_opinion": {
                "name": "Political opinion",
                "format": FormatType.TEXT.value,
            },
            "theft_risk": {
                "name": "Theft risk",
                "format": FormatType.PERCENTAGE.value,    
            },
            "age": {
                "name": "Age",
                "format": FormatType.YEARS.value,
            },
            "weight": {
                "name": "Weight",
                "format": FormatType.WEIGHT.value,
            },
            "school_level": {
                "name": "Education level",
                "format": FormatType.TEXT.value
            },
            "salary": {
                "name": "Annual salary",
                "format": FormatType.CURRENCY.value,
            },
            "debt": {
                "name": "Debt",
                "format": FormatType.CURRENCY.value,
            },
        }

    def to_dict(self):
        return {
            "model": self.model,
            "version": self.version,
            "assumptions": self.assumptions
        }
    
    def set_assumptions_json(self, assumptions_json: dict):
        for assumption in assumptions_json:
            if assumption not in self.assumptions:
                continue
            self.assumptions[assumption]['value'] = assumptions_json[assumption]
        print(self.to_dict())
        
    def set_assumption_value(self, key: str, value):
        self.assumptions[key]['value'] = value