# ]*[ --------------------------------------------------------------------- ]*[
#  .           github2stackfield - python-micro-esb Service Router            .
# ]*[ --------------------------------------------------------------------- ]*[
#  .                                                                         .
#  .  Defines routing functions called by ServiceRouter.send().               .
#  .  Each function receives a metadata dict from the x0 frontend and        .
#  .  returns a result dict.                                                  .
#  .                                                                         .
# ]*[ --------------------------------------------------------------------- ]*[

import logging
import psycopg2

import DB
from pgdbpool import pool

from service_implementation import GitHubService, StackfieldService

logger = logging.getLogger(__name__)

pool.Connection.init(DB.config)

# ---------------------------------------------------------------------------
#  Credential helpers
# ---------------------------------------------------------------------------

def _load_credentials(dbcon, cred_type):
    """Load stored API credentials from database."""
    try:
        with dbcon.cursor() as crs:
            crs.execute(
                """
                SELECT username_or_email, api_token
                    FROM github2sf.credentials
                WHERE credential_type = %s
                """,
                (cred_type,)
            )
            row = crs.fetchone()
            if row:
                return {'username_or_email': row[0], 'api_token': row[1]}
    except Exception as e:
        logger.error('_load_credentials() error:{}'.format(e))
    return {}


def _store_credentials(dbcon, cred_type, username_or_email, api_token):
    """Persist API credentials to the database."""
    try:
        with dbcon.cursor() as crs:
            crs.execute(
                """
                INSERT INTO github2sf.credentials
                    (credential_type, username_or_email, api_token)
                VALUES (%s, %s, %s)
                ON CONFLICT (credential_type) DO UPDATE
                    SET username_or_email = EXCLUDED.username_or_email,
                        api_token         = EXCLUDED.api_token,
                        updated_at        = NOW()
                """,
                (cred_type, username_or_email, api_token)
            )
        dbcon.commit()
    except Exception as e:
        logger.error('_store_credentials() error:{}'.format(e))
        dbcon.rollback()


# ---------------------------------------------------------------------------
#  Routing functions
# ---------------------------------------------------------------------------

def verify_github(metadata):
    """Verify GitHub API credentials and persist them on success.

    :param dict metadata: expects keys GitHubUserInput, GitHubTokenInput
    :return: result dict with success flag
    """
    logger.debug('user_routing.verify_github() metadata:{}'.format(metadata))

    svc = GitHubService()
    svc.github_user = metadata.get('GitHubUserInput', '')
    svc.github_token = metadata.get('GitHubTokenInput', '')
    svc.verify()

    if svc.result.get('success'):
        with pool.Handler('x0') as db:
            _store_credentials(
                db.connection,
                'github',
                svc.github_user,
                svc.github_token
            )

    return svc.result


def verify_stackfield(metadata):
    """Verify Stackfield API credentials and persist them on success.

    :param dict metadata: expects keys StackfieldEmailInput, StackfieldTokenInput
    :return: result dict with success flag
    """
    logger.debug('user_routing.verify_stackfield() metadata:{}'.format(metadata))

    svc = StackfieldService()
    svc.stackfield_email = metadata.get('StackfieldEmailInput', '')
    svc.stackfield_token = metadata.get('StackfieldTokenInput', '')
    svc.verify()

    if svc.result.get('success'):
        with pool.Handler('x0') as db:
            _store_credentials(
                db.connection,
                'stackfield',
                svc.stackfield_email,
                svc.stackfield_token
            )

    return svc.result


def search_github_issues(metadata):
    """Search GitHub issues using stored credentials.

    :param dict metadata: expects keys SearchQueryInput, SearchRepoInput
    :return: indexed dict of issue rows for x0 List population
    """
    logger.debug('user_routing.search_github_issues() metadata:{}'.format(metadata))

    with pool.Handler('x0') as db:
        creds = _load_credentials(db.connection, 'github')

    if not creds:
        return {'error': True, 'error_message': 'GitHub credentials not configured.'}

    svc = GitHubService()
    svc.github_user = creds['username_or_email']
    svc.github_token = creds['api_token']
    svc.repo = metadata.get('SearchRepoInput', '')
    svc.search_query = metadata.get('SearchQueryInput', '')
    svc.search_issues()

    return svc.result


def get_github_issue_details(metadata):
    """Fetch detailed GitHub issue data for Screen 3 population.

    :param dict metadata: expects key issue_number; repo loaded from DB
    :return: single-row dict for x0 FormfieldList population
    """
    logger.debug('user_routing.get_github_issue_details() metadata:{}'.format(metadata))

    with pool.Handler('x0') as db:
        creds = _load_credentials(db.connection, 'github')

    if not creds:
        return {0: {'error': 'GitHub credentials not configured.'}}

    # Repo may be stored as a mapping state or passed via global var.
    # Fall back to a stored repo config entry.
    repo = metadata.get('repo', '')
    if not repo:
        with pool.Handler('x0') as db:
            try:
                with db.connection.cursor() as crs:
                    crs.execute(
                        """
                        SELECT value FROM github2sf.app_config
                        WHERE config_key = 'last_search_repo'
                        """
                    )
                    row = crs.fetchone()
                    if row:
                        repo = row[0]
            except Exception:
                pass

    svc = GitHubService()
    svc.github_user = creds['username_or_email']
    svc.github_token = creds['api_token']
    svc.repo = repo
    svc.issue_number = metadata.get('issue_number', '')
    svc.get_issue_details()

    return svc.result


def create_stackfield_task(metadata):
    """Create a new Stackfield task from GitHub issue data.

    :param dict metadata: expects task fields and Stackfield room ID
    :return: result dict with success flag and new task URL
    """
    logger.debug('user_routing.create_stackfield_task() metadata:{}'.format(metadata))

    with pool.Handler('x0') as db:
        creds = _load_credentials(db.connection, 'stackfield')

    if not creds:
        return {'success': False, 'error': 'Stackfield credentials not configured.'}

    svc = StackfieldService()
    svc.stackfield_email = creds['username_or_email']
    svc.stackfield_token = creds['api_token']
    svc.room_id = metadata.get('StackfieldRoomInput', '')
    svc.task_title = metadata.get('TaskTitleInput', '')
    svc.task_description = metadata.get('TaskDescInput', '')
    svc.task_priority = metadata.get('TaskPriorityPulldown', 'medium')
    svc.github_issue_number = metadata.get('number', '')
    svc.github_issue_url = metadata.get('html_url', '')
    svc.create_task()

    return svc.result
