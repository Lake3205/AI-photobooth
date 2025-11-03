from typing import Literal, Annotated

from pydantic import BaseModel, Field

class AssumptionsResponse(BaseModel):
    ethnicity: str = Field(description="Ethnicity of the person in the image, e.g., Caucasian, African, Asian, etc.")
    religion: Literal["Christianity", "Islam", "Hinduism", "Buddhism", "Judaism", "Atheism", "Other"]
    political_opinion: Literal["Left", "Center", "Right", "Libertarian", "Authoritarian", "Other"]
    theft_risk: Annotated[float, Field(ge=0, le=100)]
    age: Annotated[int, Field(ge=0, le=120)]
    weight: Annotated[int, Field(ge=0)]
    school_level: Literal["Dropout", "Primary", "Secondary", "High School", "Vocational", "Bachelor's", "Master's", "PhD"]
    salary: Annotated[int, Field(ge=0)]
    debt: Annotated[int, Field(ge=0)]

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