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
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_user_set'
    )

    def get_info(self):
        return {'name': self.first_name, 'email': self.email,
                         'is_superuser': self.is_superuser, 'is_staff': self.is_staff}

class Company(models.Model):
    business_name = models.CharField(max_length=300)
    description = models.CharField(max_length=300,null=True)
    #subscription_plan = models.CharField(max_length=30,default='Basic')