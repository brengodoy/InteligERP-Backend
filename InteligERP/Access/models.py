from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

"""
Este archivo es donde defines los modelos de tu 
aplicación. Los modelos son clases que representan 
las tablas de la base de datos y definen la estructura 
y el comportamiento de los datos almacenados. Aquí 
puedes definir los campos, relaciones, métodos y 
ropiedades de tus modelos. Django utiliza esta 
información para generar y administrar la estructura 
de la base de datos, así como para realizar operaciones 
CRUD (crear, leer, actualizar, eliminar) en los datos.
"""


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_user_set'
    )
