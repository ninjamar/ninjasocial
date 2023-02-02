from django.http import HttpResponseRedirect

class LocationRestrictMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if (not request.user.is_anonymous) and (not request.user.is_active) and (request.path != "/inactive-user/"):
            return HttpResponseRedirect("/inactive-user/")
        response = self.get_response(request)
        return response