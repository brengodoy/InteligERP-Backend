# InteligERP Backend

## Instrucciones de uso

1. Clonar el repositorio: `git clone https://github.com/brengodoy/InteligERP-Backend.git`
2. Activar entorno virtual `source ./.venv/bin/activate`
3. Instalar requerimientos `pip install -r requirements.txt`
4. Posicionarse en la carpeta del proyecto de Django `cd ./InteligERP`
5. Iniciar proceso `python manage.py runserver`

## Tips

- Para crear usuarios de manera automática correr el comando `python manage.py create_users`.
Los usuarios a crear (posteriormente a la eliminación si correspondiera) se pueden editar en `management/commands/create_users.py`.
Funciona de la misma manera con `python manage.py create_datawarehouses`.