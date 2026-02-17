-- Migration: Add AI settings table
-- Created: 2026-02-17 16:00:00
-- Description: Add table to store AI provider configurations (enabled status and model versions)

-- UP

CREATE TABLE ai_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    provider VARCHAR(50) NOT NULL UNIQUE,
    enabled TINYINT DEFAULT 1,
    model_version VARCHAR(255) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default settings for each AI provider
INSERT INTO ai_settings (provider, enabled, model_version) VALUES
    ('openai', 1, 'gpt-4o'),
    ('claude', 1, 'claude-sonnet-4-5'),
    ('gemini', 1, 'gemini-2.5-flash');

-- DOWN

DROP TABLE IF EXISTS ai_settings;

