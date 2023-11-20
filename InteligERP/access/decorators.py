from rest_framework_simplejwt.tokens import Token, UntypedToken
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication
from functools import wraps
from django.http import HttpResponseForbidden

def obtener_jwt_desde_request(request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        return token
    else:
        return None
    
def token_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            token = obtener_jwt_desde_request(request)
            token_obj = UntypedToken(token, verify=False)
            payload = token_obj.payload
            user_id = payload['user_id']
            return view_func(request, user_id, *args, **kwargs)
        except Exception as e:
            print(f"Error al decodificar el token: {e}")
            return None
    return wrapper