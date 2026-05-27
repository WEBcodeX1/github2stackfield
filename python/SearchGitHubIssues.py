# ]*[ --------------------------------------------------------------------- ]*[
#  .    github2stackfield - Search GitHub Issues WSGI Endpoint                .
# ]*[ --------------------------------------------------------------------- ]*[
#  .                                                                         .
#  .  Called by x0 IssueSearchConnector (ServiceConnector).                  .
#  .  Searches GitHub issues and returns indexed rows for the IssueList.      .
#  .  Credentials are loaded from the database (set via Screen 1).           .
#  .                                                                         .
# ]*[ --------------------------------------------------------------------- ]*[

import sys
import json

sys.path.insert(0, '/var/www/vhosts/x0/python/github2sf')

import POSTData
from StdoutLogger import logger

from microesb.router import ServiceRouter


def application(environ, start_response):

    start_response('200 OK', [('Content-Type', 'application/json; charset=UTF-8')])

    if environ['REQUEST_METHOD'].upper() != 'POST':
        yield bytes(json.dumps({}), 'utf-8')
        return

    try:
        raw = POSTData.Environment.getPOSTData(environ)
        service_json = json.loads(raw)

        request_data = service_json.get('RequestData', {})

        logger.debug('SearchGitHubIssues RequestData:{}'.format(request_data))

        router = ServiceRouter()
        result = router.send('search_github_issues', request_data)

        logger.debug('SearchGitHubIssues result rows:{}'.format(len(result)))

        # Ensure result keys are strings (x0 List expects string-keyed indexed rows)
        if isinstance(result, dict) and 'error' not in result:
            result = {str(k): v for k, v in result.items()}

        yield bytes(json.dumps(result), 'utf-8')

    except Exception as e:
        logger.error('SearchGitHubIssues exception:{}'.format(e))
        error_result = {
            'error': True,
            'error_id': 500,
            'exception': str(e)
        }
        yield bytes(json.dumps(error_result), 'utf-8')
