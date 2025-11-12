# Database ERD

```mermaid
erDiagram
    users {
        INT id PK
        VARCHAR username 
        VARCHAR hashed_password
        VARCHAR role
        DATETIME created_at
    }

    assumptions {
        INT id PK
        DATETIME created_at
        VARCHAR ai_model
    }

    assumption_constants {
        INT id PK
        VARCHAR value
    }

    assumption_values {
        INT id PK
        INT assumption_id FK
        INT assumption_constant_id FK
        VARCHAR value
    }

    forms {
        INT id PK
        INT assumption_id FK
    }

    form_questions {
        INT id PK
        INT assumption_constant_id FK
        VARCHAR question
    }

    form_results {
        INT id PK
        INT form_id FK
        INT form_question_id FK
        VARCHAR value
    }

    
    %% Relationships
    %% assumption_values links assumption <-> constants
    assumptions ||--o{ assumption_values : "has values"
    assumption_constants ||--o{ assumption_values : "defines"

    %% forms and their questions/results
    assumptions ||--o{ forms : "has forms"
    assumption_constants ||--o{ form_questions : "used in questions"
    form_questions ||--o{ form_results : "receives answers"
    forms ||--o{ form_results : "contains results"
```
