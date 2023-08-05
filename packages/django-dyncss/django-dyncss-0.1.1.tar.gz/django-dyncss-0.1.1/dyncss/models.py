import csscompressor
from django.conf import settings
from django.db import models, transaction, router
from django.utils.translation import ugettext_lazy as _


class File(models.Model):

    content = models.TextField(
        null=False,
        verbose_name=_("Content")
    )

    minified_content = models.TextField(
        null=False,
        verbose_name=_("Minified content")
    )

    serve_minified = models.BooleanField(
        null=False,
        default=True,
        verbose_name='Serve a minified version of the content'
    )

    filename = models.CharField(
        max_length=256,
        null=False,
        blank=False,
        unique=True,
        verbose_name=_("Filename"),
        db_index=True
    )

    last_modified_date = models.DateTimeField(auto_now=True)

    comment = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name=_("Comment")
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        editable=False,
        on_delete=models.SET_NULL,
        verbose_name=_("User")

    )

    def save(self, *args, **kwargs):

        self.minified_content = csscompressor.compress(self.content)

        with transaction.atomic(using=router.db_for_write(self)):
            super(File, self).save(*args, **kwargs)

            Version.objects.filter(file=self, state='current').update(state='previous')

            Version.objects.create(
                file=self,
                content=self.content,
                serve_minified=self.serve_minified,
                user=self.user,
                comment=self.comment,
                state='current'
            )

    def __str__(self):
        return self.filename


class Meta:

    verbose_name = _("CSS File")
    app_label = _("Django DynCSS")


class Version(models.Model):

    file = models.ForeignKey(
        to=File,
        null=False,
        on_delete=models.CASCADE,
        verbose_name=_("File")
    )

    content = models.TextField(
        null=False,
        verbose_name=_("Content")
    )

    serve_minified = models.BooleanField(
        null=False,
        default=True,
        verbose_name='Serve a minified version of the content'
    )

    comment = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name=_("Comment")
    )

    created_date = models.DateTimeField(
        auto_now=True,
        db_index=True,
        editable=False,
        verbose_name=_("Created date")
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        editable=False,
        on_delete=models.SET_NULL,
        verbose_name=_("User")
    )

    STATES = (('current', 'current'), ('previous', 'previous'))

    state = models.CharField(
        null=False,
        blank=False,
        max_length=8,
        choices=STATES,
        editable=False,
        verbose_name=_("State")
    )

    def delete(self, *args, **kwargs):
        pass

    class Meta:
        verbose_name = _("Version")

    def __str__(self):
        return "{} ({})".format(self.file.filename, self.created_date)
