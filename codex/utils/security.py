from rest_framework.authentication import SessionAuthentication


class SessionCSRFExemptAuthentication(SessionAuthentication):
    """ Extend session auth and disable CSRF checks """
    def enforce_csrf(self, request):
        pass