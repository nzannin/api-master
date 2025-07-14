from rest_framework.throttling import UserRateThrottle

class BurstRateThrottle(UserRateThrottle):
    """
    Custom throttle class that allows a burst of requests for authenticated users.
    """
    scope = 'burst'

class SustainedRateThrottle(UserRateThrottle):
    """
    Custom throttle class that allows a sustained rate of requests for authenticated users.
    """
    scope = 'sustained'
     