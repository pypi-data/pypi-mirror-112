from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DynCSSConfig(AppConfig):
    name = 'dyncss'
    verbose_name = _("Django DynCSS")
