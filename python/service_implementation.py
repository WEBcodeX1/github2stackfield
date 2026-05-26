# ]*[ --------------------------------------------------------------------- ]*[
#  .           github2stackfield - Service Implementation Classes             .
# ]*[ --------------------------------------------------------------------- ]*[
#  .                                                                         .
#  .  Provides ClassHandler-based service classes for GitHub and Stackfield   .
#  .  API integration, used via python-micro-esb ServiceRouter routing.       .
#  .                                                                         .
# ]*[ --------------------------------------------------------------------- ]*[

import logging
import requests

from microesb import microesb

logger = logging.getLogger(__name__)


class GitHubService(microesb.ClassHandler):
    """GitHub API service handler.

    Provides methods to interact with the GitHub REST API v3 for
    credential verification and issue retrieval.
    """

    BASE_URL = 'https://api.github.com'

    def __init__(self):
        super().__init__()
        self.github_user = None
        self.github_token = None
        self.repo = None
        self.issue_number = None
        self.search_query = None
        self.result = {}

    def _get_auth(self):
        return (self.github_user, self.github_token)

    def _get_headers(self):
        return {
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }

    def verify(self):
        """Verify GitHub credentials by calling the /user endpoint."""
        logger.debug('GitHubService.verify() user:{}'.format(self.github_user))
        try:
            resp = requests.get(
                '{}/user'.format(self.BASE_URL),
                auth=self._get_auth(),
                headers=self._get_headers(),
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json()
                self.result = {
                    'success': True,
                    'login': data.get('login', ''),
                    'name': data.get('name', ''),
                    'public_repos': str(data.get('public_repos', 0))
                }
            else:
                self.result = {
                    'success': False,
                    'error': 'Authentication failed (HTTP {})'.format(resp.status_code)
                }
        except requests.exceptions.RequestException as e:
            logger.error('GitHubService.verify() exception:{}'.format(e))
            self.result = {'success': False, 'error': str(e)}

    def search_issues(self):
        """Search GitHub issues in the configured repository."""
        logger.debug('GitHubService.search_issues() repo:{} query:{}'.format(
            self.repo, self.search_query
        ))
        try:
            params = {
                'q': '{} repo:{} is:issue'.format(
                    self.search_query or '', self.repo or ''
                ),
                'per_page': 50,
                'sort': 'updated',
                'order': 'desc'
            }
            resp = requests.get(
                '{}/search/issues'.format(self.BASE_URL),
                params=params,
                auth=self._get_auth(),
                headers=self._get_headers(),
                timeout=15
            )
            resp.raise_for_status()
            data = resp.json()
            issues = data.get('items', [])
            self.result = {}
            for idx, issue in enumerate(issues):
                assignee = issue.get('assignee')
                self.result[idx] = {
                    'issue_number': str(issue.get('number', '')),
                    'number': '#{}'.format(issue.get('number', '')),
                    'title': issue.get('title', ''),
                    'state': issue.get('state', ''),
                    'created_at': str(issue.get('created_at', ''))[:10],
                    'assignee': assignee.get('login', '') if assignee else '',
                    'html_url': issue.get('html_url', ''),
                    'body': issue.get('body', '') or ''
                }
        except requests.exceptions.RequestException as e:
            logger.error('GitHubService.search_issues() exception:{}'.format(e))
            self.result = {'error': True, 'error_message': str(e)}

    def get_issue_details(self):
        """Fetch detailed data for a specific GitHub issue."""
        logger.debug('GitHubService.get_issue_details() repo:{} issue:{}'.format(
            self.repo, self.issue_number
        ))
        try:
            resp = requests.get(
                '{}/repos/{}/issues/{}'.format(
                    self.BASE_URL, self.repo, self.issue_number
                ),
                auth=self._get_auth(),
                headers=self._get_headers(),
                timeout=10
            )
            resp.raise_for_status()
            issue = resp.json()
            assignee = issue.get('assignee')
            body = issue.get('body', '') or ''
            self.result = {
                0: {
                    'number': str(issue.get('number', '')),
                    'title': issue.get('title', ''),
                    'state': issue.get('state', ''),
                    'html_url': issue.get('html_url', ''),
                    'body': body,
                    'assignee': assignee.get('login', '') if assignee else '',
                    'labels': ', '.join(
                        lbl.get('name', '') for lbl in issue.get('labels', [])
                    ),
                    'task_title': issue.get('title', ''),
                    'task_description': body,
                    'stackfield_room_id': '',
                    'task_priority': 'medium'
                }
            }
        except requests.exceptions.RequestException as e:
            logger.error('GitHubService.get_issue_details() exception:{}'.format(e))
            self.result = {'error': True, 'error_message': str(e)}


class StackfieldService(microesb.ClassHandler):
    """Stackfield API service handler.

    Provides methods to interact with the Stackfield REST API for
    credential verification and task creation.

    Stackfield API reference: https://stackfield.com/rest-api
    """

    BASE_URL = 'https://www.stackfield.com/api'

    def __init__(self):
        super().__init__()
        self.stackfield_email = None
        self.stackfield_token = None
        self.room_id = None
        self.task_title = None
        self.task_description = None
        self.task_priority = None
        self.github_issue_number = None
        self.github_issue_url = None
        self.result = {}

    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.stackfield_token)
        }

    def verify(self):
        """Verify Stackfield credentials by fetching user profile."""
        logger.debug('StackfieldService.verify() email:{}'.format(self.stackfield_email))
        try:
            resp = requests.get(
                '{}/v1/user'.format(self.BASE_URL),
                headers=self._get_headers(),
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json()
                self.result = {
                    'success': True,
                    'user_id': str(data.get('id', '')),
                    'name': data.get('name', ''),
                    'email': data.get('email', '')
                }
            else:
                self.result = {
                    'success': False,
                    'error': 'Authentication failed (HTTP {})'.format(resp.status_code)
                }
        except requests.exceptions.RequestException as e:
            logger.error('StackfieldService.verify() exception:{}'.format(e))
            self.result = {'success': False, 'error': str(e)}

    def create_task(self):
        """Create a new task in a Stackfield room from GitHub issue data."""
        logger.debug('StackfieldService.create_task() room:{} title:{}'.format(
            self.room_id, self.task_title
        ))
        try:
            priority_map = {
                'low': 1,
                'medium': 2,
                'high': 3,
                'urgent': 4
            }
            priority_value = priority_map.get(self.task_priority or 'medium', 2)

            description = self.task_description or ''
            if self.github_issue_url:
                description = '{}\n\n---\nGitHub Issue: {}'.format(
                    description, self.github_issue_url
                )

            payload = {
                'title': self.task_title,
                'content': description,
                'priority': priority_value
            }

            resp = requests.post(
                '{}/v1/rooms/{}/tasks'.format(self.BASE_URL, self.room_id),
                headers=self._get_headers(),
                json=payload,
                timeout=15
            )
            resp.raise_for_status()
            data = resp.json()
            self.result = {
                'success': True,
                'task_id': str(data.get('id', '')),
                'task_url': data.get('url', '')
            }
        except requests.exceptions.RequestException as e:
            logger.error('StackfieldService.create_task() exception:{}'.format(e))
            self.result = {'success': False, 'error': str(e)}
