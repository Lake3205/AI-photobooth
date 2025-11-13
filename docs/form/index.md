# Form

This section documents the API endpoints related to form handling in the backend. The form controller provides functionality to retrieve and manage assumptions associated with forms.

## Table of Contents

- [Form](#form)
  - [Table of Contents](#table-of-contents)
  - [Security](#security)

## Security

The data from the database is accessed using the id of the assumption. Only sending the id would make it easy to scrape data from the database and fill in forms for other users.

