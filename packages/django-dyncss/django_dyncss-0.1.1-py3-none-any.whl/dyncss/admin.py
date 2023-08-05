from django.contrib import admin
from django.contrib.admin.options import csrf_protect_m
from django.contrib.admin.utils import unquote
from django.db import models, transaction, router
from django.forms import Textarea
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.clickjacking import xframe_options_exempt

from dyncss.models import File, Version


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = (
        'filename',
        'last_modified_date',
    )

    fields = ('filename', 'content', 'serve_minified', 'comment',)
    readonly_fields = ('user', 'last_modified_date',)

    def get_fields(self, request, obj=None):
        if obj:
            return self.fields + ('user', 'last_modified_date',)
        return self.fields

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('filename',)
        return self.readonly_fields

    change_form_template = 'admin/file/change_form.html'
    text_area_attrs = {
        'rows': 20,
    }

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs=text_area_attrs)}
    }


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):

    actions = None

    list_display = (
        'created_date',
        'comment',
    )

    fields = ('filename', 'content', 'serve_minified', 'user', 'comment', 'created_date',)
    readonly_fields = ('filename', 'user', 'created_date',)
    actions_on_top = False
    change_form_template = 'admin/version/change_form.html'

    @staticmethod
    def filename(obj):
        return obj.file.filename


    def has_module_permission(self, request):
        return False

    @xframe_options_exempt
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': _("List of versions")}

        file_id = request.GET.get("file__exact")
        if file_id:
            try:
                file = File.objects.get(pk=file_id)
                extra_context = {'title': _("List of versions for %(filename)s") % {'filename': file.filename}}
            except File.DoesNotExist:
                file = None
        return super().changelist_view(
            request, extra_context=extra_context,
        )

    @csrf_protect_m
    def changeform_view(self, request, object_id=None, form_url='', extra_content=None):

        opts = self.model._meta

        if request.method == 'POST' and '_save_as_current' in request.POST:
            comment = request.POST.get('comment', '')
            content = request.POST.get('content', '')
            self.save_as_current(request, object_id, content, comment)
            obj = self.get_object(request, unquote(object_id))
            file_pk = obj.file.pk
            redirect_path = reverse('admin:%s_%s_change' % (self.opts.app_label, 'file'), args=(file_pk,),
                                    current_app=opts.app_label)

            return HttpResponseRedirect(redirect_path)

        extra_context = {
            'title': opts.verbose_name,
        }

        return admin.ModelAdmin.changeform_view(
            self,
            request,
            object_id=object_id,
            form_url=form_url,
            extra_context=extra_context,
        )

    def save_as_current(self, request, object_id, content, comment):
        with transaction.atomic(using=router.db_for_write(self.model)):
            obj = self.get_object(request, unquote(object_id))
            file = obj.file
            file.content = content
            file.comment = comment
            file.user = request.user
            file.save()
