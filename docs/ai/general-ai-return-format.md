# Return format

Though we're using different AI models, we want to maintain a consistent return format for easier processing. Below is the standardized format that all AI responses should adhere to:

```json
{
    "model": "model_name",
    "version": "model_version",
    "assumptions": {
        "ethnicity": {
            "name": "Ethnicity",
            "format": "text",
            "value": null
        },
        "religion": {
            "name": "Religion",
            "format": "text",
            "value": null
        },
        "political_opinion": {
            "name": "Political opinion",
            "format": "text",
            "value": null
        },
        "theft_risk": {
            "name": "Theft risk",
            "format": "percentage",    
            "value": null
        },
        "age": {
            "name": "Age",
            "format": "years",
            "value": null
        },
        "weight": {
            "name": "Weight",
            "format": "weight",
            "value": null
        },
        "school": {
            "name": "Education level",
            "format": "text",
            "value": null
        },
        "salary": {
            "name": "Annual salary",
            "format": "currency",
            "value": null
        },
        "debt": {
            "name": "Debt",
            "format": "currency",
            "value": null
        },
    }
}
```