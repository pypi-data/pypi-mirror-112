import json
import requests

STATUS_OK = 200
DEFAULT_HEADERS = {'Content-Type': 'application/json'}

def _return_result(status, response):
    return {
        "status": status,
        "result": response
    }

def request(endpoint, method, params, request_id=1):
    """ returns { "status":status, "result":result }
        result is json loaded (dict or list) 
        if request successful, status should be equal to 200 """
    # log
    print('[D] 4234 >>> sending request:\n\t endpoint: {}, method: {}, params: {}'.format(
        endpoint, method, params
    ))

    try:
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "method": method,
                "params": params  
            }
        )
        # POST request and look at the response
        response_raw = requests.post(endpoint, headers=DEFAULT_HEADERS, data=data)
        status = response_raw.status_code
        response = json.loads(response_raw.text)

        # status checks and returns
        if status != STATUS_OK:
            print("[D] 50398 >>> error when requesting. Status code: {}".format(status))
            print("\tResponse: {}\n".response)
            return _return_result(status, response)
        try:
            return _return_result(status, response['result'])
        except Exception as e:
            print("[D] 43903 >>> error when requesting. Exception: {}".format(e))
            return _return_result(e, None)
    except Exception as e:
        print("[D] 32985 >>> error when requesting. Exception: {}".format(e))
        return _return_result(e, None)
        