-- Migration: Add assumption sessions
-- Created: 2026-02-17
-- Description: Adds assumption_sessions table and assumption_session_assumptions relation table
--              to track which assumptions are related to the same selfie request

-- UP

-- Create assumption_sessions table to group related assumptions
CREATE TABLE IF NOT EXISTS assumption_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    image_name VARCHAR(255),
    image_mime_type VARCHAR(100)
);

-- Create relation table to link assumptions to sessions (many-to-many)
CREATE TABLE IF NOT EXISTS assumption_session_assumptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    assumption_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_session
        FOREIGN KEY (session_id)
        REFERENCES assumption_sessions(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_session_assumption
        FOREIGN KEY (assumption_id)
        REFERENCES assumptions(id)
        ON DELETE CASCADE,
    CONSTRAINT ux_session_assumption_unique
        UNIQUE (session_id, assumption_id)
);

-- Add session_id to form_tokens to track which session the form relates to
ALTER TABLE form_tokens
ADD COLUMN session_id INT,
ADD CONSTRAINT fk_form_tokens_session
    FOREIGN KEY (session_id)
    REFERENCES assumption_sessions(id)
    ON DELETE CASCADE;

-- Create indexes for better query performance
CREATE INDEX idx_assumption_session_assumptions_session_id
    ON assumption_session_assumptions(session_id);

CREATE INDEX idx_assumption_session_assumptions_assumption_id
    ON assumption_session_assumptions(assumption_id);

CREATE INDEX idx_form_tokens_session_id
    ON form_tokens(session_id);

-- DOWN

-- Drop indexes
DROP INDEX IF EXISTS idx_form_tokens_session_id ON form_tokens;
DROP INDEX IF EXISTS idx_assumption_session_assumptions_assumption_id ON assumption_session_assumptions;
DROP INDEX IF EXISTS idx_assumption_session_assumptions_session_id ON assumption_session_assumptions;

-- Remove session_id from form_tokens
ALTER TABLE form_tokens
DROP FOREIGN KEY IF EXISTS fk_form_tokens_session,
DROP COLUMN IF EXISTS session_id;

-- Drop tables in reverse order
DROP TABLE IF EXISTS assumption_session_assumptions;
DROP TABLE IF EXISTS assumption_sessions;
