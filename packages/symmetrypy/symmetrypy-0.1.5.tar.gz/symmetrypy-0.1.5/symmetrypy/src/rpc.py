import json
# import requests
import asyncio
from typing import final
import aiohttp
from .log import log

STATUS_OK = 200
STATUS_FAIL = -1
DEFAULT_HEADERS = {'Content-Type': 'application/json'}

def _return_result(status, response):
    return {
        "status": status,
        "result": response
    }

async def _request(session, request_info):
    """ request_info = {
                'endpoint': endpoint,
                'headers': headers,
                'data': data
        }
    """
    endpoint = request_info['endpoint']
    headers = request_info['headers']
    data = request_info['data']

    async with session.post(endpoint, headers=headers, data=data) as response:
        result = await response.json()
        return result

async def _requests_runner(request_infos : list):
    """ request_infos = [
            {
                'endpoint': endpoint,
                'headers': headers,
                'data': data
            }, ...
        ]

        returns:

    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for request_info in request_infos:
            task = asyncio.ensure_future( _request(session, request_info) )
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        return responses


def async_requests(requests_params : list):
    """ requests_params = [
            {
                'endpoint' : endpoint, 
                'method' : method, 
                'params': params, 
                'request_id : request_id'
            },
            ...
        ] """
    responses = []

    try:
        request_infos = []
        for param in requests_params:
            data = json.dumps({
                    "jsonrpc": "2.0",
                    "id": param['request_id'],
                    "method": param['method'],
                    "params": param['params']
            })
            request_infos.append( {
                    'endpoint': param['endpoint'], 
                    'headers': DEFAULT_HEADERS, 
                    'data': data
            })
        # POST request and look at the response
        responses_raw = asyncio.run( _requests_runner( request_infos ) )
        for response_raw in responses_raw:
            status = STATUS_OK
            # check if there was an error:
            if 'error' in response_raw:
                status = STATUS_FAIL
                log("WARNING: \"{}\" for request ID: {}. ErrorCode: {}\n\tparams: {}".format(
                    response_raw['error']['message'], 
                    response_raw['id'],
                    response_raw['error']['code'],
                    requests_params
                ))
            # append the result to the responses
            responses.append( _return_result(status, response_raw))
    except Exception as e:
        log(e, exception=e)
    return responses