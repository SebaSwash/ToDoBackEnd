from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Modelo para Subject
class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7)

    class Meta:
        db_table = 'Subject'

# Modelo para tabla relacional de User - Subject (asignaturas o tópicos en general asociados a un usuario)
class UserSubject(models.Model):
    user_id = models.IntegerField()
    subject_id = models.IntegerField()

    class Meta:
        db_table = 'UserSubject'

