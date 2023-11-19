import json

# MB: si se envía el JSON en lugar de Formdata se convierte en este middleware.
class ContentTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Procesar la solicitud antes de pasarla a la vista

        # Obtener el tipo de contenido de la solicitud
        content_type = request.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            # Para JSON
            data = json.loads(request.body)
            request.POST = data

        # Continuar con el flujo normal de la solicitud
        response = self.get_response(request)

        # Procesar la respuesta después de pasar por la vista

        return response