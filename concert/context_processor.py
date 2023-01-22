from django.conf import settings

def concert(request):
    return {
        "BASE_URL": settings.BASE_URL,
    }