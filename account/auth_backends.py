from django.core.validators import email_re
from django.db.models import Q

from django.contrib.auth.backends import ModelBackend

from account.compat import User
from account.models import EmailAddress


class UsernameAuthenticationBackend(ModelBackend):
    
    def authenticate(self, **credentials):
        try:
            user = User.objects.get(username__iexact=credentials["username"])
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(credentials["password"]):
                return user


class EmailAuthenticationBackend(ModelBackend):
    
    def authenticate(self, **credentials):
        qs = EmailAddress.objects.filter(Q(primary=True) | Q(verified=True))
        try:
            email_address = qs.get(email__iexact=credentials["username"])
        except EmailAddress.DoesNotExist:
            return None
        else:
            user = email_address.user
            if user.check_password(credentials["password"]):
                return user

class HybridAuthenticationBackend(ModelBackend):
    """User can login via email OR username"""
    def authenticate(self, **credentials):
        if email_re.search(credentials["username"]):
            qs = EmailAddress.objects.filter(Q(primary=True) | Q(verified=True))
            try: email_address = qs.get(email__iexact=credentials["username"])
            except EmailAddress.DoesNotExist: return None
            else: user = email_address.user
        else:
            try: user = User.objects.get(username__iexact=credentials["username"])
            except User.DoesNotExist: return None
        if user.check_password(credentials["password"]):
            return user
