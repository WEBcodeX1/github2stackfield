# ]*[ --------------------------------------------------------------------- ]*[
#  .    github2stackfield - Create Stackfield Task WSGI Endpoint              .
# ]*[ --------------------------------------------------------------------- ]*[
#  .                                                                         .
#  .  Called by x0 CreateStackfieldTaskButton (OnClick).                     .
#  .  Creates a new Stackfield task from GitHub issue data collected on       .
#  .  Screen 3. Stackfield credentials are loaded from the database.         .
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

        logger.debug('CreateStackfieldTask RequestData:{}'.format(request_data))

        router = ServiceRouter()
        result = router.send('create_stackfield_task', request_data)

        logger.debug('CreateStackfieldTask result:{}'.format(result))

        yield bytes(json.dumps(result), 'utf-8')

    except Exception as e:
        logger.error('CreateStackfieldTask exception:{}'.format(e))
        error_result = {
            'error': True,
            'error_id': 500,
            'exception': str(e)
        }
        yield bytes(json.dumps(error_result), 'utf-8')
