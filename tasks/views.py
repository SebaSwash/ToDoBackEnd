import json
import humps
import datetime
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.utils.timezone import make_aware
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# ========== Importación de decoradores (middlewares) ==========
from todo.decorators import access_token_validation

# ========== Importación de modelos ==========
from .models import Task, UserTask

# ========== Importación de funciones útiles ==========
from todo.utils import cursor_to_dict

# Enrutador de requests a distintas funciones según el método invocado
@require_http_methods(['GET', 'POST', 'PUT', 'DELETE'])
@csrf_exempt
@access_token_validation
def multiple_tasks_router(request, *args, **kwargs):
    if request.method == 'GET':
        return get_user_task_list(request, *args, **kwargs)
    
    if request.method == 'POST':
        return post_new_user_task(request, *args, **kwargs)

# Enrutador de requests a distintas funciones según el método invocado
@require_http_methods(['GET', 'POST', 'PUT', 'DELETE'])
@csrf_exempt
@access_token_validation
def single_tasks_router(request, *args, **kwargs):
    if request.method == 'PUT':
        return update_user_task(request, *args, **kwargs)
    

# Método para obtener la lista de tareas asociadas a un usuairo en particular
@require_http_methods(['GET'])
@access_token_validation
def get_user_task_list(request, *args, **kwargs):
    try:
        user_id = kwargs['user_id']
        query = """
            SELECT Task.*, Subject.name AS subject_name, Subject.color AS subject_color 
                FROM Task, UserTask, Subject
                    WHERE Task.id = UserTask.task_id AND UserTask.user_id = %s
                        AND Task.subject_id = Subject.id
                    
                    ORDER BY Task.deadline ASC
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [user_id])
            task_list = cursor_to_dict(cursor)

        if len(task_list) == 0:
            # No se han encontrado tareas asociadas al usuario
            return JsonResponse(humps.camelize({
                'task_list': task_list
            }), status=404)
        
        today = datetime.datetime.now()
    
        for task in task_list:
            # Se obtiene los días restantes para el deadline de la tarea. (positivos o negativos)
            # y se agregan al objeto de la tarea para mostrarlo en la lista.
            datetime_df = task['deadline'] - today
            task['days_remaining'] = datetime_df.days

        return JsonResponse(humps.camelize({
            'task_list': task_list
        }), status=200)

    except Exception as error:
        print(error)
        return JsonResponse({
            'message': 'Se ha producido un error interno al intentar obtener las tareas.'
        }, status=500)

# Método para registrar una nueva tarea asociada a un usuario en particular
@require_http_methods(['POST'])
@access_token_validation
def post_new_user_task(request, *args, **kwargs):
    try:
        form_data = humps.decamelize(json.loads(request.body))
        user_id = kwargs['user_id']

        # Se genera la nueva tarea y la asociación con el usuario
        new_task = Task(
            subject_id = form_data['subject_id'],
            title = form_data['title'],
            description = form_data['description'],
            deadline = form_data['deadline'],
            is_obligatory = form_data['is_obligatory'],
            notify_at = form_data['notify_at'] if form_data['notify_at'] else None,
            priority = form_data['priority'],
            progress = 0.0
        )
        new_task.save()

        # Se genera la relación entre la nueva tarea y el usuario
        UserTask(
            user_id = user_id,
            task_id = new_task.id
        ).save()

        return JsonResponse({
            'message': '¡A trabajar! La tarea ha sido registrada correctamente.'
        }, status=201)

    except Exception as error:
        return JsonResponse({
            'message': 'Se ha producido un error interno al intentar registrar la nueva tarea.'
        }, status=500)

@require_http_methods(['PUT'])
@access_token_validation
def update_user_task(request, *args, **kwargs):
    try:
        form_data = humps.decamelize(json.loads(request.body))
        user_id = kwargs['user_id']

        # Se verifica que la tarea que se intenta modificar le pertenezca al usuario
        records = UserTask.objects.filter(user_id = user_id, task_id = int(form_data['task_id'])).values()

        if records.count() == 0:
            # El usuario no tiene asociada la tarea que se especificó en la URL
            return JsonResponse({
                'message': 'Se ha producido un error. No se ha encontrado la tarea especificada o no estás asociado a ella.'
            }, status = 404)
        
        # Se obtiene la tarea de la base de datos y se modifican los campos
        task_record = Task.objects.get(id = int(form_data['task_id']))

        task_record.subject_id = form_data['subject_id']
        task_record.title = form_data['title']
        task_record.description = form_data['description']
        task_record.deadline = form_data['deadline']
        task_record.is_obligatory = form_data['is_obligatory']

        if form_data['notify_at'] != '':
            task_record.notify_at = form_data['notify_at']

        task_record.priority = form_data['priority']

        if 'progress' in form_data.keys():
            task_record.progress = form_data['progress']

        task_record.save()

        return JsonResponse({
            'message': '¡Todo okey! La tarea ha sido modificada correctamente.'
        }, status=200)

    except Exception as error:
        print(error)
        return JsonResponse({
            'message': 'Se ha producido un error interno al actualizar la tarea.'
        }, status=500)