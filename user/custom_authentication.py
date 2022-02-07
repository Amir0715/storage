import email
import json
from user.models import User
from rest_framework import authentication, exceptions
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _

class CustomAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        credentials = json.loads(request.body)
        user = authenticate(request=request, **credentials)

        if user is None:
            raise exceptions.AuthenticationFailed(_('Invalid username/password.'))

        if not user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        
        
        return (user, None)
