from django.http import HttpResponse, Http404

from dyncss.models import File


def dyncss(request, filename):
    try:
        obj = File.objects.get(filename=filename)
    except File.DoesNotExist:
        raise Http404("DynCss file does not exist")

    if obj.serve_minified:
        response = obj.minified_content
    else:
        response = obj.content

    return HttpResponse(response, content_type="text/css")
