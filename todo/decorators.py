import os
import jwt
from django.http.response import JsonResponse
from django.core.exceptions import PermissionDenied

# Función para validar el token de acceso con el identificador de usuario
def access_token_validation(function):
    def wrap(request, *args, **kwargs):
        try:
            # Se realiza la validación del token de acceso
            try:
                access_token = request.headers['Authorization']
            except:
                return JsonResponse({
                    'message': 'Token de acceso no especificado.'
                }, status = 401)

            decoded_token = jwt.decode(access_token, os.environ.get('TODO_SECRET_KEY'), algorithms=['HS256'])

            url_user_id = kwargs['user_id'] # ID de usuario en la url de la request

            # Verificación de autenticidad de usuario según el ID de la URL y el token
            if url_user_id != decoded_token['user_id']:
                # ID de usuario de la URL no coincide con la identidad del token generado
                return JsonResponse({
                    'message': 'Acceso prohibido al recurso.'
                }, status=403) 
        
        except jwt.ExpiredSignatureError:
            return JsonResponse({
                'message': 'Token de acceso expirado.'
            }, status=401)

        except Exception as error:
            return JsonResponse({
                'message': 'Se ha producido un error interno. Por favor inténtalo más tarde.'
            }, status=500)

        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap