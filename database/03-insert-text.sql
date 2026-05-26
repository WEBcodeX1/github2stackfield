-- ]*[ ------------------------------------------------------------------ ]*[
-- .   github2stackfield - UI Text / Localisation                          .
-- ]*[ ------------------------------------------------------------------ ]*[
-- .                                                                        .
-- .  Insert into the x0 webui.text table.                                  .
-- .  Both English and German translations are provided.                    .
-- .                                                                        .
-- ]*[ ------------------------------------------------------------------ ]*[

-- Navigation / Menu
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.MENU.SCREEN1', 'menu', 'API-Zugangsdaten', 'User Credentials');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.MENU.SCREEN2', 'menu', 'Issue / Aufgaben-Mapping', 'Issue / Task Mapping');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.MENU.SCREEN3', 'menu', 'Stackfield-Aufgabe verbinden', 'Connect Stackfield Task');

-- Screen 1 – GitHub Credentials
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN1.GITHUB.SECTION.HEADER',    'screen1', 'GitHub API-Zugangsdaten',         'GitHub API Credentials');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN1.GITHUB.SECTION.SUBHEADER', 'screen1', 'Benutzername und Personal Access Token eingeben', 'Enter your GitHub username and Personal Access Token');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN1.GITHUB.USER.LABEL',  'screen1', 'GitHub Benutzername', 'GitHub Username');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN1.GITHUB.TOKEN.LABEL', 'screen1', 'GitHub Personal Access Token', 'GitHub Personal Access Token');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN1.GITHUB.VERIFY.BUTTON', 'screen1', 'GitHub Zugangsdaten prüfen', 'Verify GitHub Credentials');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN1.GITHUB.VERIFY.NOTIFY', 'screen1', 'GitHub Authentifizierung', 'GitHub Authentication');

-- Screen 1 – Stackfield Credentials
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN1.STACKFIELD.SECTION.HEADER',    'screen1', 'Stackfield API-Zugangsdaten',      'Stackfield API Credentials');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN1.STACKFIELD.SECTION.SUBHEADER', 'screen1', 'E-Mail-Adresse und API-Token eingeben', 'Enter your Stackfield email and API token');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN1.STACKFIELD.EMAIL.LABEL', 'screen1', 'Stackfield E-Mail', 'Stackfield Email');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN1.STACKFIELD.TOKEN.LABEL', 'screen1', 'Stackfield API-Token', 'Stackfield API Token');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN1.STACKFIELD.VERIFY.BUTTON', 'screen1', 'Stackfield Zugangsdaten prüfen', 'Verify Stackfield Credentials');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN1.STACKFIELD.VERIFY.NOTIFY', 'screen1', 'Stackfield Authentifizierung', 'Stackfield Authentication');

-- Screen 2 – Search
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN2.SEARCH.SECTION.HEADER',    'screen2', 'GitHub Issues suchen',         'Search GitHub Issues');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN2.SEARCH.SECTION.SUBHEADER', 'screen2', 'Repository und Suchbegriff eingeben', 'Enter the repository and an optional search term');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN2.SEARCH.QUERY.LABEL', 'screen2', 'Suchbegriff (optional)', 'Search query (optional)');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN2.SEARCH.REPO.LABEL',  'screen2', 'Repository (owner/repo)', 'Repository (owner/repo)');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN2.SEARCH.BUTTON', 'screen2', 'Issues suchen', 'Search Issues');

-- Screen 2 – Issue List columns
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN2.LIST.COL.NUMBER',   'screen2', 'Nr.',        '#');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN2.LIST.COL.TITLE',    'screen2', 'Titel',      'Title');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN2.LIST.COL.STATE',    'screen2', 'Status',     'State');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN2.LIST.COL.CREATED',  'screen2', 'Erstellt',   'Created');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN2.LIST.COL.ASSIGNEE', 'screen2', 'Zugewiesen', 'Assignee');

-- Screen 2 – Context menu
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN2.CONTEXTMENU.CONNECT', 'screen2', 'Stackfield-Aufgabe verbinden', 'Connect Stackfield Task');

-- Screen 3 – GitHub Issue Details
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN3.ISSUE.SECTION.HEADER',    'screen3', 'GitHub Issue Eigenschaften',   'GitHub Issue Properties');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN3.ISSUE.SECTION.SUBHEADER', 'screen3', 'Daten aus der GitHub API',     'Data from the GitHub API');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN3.ISSUE.NUMBER.LABEL', 'screen3', 'Issue-Nummer', 'Issue Number');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN3.ISSUE.STATE.LABEL',  'screen3', 'Status',       'State');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN3.ISSUE.TITLE.LABEL',  'screen3', 'Titel',        'Title');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN3.ISSUE.URL.LABEL',    'screen3', 'GitHub URL',   'GitHub URL');

-- Screen 3 – Stackfield Mapping
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN3.STACKFIELD.SECTION.HEADER',    'screen3', 'Stackfield Aufgaben-Zuordnung',  'Stackfield Task Mapping');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN3.STACKFIELD.SECTION.SUBHEADER', 'screen3', 'Ziel-Raum und Aufgaben-Details', 'Target room and task details');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN3.STACKFIELD.ROOM.LABEL', 'screen3', 'Stackfield Raum-ID', 'Stackfield Room ID');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN3.TASK.TITLE.LABEL',    'screen3', 'Aufgaben-Titel',       'Task Title');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN3.TASK.DESC.LABEL',     'screen3', 'Beschreibung',         'Description');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN3.TASK.PRIORITY.LABEL', 'screen3', 'Priorität',            'Priority');

-- Screen 3 – Priority options
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN3.PRIORITY.LOW',    'screen3', 'Niedrig',    'Low');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN3.PRIORITY.MEDIUM', 'screen3', 'Mittel',     'Medium');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN3.PRIORITY.HIGH',   'screen3', 'Hoch',       'High');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN3.PRIORITY.URGENT', 'screen3', 'Dringend',   'Urgent');

-- Screen 3 – Create button
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN3.CREATE.BUTTON', 'screen3', 'Neue Stackfield-Aufgabe erstellen', 'Create New Stackfield Task');
INSERT INTO webui.text (id, "group", value_de, value_en) VALUES
    ('TXT.SCREEN3.CREATE.NOTIFY', 'screen3', 'Stackfield Aufgabe erstellen',      'Create Stackfield Task');
