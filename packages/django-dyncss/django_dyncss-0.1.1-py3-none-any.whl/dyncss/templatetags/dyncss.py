from django import template
from django.utils.safestring import mark_safe

from dyncss.models import File

register = template.Library()


@register.simple_tag
def dyncss(filename, inline=False):
    if inline == True:
        try:
            tag = "<style>\n"
            obj = File.objects.get(filename=filename)
            if obj.serve_minified:
                tag += obj.minified_content
                tag += "\n</style>"

            else:
                tag += obj.content
                tag += "\n</style>"

        except File.DoesNotExist:
            tag = ''
    else:
        tag = '<link rel="stylesheet" type="text/css" href="{}">'.format(filename)

    return mark_safe(tag)
