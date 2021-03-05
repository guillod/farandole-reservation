from slots import models

# Hack to get request object in models.request
def RequestExposerMiddleware(get_response):
    def middleware(request):
        models.request = request
        response = get_response(request)
        return response
    return middleware
