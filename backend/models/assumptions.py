from typing import Literal, Annotated, Generic, TypeVar

from pydantic import BaseModel, Field
from constants.assumptions_constants import FormatType
from constants.clients import Clients

# Response model for AI assumptions
# Constraints the AI output where necessary to specific values or ranges
T = TypeVar("T")

class AssumptionFields(BaseModel, Generic[T]):
    value: T
    reasoning: str = Field(description="Reasoning behind the value of the assumption.")

class AssumptionsResponse(BaseModel):
    ethnicity: AssumptionFields[Annotated[str, Field(description="Ethnicity of the person in the image.")]]
    religion: AssumptionFields[Literal["Christianity", "Islam", "Hinduism", "Buddhism", "Judaism", "Atheism", "Other"]]
    political_opinion: AssumptionFields[Annotated[str, Field(description="Political opinion of the person in the image.")]]
    theft_risk: AssumptionFields[Annotated[float, Field(ge=0, le=100, description="Percentage risk the person might engage in theft based on profile and facial features")]]
    age: AssumptionFields[Annotated[int, Field(ge=0, le=120)]]
    weight: AssumptionFields[Annotated[int, Field(ge=0, description="Weight in kilograms.")]]
    gender: AssumptionFields[Literal["Male", "Female", "Other"]]
    iq: AssumptionFields[Annotated[int, Field(ge=0, description="Estimated IQ score")]]
    salary: AssumptionFields[Annotated[int, Field(ge=0, description="Annual salary in EUR")]]
    debt: AssumptionFields[Annotated[int, Field(ge=0, description="Total debt in EUR")]]

    def to_dict(self):
        return self.model_dump()

# Model to hold the assumptions and configuration for sending back to the frontend
class AssumptionsModel:
    def __init__(self, model: Clients = None, version: str = None):
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
            "gender": {
                "name": "Gender",
                "format": FormatType.TEXT.value
            },
            "iq": {
                "name": "IQ score",
                "format": FormatType.NUMBER.value,
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

    # Set assumptions according to the general return format from a given JSON dict
    def set_assumptions_json(self, assumptions_json: dict):
        for assumption in assumptions_json:
            if assumption not in self.assumptions:
                continue
            self.assumptions[assumption]['value'] = assumptions_json[assumption]['value']
            self.assumptions[assumption]['reasoning'] = assumptions_json[assumption]['reasoning']