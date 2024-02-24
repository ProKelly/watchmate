
from rest_framework.throttling import UserRateThrottle

class ReviewCreateThrottle(UserRateThrottle):
    scope = "review-create" #this will be used in the settings.py file to set the throttle rates

class ReviewListThrottle(UserRateThrottle):
    scope = "review-list"