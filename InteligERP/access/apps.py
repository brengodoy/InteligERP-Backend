from django.apps import AppConfig

"""
Este archivo se utiliza para configurar y personalizar 
la aplicación Django. Puedes utilizarlo para establecer 
configuraciones específicas de la aplicación, como el nombre 
legible de la aplicación, configuraciones de permisos, rutas 
de URL adicionales, señales, entre otros. También puedes 
realizar acciones específicas cuando la aplicación se carga, 
utilizando los métodos proporcionados por la clase AppConfig.
"""


class AccessConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'access'
