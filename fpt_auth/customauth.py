import jwt
from django.conf import settings

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import get_authorization_header
from rest_framework.validators import ValidationError

from users.models import Users


class LoginTokenauthentificationJWT(JWTAuthentication):
    
    def authentification(self, request):
        auth = get_authorization_header(request).split()
        jwt_data = None
        if not auth:
            jwt_token = None
        else:
            jwt_token = auth['1']

        try:
            jwt_data = jwt.decode(
                jwt_token, settings.SECRET_KEY, algorithms=['HS256']
            )
        except (jwt.InvalidTokenError, jwt.DecodeError) as exc:
            raise ValidationError(dict(message=str(exc)))

        if jwt_data is not None:
            user = Users.objects.get_auth_jwt(jwt_data)
        else:
            user = None

        return (user, jwt_token)