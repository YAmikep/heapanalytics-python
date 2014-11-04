# coding=utf-8
from __future__ import unicode_literals, absolute_import

"""
Consumers to send the data to Heap Analytics.

To write your own consumer, all you need to do is to implement a send method.

Example of advanced consumers that could be developped:
 - batch sending if Heap supports it one day
 - asynchronous sending

"""

# Python
import platform
import requests

# Local
from .version import __version__
from .exceptions import HeapAnalyticsException
from .logger import logger


class Consumer(object):
    """
    This simple consumer sends an HTTP request directly to Heap Analytics, with one request for every call.
    This is the default consumer for Heap Analytics objects.

    """

    _default_endpoints = {
        'track': 'https://heapanalytics.com/api/track',
        'identify': 'https://heapanalytics.com/api/identify',
    }
    _default_headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'heap-analytics-python/{} (Python {})'.format(__version__, platform.python_version()),
    }

    def __init__(self, track_url=None, identify_url=None):
        self._endpoints = {
            'track': track_url or self._default_endpoints['track'],
            'identify': identify_url or self._default_endpoints['identify'],
        }

    def send(self, endpoint, json_data):
        """
        Send the data to Heap Analytics.
        Will raise an exception if the endpoint doesn't exist, if the server is unreachable or for some reason can't process the data.

        endpoint: one of 'track' or 'identify', the Heap Analytics endpoint for sending the data
        json_data: the json content to send to the endpoint.

        """
        logger.debug('Endpoint: {} - JSON data: {}'.format(endpoint, json_data))

        if endpoint in self._endpoints:
            url = self._endpoints[endpoint]
            headers = self._default_headers

            try:
                requests.post(url, data=json_data, headers=headers)
            except Exception as e:
                raise HeapAnalyticsException(e)
        else:
            raise HeapAnalyticsException('This endpoint is unknown: "{0}". Valid endpoints are one of {1}'.format(endpoint, self._endpoints.keys()))
