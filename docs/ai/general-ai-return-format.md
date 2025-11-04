# Return format

Though we're using different AI models, we want to maintain a consistent return format for easier processing. Below is the standardized format that all AI responses should adhere to:

```json
{
    "model": "model_name",
    "version": "model_version",
    "assumptions": {
        "ethnicity": {
            "name": "Ethnicity",
            "value": "ethnicity_value",
            "format": "text"
        },
        "religion": {
            "name": "Religion",
            "value": "religion_value",
            "format": "text",
        },
        "political_opinion": {
            "name": "Political opinion",
            "value": "political_opinion_value",
            "format": "text",
        },
        "theft_risk": {
            "name": "Theft risk",
            "value": 0,
            "format": "percentage",    
        },
        "age": {
            "name": "Age",
            "value": 0,
            "format": "years",
        },
        "weight": {
            "name": "Weight",
            "value": 0,
            "format": "weight",
        },
        "school": {
            "name": "Education level",
            "value": "education_level_value",
            "format": "text"
        },
        "salary": {
            "name": "Annual salary",
            "value": 0,
            "format": "currency",
        },
        "debt": {
            "name": "Debt",
            "value": 0,
            "format": "currency",
        },
    }
}
```