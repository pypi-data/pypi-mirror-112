from .values import cluster_endpoints as endpoints
from .values import TOKEN_PROGRAM_ID
from .rpc import async_requests
from . import rpc
from .log import log
from pprint import pprint


class Connection():
    """ deals with Solana RPC Connections """
    def __init__(self, endpoint=endpoints.MAINNET_BETA):
        self.endpoint = endpoint

    def get_signatures( self, pubkeys, before_sigs=None, limits=None, until_sigs=None):
        """ input: 
                pubkeys:     list of pubkeys to get signatures for asynchronously
                before_sigs: None or list of signatures (or Nones) for each pubkey
                             returned signatures for a given pubkey will start before 
                             that signature. Use None to retreive latest signatures
                limits:      None or list for how many signatures to return for each pubkey
                             Default = Max = 1000
                until_sigs:  None or list of stop signatures - returns up to that signature
                             for each pubkey.
            return:          dictionary of confirmed signatures for each pubkey
                { 
                    <pubkey> : {
                        'status_code': 200 | -1, 
                        'signatures': [
                            { # default response
                                'blockTime': 1626129650,
                                'confirmationStatus': 'finalized',
                                'err': None,
                                'memo': None,
                                'signature': '5s9iipyNRzs3rH6...',
                                'slot': 86803241}
                            }, ...
                        ]
                    }, ...
                }
        """
        # 0. some initial variables
        num_pubkeys = len(pubkeys)
        request_params = []
        results = {
            pubkey: {
                'status_code': -1,
                'signatures': []
            } for pubkey in pubkeys
        }

        # 1. security checks
        try:    
            if before_sigs and len(before_sigs) != num_pubkeys:
                raise Exception("length of pubkeys should equal length of before_sigs")
            if limits and len(limits) != num_pubkeys:
                raise Exception("length of pubkeys should equal length of limits")
            if until_sigs and len(until_sigs) != num_pubkeys:
                raise Exception("length of pubkeys should equal length of until_sigs")
        except Exception as e:
            log('get_signatures()', e)

        # 2. generate parameters for async requests
        for i in range(num_pubkeys):
            pubkey = pubkeys[i]
            method = "getConfirmedSignaturesForAddress2"
            ops = dict()
            if before_sigs and before_sigs[i]: ops['before'] = before_sigs[i]
            if until_sigs and until_sigs[i]: ops['until'] = until_sigs[i]
            if limits and limits[i]: ops['limit'] = limits[i]
            params = [pubkey, ops]

            request_params.append( {
                'endpoint': self.endpoint,
                'method': method,
                'params': params,
                'request_id': i
            } )

        # 3. make async rpc requests and get raw responses
        raw_responses = async_requests( request_params )

        # 4. format raw responses into acceptable way
        for raw_reponse in raw_responses:
            try:
                if raw_reponse['status'] == 200:
                    pubkey_idx = raw_reponse['result']['id']
                    pubkey = pubkeys[ pubkey_idx ]
                    results[pubkey] = {
                        'status_code': 200,
                        'signatures': raw_reponse['result']['result']
                    }
            except Exception as e:
                log(e, e)
        return results

    def get_transaction_balances(self, signatures : list):
        """ input list of pubkeys with their signatures to decode
                signatures = { 
                    [ { 'signature': <signature>, 'pubkey': <pubkey> }, ... ] }
            returns 
                responses = [
                    {
                        'signature': <signature>,
                        'pubkey': <pubkey>,
                        'status_code': 200 | -1,
                        'pre_sol' : float,
                        'post_sol': float,
                        'pre_token' : float, # = 0 if it's not a token account
                        'post_token': float  # = 0 if it's not a token account
                    }, ...
                ] """
        # 0. some initial variables
        num_signatures = len(signatures)
        request_params = []
        results = [
            {
                'signature': signature['signature'],
                'pubkey': signature['pubkey'],
                'status_code': -1,
                'pre_sol' : 0,
                'post_sol': 0,
                'pre_token' : 0,
                'post_token': 0
            } for signature in signatures
        ]

        # 1. generate parameters for async requests
        for i in range(num_signatures):
            signature = signatures[i]['signature']
            method = "getConfirmedTransaction"
            ops = {"encoding": "jsonParsed"}
            params = [signature, ops]

            request_params.append( {
                'endpoint': self.endpoint,
                'method': method,
                'params': params,
                'request_id': i
            })
        
        # 2. make async rpc requests and get raw responses
        raw_responses = async_requests( request_params )

        # 3. format raw responses in acceptable way
        for i in range(num_signatures):
            raw_response = raw_responses[i]
            # get balances from the response
            balances = {}
            try:
                # get the index with which we'll look up the right signature for results
                response_id = raw_response['result']['id']
                pre_token_balances = {}
                post_token_balances = {}
                pre_sol_balances = {}
                post_sol_balances = {}
                # get pre and post token balances as well as sol balances
                if raw_response['status'] == 200:
                    if raw_response['result']['result'] != None:
                        transaction = raw_response['result']['result']['transaction']
                        meta = raw_response['result']['result']['meta']
                        
                        # get all pubkeys that were in the transaction
                        pubkeys = [ 
                            key['pubkey'] for key in transaction['message']['accountKeys']
                        ]
                        # get all available pre token balances
                        pre_token_balances = {
                            pubkeys[ pre_token_balance['accountIndex'] ] : float(pre_token_balance['uiTokenAmount']['uiAmountString'])
                            for pre_token_balance in meta['preTokenBalances']
                        }
                        # get all available post token balances
                        post_token_balances = {
                            pubkeys[ post_token_balance['accountIndex'] ] : float(post_token_balance['uiTokenAmount']['uiAmountString'] )
                            for post_token_balance in meta['postTokenBalances']
                        }
                        # get all available pre sol balances (every account should have it)
                        pre_sol_balances = { 
                            pubkeys[i] : meta['preBalances'][i] / 10**9
                            for i in range(len(pubkeys))
                        }
                        # get all available post sol balances (every account should have it)
                        post_sol_balances = { 
                            pubkeys[i] : meta['postBalances'][i] / 10**9
                            for i in range(len(pubkeys))
                        }
                        # combine balances into a single variable
                        for pubkey in pubkeys:
                            balances[ pubkey ] = {
                                'pre_sol': pre_sol_balances[ pubkey ] if pubkey in pre_sol_balances else 0,
                                'post_sol':  post_sol_balances[ pubkey ] if pubkey in post_sol_balances else 0,
                                'pre_token':  pre_token_balances[ pubkey ] if pubkey in pre_token_balances else 0,
                                'post_token':  post_token_balances[ pubkey ] if pubkey in post_token_balances else 0
                            }
            except Exception as e:
                log(e, exception=e)

            # add balances to that signature response
            pubkey = results[response_id]['pubkey']
            if pubkey in balances:
                results[response_id]['pre_sol'] = balances[pubkey]['pre_sol']
                results[response_id]['post_sol'] = balances[pubkey]['post_sol']
                results[response_id]['pre_token'] = balances[pubkey]['pre_token']
                results[response_id]['post_token'] = balances[pubkey]['post_token']
                results[response_id]['status_code'] = 200
            else:
                log(' WARNING: in get_transaction_balances(). pubkey "{}" was not found in signature accounts'.format(
                    pubkey))
        
        # 4. return responses
        return results

    def get_token_accounts(self, pubkeys : list):
        """ input: list of wallet account pubkeys 
            returns 
                responses = {
                     <pubkey1> : { 
                         'status_code': 200 | -1, 
                         'accounts' :[ <tokenAccount1>, ...]
                    }, ...
                } """
        # 0. some initial variables
        requests_params = []
        results = { 
            pubkey: {
                'status_code': -1, 
                'accounts': []
            } for pubkey in pubkeys 
        }
        
        # 1. remove duplicate pubkeys if any
        pubkeys = list(set(pubkeys))
        
        # 2. generate parameters for async requests
        for pubkey_idx in range(len(pubkeys)):
            pubkey = pubkeys[pubkey_idx]
            method = "getTokenAccountsByOwner"
            ops1 = {"programId": TOKEN_PROGRAM_ID}
            ops2 = {"encoding": "jsonParsed"}
            params = [pubkey, ops1, ops2]
            
            requests_params.append( { 
                'endpoint': self.endpoint,
                'method': method,
                'params': params,
                'request_id': pubkey_idx 
            } )

        # 3. make async rpc requests and get raw responses
        raw_responses = async_requests( requests_params )
        
        # 4. format raw responses acceptable way
        for raw_response in raw_responses:
            try:
                if raw_response['status'] == 200:
                    pubkey_idx = raw_response['result']['id']
                    owner = pubkeys[pubkey_idx]

                    raw_token_accounts = raw_response[
                        'result']['result']['value']
                    token_accounts = [
                        token_account['pubkey'] for token_account in raw_token_accounts
                    ]
                    results[owner] = {'status_code': 200, 'accounts': token_accounts}
            except Exception as e:
                log(e, exception=e)

        # 5. return responses
        return results


