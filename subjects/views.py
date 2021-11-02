import json
import humps
from django.db import connection
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# ========== Importación de decoradores (middlewares) ==========
from todo.decorators import access_token_validation

# ========== Importación de modelos ==========
from .models import Subject, UserSubject

# ========== Importación de funciones útiles ==========
from todo.utils import cursor_to_dict

# Enrutador para las distintas funciones según el método entregado
@require_http_methods(['GET', 'POST', 'PUT', 'DELETE'])
@csrf_exempt
@access_token_validation
def multiple_subjects_router(request, *args, **kwargs):
    if request.method == 'GET':
        return get_user_subject_list(request, *args, **kwargs)
    
    if request.method == 'POST':
        return post_new_subject(request, *args, **kwargs)

# Método para obtener la lista de asignaturas asociadas a un usuario
@require_http_methods(['GET'])
def get_user_subject_list(request, *args, **kwargs):
    try:
        user_id = kwargs['user_id']
        # Se obtiene la lista de asignaturas asociadas al usuario
        query = """
            SELECT Subject.* FROM Subject, UserSubject
                WHERE Subject.id = UserSubject.subject_id
                    AND UserSubject.user_id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [user_id])
            data = cursor_to_dict(cursor)

            if len(data) == 0:
                # No se han encontrado asignaturas asociadas
                return JsonResponse(humps.camelize({
                    'subject_list': data
                }), status=404)

        return JsonResponse(humps.camelize({
            'subject_list': data
        }), status = 200)

    except Exception as error:
        print(error)
        return JsonResponse({
            'message': 'Se ha producido un error interno al obtener las asignaturas.'
        }, status=500)

# Método para registrar una nueva asignatura
@require_http_methods(['POST'])
def post_new_subject(request, *args, **kwargs):
    try:
        user_id = kwargs['user_id']
        form_data = humps.camelize(json.loads(request.body))

        new_subject = Subject(
            name = form_data['name'],
            color = form_data['color']
        )

        new_subject.save()

        # Se almacena la relación entre la asignatura registrada y el usuario actual
        UserSubject(
            user_id = user_id,
            subject_id = new_subject.id
        ).save()

        # Se registra la nueva asignatura y se asocia al usuario actual
        return JsonResponse(humps.camelize({
            'message': '¡Todo okey! Asignatura registrada correctamente.'
        }), status=201)

    except Exception as error:
        print(error)

        return JsonResponse({
            'message': 'Se ha producido un error interno al registrar la asignatura.'
        }, status=500)
