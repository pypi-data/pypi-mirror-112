from .values import cluster_endpoints as endpoints
from .values import TOKEN_PROGRAM_ID
from .values import STATUS_OK
from .rpc import request
from . import rpc


def _safe_return(response_raw, fail_result=[]):
    """ checks the status of response_raw.
        if ok, returns { 'status': STATUS_OK, 'result': response result }
        if fail, returns { 'status': response status, 'result': fail_result } 
    """
    try:
        if response_raw['status'] != rpc.STATUS_OK:
            print("[D] 24398 >>> get_signatures call did not return OK status")
            print("\tReturning empty...")
            return { 'status': response_raw['status'], 'result': [] }
    except Exception as e:
        print("[D] 84721 >>> safety check exception: {}\n\t returning empty".format(e))
        return { 'status': e, 'result': fail_result}
    return { 'status': STATUS_OK, 'result': response_raw['result'] }

class Connection():
    """ deals with Solana RPC Connections """
    def __init__(self, endpoint=endpoints.MAINNET_BETA):
        self.endpoint = endpoint

    def get_signatures( self, pubkey, before_sig=None, limit=None, until_sig=None):
        """ get confirmed signatures for pubkey.
            returns {
                'status': values.STATUS_OK | other error status from RPC
                'result': [list_of_signatures] 
            }
        """
        # define parameters for request
        method = "getConfirmedSignaturesForAddress2"
        ops = dict()
        if before_sig: ops['before'] = before_sig
        if until_sig: ops['until'] = until_sig
        if limit: ops['limit'] = limit
        params = [pubkey, ops]

        # get response
        response_raw = request(self.endpoint, method, params)
        return _safe_return(response_raw, [])

    def get_transaction_data(self, signature):
        """ gets human readable transaction data for signature
            returns {
                'status': values.STATUS_OK | other error status from RPC
                'result': {dict of transaction data} 
            }
         """
        method = "getConfirmedTransaction"
        ops = {"encoding": "jsonParsed"}
        params = [signature, ops]

        # make rpc request
        response_raw = request(self.endpoint, method, params)
        return _safe_return(response_raw, dict())

    def get_token_accounts(self, pubkey):
        """ returns list of token accounts for the pubkey """
        method = "getTokenAccountsByOwner"
        ops1 = {"programId": TOKEN_PROGRAM_ID}
        ops2 = {"encoding": "jsonParsed"}
        params = [pubkey, ops1, ops2]
        # make rpc request
        response_raw = request(self.endpoint, method, params)
        return _safe_return(response_raw, list())



