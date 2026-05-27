-- ]*[ ------------------------------------------------------------------ ]*[
-- .   github2stackfield - x0 Application Configuration                    .
-- ]*[ ------------------------------------------------------------------ ]*[
-- .                                                                        .
-- .  Insert the x0 system.config rows for the github2stackfield app.       .
-- .  Adjust app_id value if your x0 setup uses a different identifier.     .
-- .                                                                        .
-- ]*[ ------------------------------------------------------------------ ]*[

-- Remove any previously inserted config for this app
DELETE FROM system.config WHERE app_id = 'github2sf';

INSERT INTO system.config (app_id, config_group, "value") VALUES
    ('github2sf', 'index_title',         'GitHub ↔ Stackfield Connector'),
    ('github2sf', 'debug_level',         '0'),
    ('github2sf', 'display_language',    'en'),
    ('github2sf', 'default_screen',      'Screen1'),
    ('github2sf', 'parent_window_url',   'null'),
    ('github2sf', 'subdir',              '/static/github2sf'),
    ('github2sf', 'config_file_menu',    'menu.json'),
    ('github2sf', 'config_file_object',  'object.json'),
    ('github2sf', 'config_file_skeleton','skeleton.json');
