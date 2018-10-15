import time
import collections
import random
import math
import requests
import string
import json

'''
SEE README FOR INSTRUCTIONS ON FUNCTIONALITY
GALLERY MODULE CREATED BY: DAVID PRYOR, NICK SIMMONS, AND RITU GOWLIKAR
'''

class Gallery(object):
    def __init__(self, apiLocation, apiKey, apiSecret):
        self.apiLocation = apiLocation
        self.apiKey = apiKey
        self.apiSecret = apiSecret

    def buildOauthParams(self):
        return {'oauth_consumer_key': self.apiKey,
                'oauth_nonce': self.generate_nonce(5),
                'oauth_signature_method': 'HMAC-SHA1',
                'oauth_timestamp': str(int(math.floor(time.time()))),
                'oauth_version': '1.0'}

    '''Finds workflows in a subscription'''

    def subscription(self):
        method = 'GET'
        url = self.apiLocation + '/workflows/subscription/'
        params = self.buildOauthParams()
        signature = self.generateSignature(method, url, params)
        params.update({'oauth_signature': signature})
        output = requests.get(url, params=params)
        return output.text


    '''Returns the questions for the given Alteryx Analytics App'''

    def questions(self, appId):
        method = 'GET'
        url = self.apiLocation + '/workflows/' + appId + '/questions/'
        params = self.buildOauthParams()
        signature = self.generateSignature(method, url, params)
        params.update({'oauth_signature': signature})
        output = requests.get(url, params=params)
        return output, output.content

    '''Queue an app execution job. Returns ID of the job'''

    def executeWorkflow(self, appId, *kwpos, **kwargs):
        if('payload' in kwargs):
            print('Payload included: %s' % kwargs['payload'])
            data = kwargs['payload']
            method = 'POST'
            url = self.apiLocation + '/workflows/' + appId + '/jobs/'
            params = self.buildOauthParams()
            signature = self.generateSignature(method, url, params)
            params.update({'oauth_signature': signature})
            output = requests.post(url, json=data, headers={'Content-Type':'application/json'}, params=params)
        else:
            print('No Payload included')
            method = 'POST'
            url = self.apiLocation + '/workflows/' + appId + '/jobs/'
            params = self.buildOauthParams()
            signature = self.generateSignature(method, url, params)
            params.update({'oauth_signature': signature})
            output = requests.post(url, params=params)
            
        return output,output.content


    '''Returns the jobs for the given Alteryx Analytics App'''

    def getJobs(self, appId):
        method = 'GET'
        url = self.apiLocation + '/workflows/' + appId + '/jobs/'
        params = self.buildOauthParams()
        signature = self.generateSignature(method, url, params)
        params.update({'oauth_signature': signature})
        output = requests.get(url, params=params)
        return output, output.content

    '''Retrieves the job and its current state'''

    def getJobStatus(self, jobId):
        method = 'GET'
        url = self.apiLocation + '/jobs/' + jobId + '/'
        params = self.buildOauthParams()
        signature = self.generateSignature(method, url, params)
        params.update({'oauth_signature': signature})
        output = requests.get(url, params=params)
        return output, output.content

    '''Returns the output for a given job (FileURL)'''

    def getJobOutput(self, jobID, outputID):
        method = 'GET'
        url = '/jobs/' + jobID + '/output/' + '/outputID/'
        params = self.buildOauthParams()
        signature = self.generateSignature(method, url, params)
        params.update({'oauth_signature': signature})
        output = requests.get(url, params=params)
        return output, output.content

    '''Returns the App that was requested'''

    def getApp(self, appId):
        method = 'GET'
        url = self.apiLocation + '/' + appId + '/package/'
        params = self.buildOauthParams()
        signature = self.generateSignature(method, url, params)
        params.update({'oauth_signature': signature})
        output = requests.get(url, params=params)
        return output, output.content

    '''Generate pseudorandom number'''

    def generate_nonce(self, length=5):
        return ''.join([str(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)) for i in
                        range(length)])

    def generateSignature(self, httpMethod, url, params):
        import urllib
        import hmac
        import binascii
        import hashlib
        from requests.utils import quote

        """returns HMAC-SHA1 sign"""

        q = lambda x: quote(x, safe="~")
        sorted_params = collections.OrderedDict(sorted(params.items()))
        normalized_params = urllib.urlencode(sorted_params)
        base_string = "&".join((httpMethod.upper(), q(url), q(normalized_params)))
        sig = hmac.new("&".join([self.apiSecret, '']), base_string, hashlib.sha1)
        return sig.digest().encode("base64").rstrip('\n')
