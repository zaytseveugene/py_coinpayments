from urllib import request, parse, error
import hmac
import hashlib
import json
from collections import namedtuple

API_KEY = ''


def _json_hook(d):
    return namedtuple('X', list(d.keys()))(*list(d.values()))


def p_object(data):
    return json.loads(data, object_hook=_json_hook).result


class CryptoPayments:
    url = 'https://www.coinpayments.net/api.php'

    def __init__(self, public_key, private_key, ipn_url):
        self.public_key = public_key
        self.private_key = private_key
        self.ipn_url = ipn_url
        self.format = 'json'
        self.version = 1

    def create_hmac(self, **params):
        """ Generate an HMAC based upon the url arguments/parameters
            
            We generate the encoded url here and return it to Request because
            the hmac on both sides depends upon the order of the parameters, any
            change in the order and the hmacs wouldn't match
        """
        encoded = parse.urlencode(params).encode('utf-8')
        return encoded, hmac.new(bytearray(self.private_key, 'utf-8'), encoded, hashlib.sha512).hexdigest()

    def request(self, request_method, **params):
        """The basic request that all API calls use

            the parameters are joined in the actual api methods so the parameter
            strings can be passed and merged inside those methods instead of the 
            request method. The final encoded URL and HMAC are generated here
        """
        encoded, sig = self.create_hmac(**params)

        headers = {'hmac': sig}

        req = None
        if request_method == 'get':
            req = request.Request(self.url, headers=headers)
        elif request_method == 'post':
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            req = request.Request(self.url, data=encoded, headers=headers)

        try:
            response = request.urlopen(req)
            # status_code = response.getcode()
            response_body = response.read()
        except error.HTTPError as e:
            # status_code = e.getcode()
            response_body = e.read()

        return p_object(response_body)

    def create_transaction(self, params=None):
        """ Creates a transaction to give to the purchaser
            https://www.coinpayments.net/apidoc-create-transaction
        """
        if params is None:
            params = {}
        params.update({'cmd': 'create_transaction',
                       'ipn_url': self.ipn_url,
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.request('post', **params)

    def get_basic_info(self, params=None):
        """Gets merchant info based on API key (callee)
           https://www.coinpayments.net/apidoc-get-basic-info
        """
        if params is None:
            params = {}
        params.update({'cmd': 'get_basic_info',
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.request('post', **params)

    def rates(self, params=None):
        """Gets current rates for currencies
           https://www.coinpayments.net/apidoc-rates 
        """
        if params is None:
            params = {}
        params.update({'cmd': 'rates',
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.request('post', **params)

    def balances(self, params=None):
        """Get current wallet balances
            https://www.coinpayments.net/apidoc-balances
        """
        if params is None:
            params = {}
        params.update({'cmd': 'balances',
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.request('post', **params)

    def get_deposit_address(self, params=None):
        """Get address for personal deposit use
           https://www.coinpayments.net/apidoc-get-deposit-address
        """
        if params is None:
            params = {}
        params.update({'cmd': 'get_deposit_address',
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.request('post', **params)

    def get_callback_address(self, params=None):
        """Get a callback address to receive info about address status
           https://www.coinpayments.net/apidoc-get-callback-address 
        """
        if params is None:
            params = {}
        params.update({'cmd': 'get_callback_address',
                       'ipn_url': self.ipn_url,
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.request('post', **params)

    def create_transfer(self, params=None):
        """Not really sure why this function exists to be honest, it transfers
            coins from your addresses to another account on coinpayments using
            merchant ID
           https://www.coinpayments.net/apidoc-create-transfer
        """
        if params is None:
            params = {}
        params.update({'cmd': 'create_transfer',
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.request('post', **params)

    def create_withdrawal(self, params=None):
        """Withdraw or masswithdraw(NOT RECOMMENDED) coins to a specified address,
        optionally set a IPN when complete.
            https://www.coinpayments.net/apidoc-create-withdrawal
        """
        if params is None:
            params = {}
        params.update({'cmd': 'create_withdrawal',
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.request('post', **params)

    def convert_coins(self, params=None):
        """Convert your balances from one currency to another
            https://www.coinpayments.net/apidoc-convert 
        """
        if params is None:
            params = {}
        params.update({'cmd': 'convert',
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.request('post', **params)

    def get_withdrawal_history(self, params=None):
        """Get list of recent withdrawals (1-100max)
            https://www.coinpayments.net/apidoc-get-withdrawal-history 
        """
        if params is None:
            params = {}
        params.update({'cmd': 'get_withdrawal_history',
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.request('post', **params)

    def get_withdrawal_info(self, params=None):
        """Get information about a specific withdrawal based on withdrawal ID
            https://www.coinpayments.net/apidoc-get-withdrawal-info
        """
        if params is None:
            params = {}
        params.update({'cmd': 'get_withdrawal_info',
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.request('post', **params)

    def get_conversion_info(self, params=None):
        """Get information about a specific withdrawal based on withdrawal ID
            https://www.coinpayments.net/apidoc-get-conversion-info
        """
        if params is None:
            params = {}
        params.update({'cmd': 'get_conversion_info',
                       'key': self.public_key,
                       'version': self.version,
                       'format': self.format})
        return self.request('post', **params)

    @staticmethod
    def validate_mac(uuid, price, currency, test_hash):
        to_check = API_KEY + '_' + uuid + '_' + str(int(price * 100)) + currency
        computed_hash = hashlib.sha256(to_check).hexdigest()
        return computed_hash == test_hash
