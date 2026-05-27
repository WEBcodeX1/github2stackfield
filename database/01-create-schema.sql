-- ]*[ ------------------------------------------------------------------ ]*[
-- .   github2stackfield - Database Schema                                  .
-- ]*[ ------------------------------------------------------------------ ]*[
-- .                                                                        .
-- .  Run against an existing x0 PostgreSQL database.                       .
-- .  The x0 framework must be set up first (see x0 repository).            .
-- .                                                                        .
-- ]*[ ------------------------------------------------------------------ ]*[

-- Application schema
CREATE SCHEMA IF NOT EXISTS github2sf;

-- ---------------------------------------------------------------------------
--  API Credentials storage
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS github2sf.credentials (
    credential_type   VARCHAR(20)  NOT NULL,
    username_or_email TEXT         NOT NULL,
    api_token         TEXT         NOT NULL,
    updated_at        TIMESTAMP    NOT NULL DEFAULT NOW(),
    CONSTRAINT pk_credentials PRIMARY KEY (credential_type)
);

COMMENT ON TABLE github2sf.credentials IS
    'Stores GitHub and Stackfield API credentials (one row per credential_type).';

-- ---------------------------------------------------------------------------
--  Application configuration key-value store
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS github2sf.app_config (
    config_key    VARCHAR(100) NOT NULL,
    value         TEXT,
    updated_at    TIMESTAMP    NOT NULL DEFAULT NOW(),
    CONSTRAINT pk_app_config PRIMARY KEY (config_key)
);

COMMENT ON TABLE github2sf.app_config IS
    'Key-value store for github2stackfield application runtime configuration.';

-- ---------------------------------------------------------------------------
--  Issue / Task mapping log
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS github2sf.issue_task_mapping (
    id                  SERIAL        NOT NULL,
    github_repo         TEXT          NOT NULL,
    github_issue_number INTEGER       NOT NULL,
    github_issue_title  TEXT,
    stackfield_room_id  TEXT          NOT NULL,
    stackfield_task_id  TEXT,
    stackfield_task_url TEXT,
    created_at          TIMESTAMP     NOT NULL DEFAULT NOW(),
    CONSTRAINT pk_issue_task_mapping PRIMARY KEY (id)
);

CREATE INDEX IF NOT EXISTS idx_issue_task_mapping_repo_issue
    ON github2sf.issue_task_mapping (github_repo, github_issue_number);

COMMENT ON TABLE github2sf.issue_task_mapping IS
    'Audit log of all GitHub issue → Stackfield task mappings created by the app.';
