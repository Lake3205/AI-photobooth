from typing import Literal, Annotated, Generic, TypeVar

from config import SHOW_REASONING
from constants.assumptions_constants import FormatType
from constants.clients import Clients
from pydantic import BaseModel, Field

# Response model for AI assumptions
# Constraints the AI output where necessary to specific values or ranges
T = TypeVar("T")

if SHOW_REASONING:
    class AssumptionFields(BaseModel, Generic[T]):
        value: T
        reasoning: str = Field(
            description="Reasoning behind the value of the assumption. Give the explanation in 'you' form. Don't mention the lack of certainty. Be as critical and direct as possible in a slight malevolent tone.")
else:
    class AssumptionFields(BaseModel, Generic[T]):
        value: T


class AssumptionsResponse(BaseModel):
    ethnicity: AssumptionFields[Annotated[str, Field(
        description="Ethnicity of the person in the image, e.g., Caucasian, African, Asian, etc. In case of mixed, use the most dominant.")]]
    religion: AssumptionFields[
        Annotated[str, Field(description="Religion of the person in the image. If uncertain, take a guess.")]]
    political_opinion: AssumptionFields[
        Annotated[str, Field(description="Political opinion of the person in the image. If uncertain, take a guess.")]]
    theft_risk: AssumptionFields[
        Annotated[float, Field(ge=0, le=100, description="Percentage risk the person might engage in theft.")]]
    age: AssumptionFields[Annotated[int, Field(ge=0, le=120)]]
    weight: AssumptionFields[Annotated[int, Field(ge=0, description="Weight in kilograms.")]]
    gender: AssumptionFields[Literal["Male", "Female", "Other"]]
    iq: AssumptionFields[Annotated[int, Field(ge=0, description="Estimated IQ score")]]
    salary: AssumptionFields[
        Annotated[int, Field(ge=0, description="Annual salary in EUR, the modal income is around 30,000 EUR.")]]
    debt: AssumptionFields[Annotated[int, Field(ge=0, description="Total debt in EUR")]]

    def to_dict(self):
        return self.model_dump()


# Model to hold the assumptions and configuration for sending back to the frontend
class AssumptionsModel:
    def __init__(self, model: Clients = None, version: str = None):
        self.model = model
        self.version = version
        self.token = None
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
        result = {
            "model": self.model,
            "version": self.version,
            "assumptions": self.assumptions,
            "token": self.token
        }
        if hasattr(self, 'assumption_id') and self.assumption_id:
            result["id"] = self.assumption_id
        return result

    # Set assumptions according to the general return format from a given JSON dict
    def set_assumptions_json(self, assumptions_json: dict):
        for assumption in assumptions_json:
            if assumption not in self.assumptions:
                continue
            self.assumptions[assumption]['value'] = assumptions_json[assumption]['value']
            if SHOW_REASONING and "reasoning" in assumptions_json[assumption]:
                self.assumptions[assumption]['reasoning'] = assumptions_json[assumption]['reasoning']

    def set_token(self, token: str):
        self.token = token
