from django.http import HttpResponseRedirect
from django.utils.http import urlencode
from urllib.parse import quote
from django.conf import settings
from socialapp.models import User
import requests
class EmailVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # should only users with an account be allowed to view sitw?
        if not request.user.is_anonymous and not request.user.is_staff:
            if not request.user.is_verified and request.path not in ["/verification/", "/logout/"]: #and (not request.user.is_anonymous): # and (request.path != "/verification/"
                headers = {"Authorization": f"Bearer {settings.AUTH0_TOKEN}"}
                q = f"?q=email%3A%22{quote(request.user.email)}%22&search_engine=v3"
                r = requests.get(f'{settings.AUTH0_BASE_API_URL}/api/v2/users{q}', headers=headers)
                if r.json()[0]["email_verified"]:
                    # verify email
                    user = User.objects.get(email=request.user.email)
                    user.is_verified = True
                    user.save()
                else:
                    return HttpResponseRedirect("/verification/")
        response = self.get_response(request)
        return response