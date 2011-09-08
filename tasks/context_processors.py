def sharejs_url(request):
    from django.conf import settings
    return { 'SHAREJS_URL': settings.SHAREJS_URL }
