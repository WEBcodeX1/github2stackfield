# ]*[ --------------------------------------------------------------------- ]*[
#  .    github2stackfield - Verify GitHub Credentials WSGI Endpoint           .
# ]*[ --------------------------------------------------------------------- ]*[
#  .                                                                         .
#  .  Called by x0 GitHubVerifyButton (OnClick).                             .
#  .  Validates GitHub API user/token and stores them in the database.        .
#  .                                                                         .
# ]*[ --------------------------------------------------------------------- ]*[

import sys
import json

import POSTData
from StdoutLogger import logger

from router import ServiceRouter


def application(environ, start_response):

    start_response('200 OK', [('Content-Type', 'application/json; charset=UTF-8')])

    if environ['REQUEST_METHOD'].upper() != 'POST':
        yield bytes(json.dumps({'error': True, 'error_id': 400}), 'utf-8')
        return

    try:
        raw = POSTData.Environment.getPOSTData(environ)
        service_json = json.loads(raw)

        request_data = service_json.get('RequestData', {})

        logger.debug('VerifyGitHubCredentials RequestData:{}'.format(request_data))

        router = ServiceRouter()
        result = router.send('verify_github', request_data)

        logger.debug('VerifyGitHubCredentials result:{}'.format(result))

        yield bytes(json.dumps(result), 'utf-8')

    except Exception as e:
        logger.error('VerifyGitHubCredentials exception:{}'.format(e))
        error_result = {
            'error': True,
            'error_id': 500,
            'exception': str(e)
        }
        yield bytes(json.dumps(error_result), 'utf-8')
