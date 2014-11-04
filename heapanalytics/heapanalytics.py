# coding=utf-8
from __future__ import unicode_literals, absolute_import

"""
A module for using the HeapAnalytics Server-Side API (https://heapanalytics.com/docs/server-side)
The heapanalytics package allows you to easily track events and update user properties from your python application.

The HeapAnalytics class is the primary class for tracking events and sending user updates.


from heapanalytics import HeapAnalytics

app_id = "XXXXXXXXXX"
heap = HeapAnalytics(app_id)

# Send an event
heap.track('12345', 'Welcome email sent', {'Email': 'john@example.com'})

# Update user profile
heap.identify(
    '12345',
    {
        'First name': 'John',
        'Last name': 'Smith',
    }
)

"""

# Local
from .utils import json
from .consumer import Consumer


class HeapAnalytics(object):
    """
    Allows to track events and send user updates to Heap Analytics from your python code.
    """

    def __init__(self, app_id, consumer=None):
        """
        Creates a new Heap Analytics object, which can be used for all tracking.

        app_id: the app_id corresponding to one of your projects.
        consumer: (optional) the consumer used to actually send the request. Default: consumer.Consumer

        Using a consumer ensures that the responsibility of actually sending the request is not included in this class and can therefore be changed.
        For example, batch sending if Heap Analytics supports it one day, asynchronous sending, etc.

        """
        self._app_id = app_id
        self._consumer = consumer or Consumer()

    def track(self, identity, event_name, properties=None):
        """
        Tracks an event along with an identity representing the user related to this event.

        identity: an email, handle, or Heap-generated user ID. This identity typically corresponds to an existing user. If no such identity exists, then a new user will be created.
        event_name: the name of the server-side event. Limited to 1024 characters.
        properties: (optional) an object with key-value properties you want associated with the event. Each property must either be a number or string with fewer than 1024 characters.

        # Track that user "12345"'s welcome email was sent
        heap.track("12345", "Welcome email sent")

        # Track with properties
        heap.track("12345", "Welcome email sent", { 'Email': 'john@example.com' })

        """
        properties = properties or {}

        event = {
            'app_id': self._app_id,
            'identity': identity,
            'event': event_name,
            'properties': properties
        }

        self._consumer.send('track', json.dumps(event, separators=(',', ':')))

    def identify(self, identity, properties=None):
        """
        Assign properties to a user.

        identity: an email, handle, or Heap-generated user ID. This identity typically corresponds to an existing user. If no such identity exists, then a new user will be created with that handle. Limited to 1024 characters.
        properties: (optional) an object with key-value properties you want associated with the user. Each property must either be a number or string with fewer than 1024 characters.

        # Update user's properties
        heap.identify(
            "12345",
            {
                "First name": "John",
                "Last name": "Smith"
            }
        )

        """
        properties = properties or {}

        event = {
            'app_id': self._app_id,
            'identity': identity,
            'properties': properties
        }

        self._consumer.send('identify', json.dumps(event, separators=(',', ':')))
