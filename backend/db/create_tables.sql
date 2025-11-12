CREATE TABLE assumptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ai_model VARCHAR(255) NOT NULL
);

CREATE TABLE formats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    value VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE assumption_constants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    format_id INT NOT NULL,
    value VARCHAR(255) NOT NULL,
    CONSTRAINT fk_format
        FOREIGN KEY (format_id)
        REFERENCES formats(id)
        ON DELETE RESTRICT
);

CREATE TABLE assumption_values (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assumption_id INT NOT NULL,
    assumption_constant_id INT NOT NULL,
    value TEXT,
    CONSTRAINT fk_assumption
        FOREIGN KEY (assumption_id)
        REFERENCES assumptions(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_assumption_constant
        FOREIGN KEY (assumption_constant_id)
        REFERENCES assumption_constants(id)
        ON DELETE RESTRICT,
    CONSTRAINT ux_assumption_constant_unique
        UNIQUE (assumption_id, assumption_constant_id)
);

CREATE TABLE forms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assumption_id INT NOT NULL,
    CONSTRAINT fk_forms_assumption
        FOREIGN KEY (assumption_id)
        REFERENCES assumptions(id)
        ON DELETE CASCADE
);

CREATE TABLE form_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assumption_constant_id INT NOT NULL,
    question TEXT NOT NULL,
    CONSTRAINT fk_form_question_constant
        FOREIGN KEY (assumption_constant_id)
        REFERENCES assumption_constants(id)
        ON DELETE RESTRICT
);

CREATE TABLE form_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    form_id INT NOT NULL,
    form_question_id INT NOT NULL,
    value TEXT,
    CONSTRAINT fk_form_result_form
        FOREIGN KEY (form_id)
        REFERENCES forms(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_form_result_question
        FOREIGN KEY (form_question_id)
        REFERENCES form_questions(id)
        ON DELETE CASCADE,
    CONSTRAINT ux_form_result_unique
        UNIQUE (form_id, form_question_id)
);

CREATE INDEX idx_assumption_constants_format_id
    ON assumption_constants(format_id);

CREATE INDEX idx_assumption_values_assumption_id
    ON assumption_values(assumption_id);

CREATE INDEX idx_assumption_values_constant_id
    ON assumption_values(assumption_constant_id);

CREATE INDEX idx_forms_assumption_id
    ON forms(assumption_id);

CREATE INDEX idx_form_questions_constant_id
    ON form_questions(assumption_constant_id);

CREATE INDEX idx_form_results_form_id
    ON form_results(form_id);

CREATE INDEX idx_form_results_question_id
    ON form_results(form_question_id);
