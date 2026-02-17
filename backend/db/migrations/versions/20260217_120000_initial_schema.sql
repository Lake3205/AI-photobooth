-- Migration: Initial database schema
-- Created: 2026-02-17
-- Description: Creates all base tables for the AI-photobooth application

-- UP

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Assumptions table
CREATE TABLE IF NOT EXISTS assumptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ai_model VARCHAR(255) NOT NULL,
    reasoning_enabled TINYINT DEFAULT 1,
    thought TEXT
);

-- Formats table
CREATE TABLE IF NOT EXISTS formats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    value VARCHAR(255) NOT NULL UNIQUE
);

-- Assumption constants table
CREATE TABLE IF NOT EXISTS assumption_constants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    format_id INT NOT NULL,
    value VARCHAR(255) NOT NULL,
    CONSTRAINT fk_format
        FOREIGN KEY (format_id)
        REFERENCES formats(id)
        ON DELETE RESTRICT
);

-- Assumption values table
CREATE TABLE IF NOT EXISTS assumption_values (
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

-- Forms table
CREATE TABLE IF NOT EXISTS forms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assumption_id INT NOT NULL,
    CONSTRAINT fk_forms_assumption
        FOREIGN KEY (assumption_id)
        REFERENCES assumptions(id)
        ON DELETE CASCADE
);

-- Form question types table
CREATE TABLE IF NOT EXISTS form_question_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    value VARCHAR(255) NOT NULL UNIQUE,
    min INT,
    max INT
);

-- Form questions table
CREATE TABLE IF NOT EXISTS form_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_type_id INT NOT NULL,
    question TEXT NOT NULL,
    CONSTRAINT fk_form_question_type
        FOREIGN KEY (question_type_id)
        REFERENCES form_question_types(id)
        ON DELETE RESTRICT
);

-- Form results table
CREATE TABLE IF NOT EXISTS form_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    form_id INT NOT NULL,
    form_question_id INT NOT NULL,
    value TEXT,
    explanation TEXT,
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

-- Form tokens table
CREATE TABLE IF NOT EXISTS form_tokens (
    token VARCHAR(512) PRIMARY KEY,
    assumption_id INT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used TINYINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_form_tokens_assumption
        FOREIGN KEY (assumption_id)
        REFERENCES assumptions(id)
        ON DELETE CASCADE
);

-- Create indexes for better query performance (skip if they exist)
CREATE INDEX IF NOT EXISTS idx_assumption_constants_format_id
    ON assumption_constants(format_id);

CREATE INDEX IF NOT EXISTS idx_assumption_values_assumption_id
    ON assumption_values(assumption_id);

CREATE INDEX IF NOT EXISTS idx_assumption_values_constant_id
    ON assumption_values(assumption_constant_id);

CREATE INDEX IF NOT EXISTS idx_forms_assumption_id
    ON forms(assumption_id);

CREATE INDEX IF NOT EXISTS idx_form_questions_type_id
    ON form_questions(question_type_id);

CREATE INDEX IF NOT EXISTS idx_form_results_form_id
    ON form_results(form_id);

CREATE INDEX IF NOT EXISTS idx_form_results_question_id
    ON form_results(form_question_id);

CREATE INDEX IF NOT EXISTS idx_form_tokens_assumption_id
    ON form_tokens(assumption_id);

-- DOWN

-- Drop tables in reverse order (respecting foreign key constraints)
DROP TABLE IF EXISTS form_tokens;
DROP TABLE IF EXISTS form_results;
DROP TABLE IF EXISTS form_questions;
DROP TABLE IF EXISTS form_question_types;
DROP TABLE IF EXISTS forms;
DROP TABLE IF EXISTS assumption_values;
DROP TABLE IF EXISTS assumption_constants;
DROP TABLE IF EXISTS formats;
DROP TABLE IF EXISTS assumptions;
DROP TABLE IF EXISTS users;