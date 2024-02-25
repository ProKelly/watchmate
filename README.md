# watchmate
watchmate is a website that acts a portal for movie sales, django and django Rest Framework (DRF) are used to implement the backend and build the API's.

**How To Use watchmate**

**step 1:** install django by running *pip install django* on your command line interface 
**step 2:** install django rest framework by running *pip install rest_framework* on your command line interface

**User Authenticaation with DJango Rest**
- I used Token authentication, so the programe is configured to use token authentication but others options such as
  Json Web Token (JWT) authentication are still applicable by just configuring the *settings.py* to reflect the change
  **How**
  change the REST_FRAMEWORK dictionary to reflect the changes:
      REST_FRAMEWORK = {
            'DEFAULT_AUTHENTICATION_CLASSES' : [
                  'rest_framework.authentication.TokenAuthentication',
                   #'rest_framework.authentication.BasicAuthentication',
                   #'rest_framework_simplejwt.authentication.JWTAuthentication',
              ]
      }
  ensure to import the right modules and classes to utilize this authentication technique effectively such as
  *from rest_framework.authtoken.models import Token* and also endeavor to include the default code in the
  models.py file
  
            "from django.conf import settings
            from django.db.models.signals import post_save
            from django.dispatch import receiver
            from rest_framework.authtoken.models import Token
            
            @receiver(post_save, sender=settings.AUTH_USER_MODEL)
            def create_auth_token(sender, instance=None, created=False, **kwargs):
                if created:
                    Token.objects.create(user=instance)"
  **import the models in the views inoder for it to be executed any time the views are being executed.

  **Views**

  i implemented both function based views and class based views utilizing generic classes and also making use of
  viewsets, ModelViewsets, and routers in DRF and for the function based views, i utilized many decorators.

  **Throttling**

  I also implemented UserRate throttling, AnonRateThrottling and ScopeRateThrottling to control request to the api      by users.

  **Serializers**

  i made use of ModelSerializers, since they are easier to use and added alot of validators.

