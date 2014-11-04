heapanalytics-python
====================

A module for using the HeapAnalytics Server-Side API (https://heapanalytics.com/docs/server-side).

The heapanalytics package allows you to easily track events and update user properties from your python application.

## Getting Started

The HeapAnalytics class is the primary class for tracking events and sending user updates.

```python
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
```