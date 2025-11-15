# Form

This section documents the API endpoints related to form handling in the backend. The form controller provides functionality to retrieve and manage assumptions associated with forms.

## Table of Contents

- [Form](#form)
  - [Table of Contents](#table-of-contents)
  - [Security](#security)
  - [Goals](#goals)
    - [Questions](#questions)

## Security

The data from the database is accessed using the id of the assumption. Only sending the id would make it easy to scrape data from the database and fill in forms for other users. To combat this, we use a jwt token that is generated with the generation of the assumptions and stored in our database. This token is then required to access the form and the generated assumptions.

## Goals

We want to collect data from users through the form. 

- How shocked are they by the results?
- How happy are they with the results?
- Do they feel like it's accurate?
- Have they changed their viewpoint on AI?
- Do they feel like there should be more regulation on AI?

### Questions

- On a scale from 1 to 10, how shocked are you by the results?
- On a scale from 1 to 10, how happy are you with the results?
- On a scale from 1 to 10, how accurate do you feel the results are?
- Have you changed your viewpoint on AI after seeing the results? (Yes/No, and optionally explain)
- Do you feel there should be more regulation on AI? (Yes/No, and optionally explain)