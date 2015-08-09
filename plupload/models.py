# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from plupload.settings import (UPLOAD_TO, MEDIA_ROOT, EXTENSIONS, MAX_FILE_SIZE, UNIQUE_NAMES, UPLOAD_CHMOD,
                               SHOW_REMOVE, SHOW_THUMBNAIL)
from plupload.utils import split_resize_to
from plupload.forms import PluploadFormField
from random import choice
from types import StringType, IntType
import os
import datetime
import re


"""
Usage example
-------------

In models:

    from plupload.models import PluploadField

    class MyModel(models.Model):
        image1 = PluploadField("Picture 1", upload_to='my_upload_dir/')
        image2 = PluploadField("Picture 2", upload_to='my_upload_dir/', resize_to='800', resize_quality='90')
        image3 = PluploadField("Picture 3", upload_to='my_upload_dir/', resize_to='640x480', resize_quality='85',
                               extensions=['jpg', 'jpeg', 'png', 'gif', 'tiff'],
                               max_file_size=10, show_remove=False, unique_names=False, upload_chmod='660',
                               show_thumbnail=True)
        # Django >= 1.5:
        image4 = PluploadField("Picture 4", allow_files/allow_folders=True/False, upload_to='my_upload_dir/',
                               resize_to='800', resize_quality='90')
        attachment = PluploadField("Some attachment", upload_to='my_upload_dir/', extensions=['rar', 'zip', 'pdf'])
                                   # no 'resize_to' 'resize_quality' for non image files


In forms:

    from plupload.forms import PluploadFormField

    class MyForm(forms.Form):
        image = PluploadFormField(upload_to='my_upload_dir/')
        file = PluploadFormField(upload_to='my_upload_dir/', extensions=['rar', 'zip', 'pdf'])

"""


class PluploadField(models.FilePathField):
    default_error_messages = {
        'invalid_choice': _(u'''%(value)s is not one of the available choices.
                            The file has not been successfully uploaded or does not exist anymore.'''),
    }

    def __init__(self, verbose_name=None, name=None, path='', match=None, recursive=False, allow_files=True,
                 allow_folders=False, **kwargs):
        self.upload_to = kwargs.pop('upload_to', UPLOAD_TO)
        self.path = os.path.join(MEDIA_ROOT, self.upload_to.lstrip('/'))
        self.resize_width, self.resize_height, self.resize_quality = ('', '', '')  # resizing parameters
        self.resize_to = None
        if 'resize_to' in kwargs.keys():
            self.resize_to = kwargs.pop('resize_to', '')
            self.resize_width, self.resize_height = split_resize_to(self.resize_to)
        if 'resize_quality' in kwargs.keys():
            self.resize_quality = kwargs.pop('resize_quality')
            pattern = re.compile('^0|100|[0-9]{1,2}$')
            assert (
                type(self.resize_quality) is IntType and self.resize_quality >= 0 and self.resize_quality <= 100
                or
                type(self.resize_quality) is StringType and (pattern.match(self.resize_quality) or False)
            ), _("resize_quality must be int or string representing a number between 0 and 100")
            self.resize_quality = int(self.resize_quality)
        self.extensions = kwargs.pop('extensions', EXTENSIONS)  # allowed extensions for this field
        self.max_file_size = kwargs.pop('max_file_size', MAX_FILE_SIZE)  # max allowed file size in Mb
        self.unique_names = kwargs.pop('unique_names', UNIQUE_NAMES)  # change uploaded file name to make it unique
        self.upload_chmod = kwargs.pop('upload_chmod', UPLOAD_CHMOD)  # attempt chmod once file is uploaded
        self.show_remove = kwargs.pop('show_remove', SHOW_REMOVE)  # show the remove checkbox
        self.show_thumbnail = kwargs.pop('show_thumbnail', SHOW_THUMBNAIL)  # shows as thumbnail of the uploaded image
        super(PluploadField, self).__init__(
            verbose_name=verbose_name, name=name, path=path, match=match, recursive=recursive, allow_files=allow_files,
            allow_folders=allow_folders, **kwargs
        )

    def formfield(self, **kwargs):
        """
        This is a fairly standard way to set up some defaults while letting the caller override them.
        """
        defaults = {
            'path': self.path,
            'match': self.match,
            'recursive': self.recursive,
            'allow_files': self.allow_files,  # Django >= 1.5
            'allow_folders': self.allow_folders,  # Django >= 1.5
            'form_class': PluploadFormField,
            'upload_to': self.upload_to,
            'resize_width': self.resize_width,
            'resize_height': self.resize_height,
            'resize_quality': self.resize_quality,
            'extensions': self.extensions,
            'max_file_size': self.max_file_size,
            'unique_names': self.unique_names,
            'upload_chmod': self.upload_chmod,
            'show_remove': self.show_remove,
            'show_thumbnail': self.show_thumbnail,
        }
        defaults.update(kwargs)
        return super(PluploadField, self).formfield(**defaults)


class PluploadControlCode(models.Model):
    upload_to = models.CharField(u"Upload path", max_length=100, blank=True, null=True)
    code = models.CharField(u"Control code", max_length=100)
    upload_done = models.BooleanField(u"Upload done?", default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % (self.code)

    def save(self, *args, **kwargs):
        # removing control codes older that 24 hours
        PluploadControlCode.objects.filter(date__lt=datetime.datetime.now() - datetime.timedelta(days=1)).delete()
        super(PluploadControlCode, self).save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(PluploadControlCode, self).__init__(*args, **kwargs)
        if not self.code:
            self.code = self.generate_control_code()
            while PluploadControlCode.objects.filter(code=self.code):
                self.code = self.generate_control_code()

    def generate_control_code(self):
        # better not using &, it is escaped to &amp;
        return ''.join([
            choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^*(-_=+)') for i in range(100)
        ])

    class Meta:
        pass
