# Return format

Though we're using different AI models, we want to maintain a consistent return format for easier processing. Below is the standardized format that all AI responses should adhere to:

```json
{
    "model": "model_name",
    "version": "model_version",
    "assumptions": {
        "Ethnicity": {
            "name": "Ethnicity",
            "value": "ethnicity_value",
            "format": "text"
        },
        "Religion": {
            "name": "Religion",
            "value": "religion_value",
            "format": "text",
        },
        "PoliticalOpinion": {
            "name": "Political opinion",
            "value": "political_opinion_value",
            "format": "text",
        },
        "TheftRisk": {
            "name": "Theft risk",
            "value": 0,
            "format": "percentage",    
        },
        "Age": {
            "name": "Age",
            "value": 0,
            "format": "years",
        },
        "Weight": {
            "name": "Weight",
            "value": 0,
            "format": "weight",
        },
        "School": {
            "name": "Education level",
            "value": "education_level_value",
            "format": "text"
        },
        "Salary": {
            "name": "Annual salary",
            "value": 0,
            "format": "currency",
        },
        "Debt": {
            "name": "Debt",
            "value": 0,
            "format": "currency",
        },
    }
}
```