# ]*[ --------------------------------------------------------------------- ]*[
#  .    github2stackfield - Get GitHub Issue Details WSGI Endpoint            .
# ]*[ --------------------------------------------------------------------- ]*[
#  .                                                                         .
#  .  Called by x0 IssueDetailsConnector (ServiceConnector) on Screen 3.     .
#  .  Fetches full GitHub issue details and pre-populates Screen 3            .
#  .  formfields (IssueDetailsForm + StackfieldMappingForm task fields).     .
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

        logger.debug('GetGitHubIssueDetails RequestData:{}'.format(request_data))

        router = ServiceRouter()
        result = router.send('get_github_issue_details', request_data)

        logger.debug('GetGitHubIssueDetails result:{}'.format(result))

        # x0 FormfieldList expects {"0": {...field values...}}
        if isinstance(result, dict) and 0 in result:
            result = {'0': result[0]}

        yield bytes(json.dumps(result), 'utf-8')

    except Exception as e:
        logger.error('GetGitHubIssueDetails exception:{}'.format(e))
        error_result = {
            'error': True,
            'error_id': 500,
            'exception': str(e)
        }
        yield bytes(json.dumps(error_result), 'utf-8')
