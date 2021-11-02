import os
import jwt
import json
import humps
import bcrypt
from datetime import datetime, timedelta, timezone
from json.encoder import JSONEncoder
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# ========== Importación de decoradores (middlewares) ==========
from todo.decorators import access_token_validation

# ========== Importación de modelos ==========
from .models import User

@require_http_methods(['POST'])
@csrf_exempt
def post_session_authentication(request, *args, **kwargs):
    try:
        form_data = humps.camelize(json.loads(request.body.decode('UTF-8')))

        # Se verifica si el usuario existe en la base de datos
        registered_users = User.objects.filter(email = form_data['email'])
        registered_users = list(registered_users.values())

        if len(registered_users) == 0:
            # No hay un usuario registrado bajo el email ingresado
            return JsonResponse({
                'message': 'Las credenciales ingresadas no son válidas. Revisa e inténtalo nuevamente.'
            }, status = 401)
            
        # Se verifica que la contraseña coincida con la ingresada en el formulario
        database_user = registered_users[0]
            
        if not bcrypt.checkpw(form_data['password'].encode('UTF-8'), database_user['password'].encode('UTF-8')):
            # El correo electrónico ingresado es válido, pero no se ha entregado la contraseña correcta
            return JsonResponse({
                'message': 'Las credenciales ingresadas no son válidas. Revisa e inténtalo nuevamente.'
            }, status = 401)
            
        # El usuario y contraseña que se han ingresado son válidos. Se generan los tokens de autenticación.
        access_token = jwt.encode({
            'user_id': database_user['id'],
            'iat': datetime.now(tz=timezone.utc),
            'exp': datetime.now(tz=timezone.utc) + timedelta(minutes=60)
        }, os.environ.get('TODO_SECRET_KEY'), algorithm = 'HS256')

        return JsonResponse(humps.camelize({
            'access_token': access_token,
            'user_id': database_user['id'],
            'fullname': database_user['fullname'],
            'email': database_user['email']
        }), status=200)
            
    except Exception as error:
        print(error)
        
        return JsonResponse({
            'message': 'Se ha producido un error interno. ¡Por favor inténtalo más tarde!'
        }, status=500)


@require_http_methods(['GET'])
@access_token_validation
def get_user_data(request, *args, **kwargs):
    try:
        user_id = kwargs['user_id']
        user_data = list(User.objects.filter(id=user_id).values())
        
        if len(user_data) == 0:
            # El usuario no existe
            return JsonResponse({
                'message': 'Recurso no encontrado.'
            }, status=404)
        
        user_data = user_data[0]

        # Se retornan los datos del usuario
        del user_data['password']

        return JsonResponse(user_data, status=200)

    except Exception as error:
        print(error)

        return JsonResponse({
            'message': 'Se ha producido un error interno. ¡Por favor inténtalo más tarde!'
        }, status=500)
