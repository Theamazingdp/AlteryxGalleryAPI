"""
SEE README FOR INSTRUCTIONS ON FUNCTIONALITY
GALLERY MODULE CREATED BY: DAVID PRYOR, NICK SIMMONS, AND RITU GOWLIKAR
"""

import time
import collections
import random
import math
import requests
import string
import urllib
import hmac
import hashlib
from requests.utils import quote


class Gallery(object):
    def __init__(self, api_location, api_key, api_secret):
        self.api_location = api_location
        self.api_key = api_key
        self.api_secret = api_secret

    def build_oauth_params(self):
        return {
            "oauth_consumer_key": self.api_key,
            "oauth_nonce": Gallery.generate_nonce(5),
            "oauth_signature_method": "HMAC-SHA1",
            "oauth_timestamp": str(int(math.floor(time.time()))),
            "oauth_version": "1.0",
        }

    def subscription(self):
        """
        Finds workflows in a subscription
        :return:
        """

        method = "GET"
        url = self.api_location + "/workflows/subscription/"
        params = self.build_oauth_params()
        signature = self.generate_signature(method, url, params)
        params.update({"oauth_signature": signature})
        output = requests.get(url, params=params)
        return output.text

    def questions(self, app_id):
        """
        Returns the questions for the given Alteryx Analytics App
        :param app_id:
        :return:
        """
        method = "GET"
        url = self.api_location + "/workflows/" + app_id + "/questions/"
        params = self.build_oauth_params()
        signature = self.generate_signature(method, url, params)
        params.update({"oauth_signature": signature})
        output = requests.get(url, params=params)
        return output, output.content

    def execute_workflow(self, app_id, **kwargs):
        """
        Queue an app execution job. Returns ID of the job
        :param app_id:
        :param kwargs:
        :return:
        """
        if "payload" in kwargs:
            print("Payload included: %s" % kwargs["payload"])
            data = kwargs["payload"]
            method = "POST"
            url = self.api_location + "/workflows/" + app_id + "/jobs/"
            params = self.build_oauth_params()
            signature = self.generate_signature(method, url, params)
            params.update({"oauth_signature": signature})
            output = requests.post(
                url, json=data, headers={"Content-Type": "application/json"}, params=params
            )
        else:
            print("No Payload included")
            method = "POST"
            url = self.api_location + "/workflows/" + app_id + "/jobs/"
            params = self.build_oauth_params()
            signature = self.generate_signature(method, url, params)
            params.update({"oauth_signature": signature})
            output = requests.post(url, params=params)

        return output, output.content

    def get_jobs(self, app_id):
        """
        Returns the jobs for the given Alteryx Analytics App
        :param app_id:
        :return:
        """
        method = "GET"
        url = self.api_location + "/workflows/" + app_id + "/jobs/"
        params = self.build_oauth_params()
        signature = self.generate_signature(method, url, params)
        params.update({"oauth_signature": signature})
        output = requests.get(url, params=params)
        return output, output.content

    def get_job_status(self, job_id):
        """
        Retrieves the job and its current state
        :param job_id:
        :return:
        """
        method = "GET"
        url = self.api_location + "/jobs/" + job_id + "/"
        params = self.build_oauth_params()
        signature = self.generate_signature(method, url, params)
        params.update({"oauth_signature": signature})
        output = requests.get(url, params=params)
        return output, output.content

    def get_job_output(self, job_id, output_id):
        """
        Returns the output for a given job (FileURL)
        :param job_id:
        :param output_id:
        :return:
        """
        method = "GET"
        url = "/jobs/" + job_id + "/output/" + "/outputID/"
        params = self.build_oauth_params()
        signature = self.generate_signature(method, url, params)
        params.update({"oauth_signature": signature})
        output = requests.get(url, params=params)
        return output, output.content

    def get_app(self, app_id):
        """
        Returns the App that was requested
        :param app_id:
        :return:
        """
        method = "GET"
        url = self.api_location + "/" + app_id + "/package/"
        params = self.build_oauth_params()
        signature = self.generate_signature(method, url, params)
        params.update({"oauth_signature": signature})
        output = requests.get(url, params=params)
        return output, output.content

    @staticmethod
    def generate_nonce(length=5):
        """
        Generate pseudorandom number
        :param length:
        :return:
        """
        return "".join(
            [
                str(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase))
                for _ in range(length)
            ]
        )

    def generate_signature(self, http_method, url, params):
        """
        returns HMAC-SHA1 sign
        :param http_method:
        :param url:
        :param params:
        :return:
        """

        q = lambda x: quote(x, safe="~")
        sorted_params = collections.OrderedDict(sorted(params.items()))
        normalized_params = urllib.urlencode(sorted_params)
        base_string = "&".join((http_method.upper(), q(url), q(normalized_params)))
        sig = hmac.new("&".join([self.api_secret, ""]), base_string, hashlib.sha1)
        return sig.digest().encode("base64").rstrip("\n")
