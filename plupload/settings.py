# -*- coding: utf-8 -*-
from django.conf import settings
from plupload.utils import split_resize_to

"""
Some settings you might want to include in your project's settings file.

PLUPLOAD_UPLOAD_TO: path relative to MEDIA_ROOT, where files will be uploaded. General setting, you probably want to set
'upload_to' attribute for the PluploadField instead. Default ''

PLUPLOAD_MAX_FILE_SIZE: Mb, maximum allowed file size for upload. General setting, you can also use 'max_file_size'
field attribute. Default None

PLUPLOAD_CHUNK_SIZE: Mb, dimension of each chunk the file is split into during upload, default 1 Mb

PLUPLOAD_UNIQUE_NAMES: if True unique random names will be used for uploaded files; if False the original file name
will be kept, but if a file with the same name exists it will be overwritten without advice. General setting, you can
also use 'unique_names' field attribute. Default True

PLUPLOAD_UPLOAD_CHMOD: tries to change file permissions to the uploaded file, after the file has been uploaded, must be
an integer or a string (if it has leading zeros) representing the permissions; if set i.e. to '640', tries to chmod
uploaded file to 0640 after upload is done. General setting, you can also use 'upload_chmod' field attribute.
Default None

PLUPLOAD_RESIZE_TO: image size, if the uploaded image is larger that this value, a resize will be tried. General
setting, you can also use 'resize_to' field attribute
    allowed formats examples:
    "300" -> width:300 height:300 modifies aspect ratio
    "300x200" -> width:300 height:200 modifies aspect ratio
    "x200" -> width:undefined height:200 keeps aspect ratio
    "300x" -> width:300 height:undefined keeps aspect ratio

PLUPLOAD_RESIZE_QUALITY: image quality, where applies. General setting, you can also use 'unique_names' field attribute.
Default 90

PLUPLOAD_EXTENSIONS: a list of valid file extensions for upload, case insensitive, if you haven't defined an
'extensions' attribute on field definition -> well, plupload extensions ARE case sensitive: but if you write
'jpg' here, 'jpg', 'JPG' and 'Jpg' will be added as valid file extensions.. General setting, you can also use
'extensions' field attribute. Default None = all file extensions allowed

PLUPLOAD_AUTO_START: if True the file is uploaded as soon as it is added to the list of upload, otherwise an 'upload'
button will show. Default True

PLUPLOAD_SHOW_REMOVE: if you want to display the 'remove' checkbox once the file has been uploaded. General setting,
you can also use 'show_remove' field attribute. Default True

PLUPLOAD_SHOW_THUMBNAIL: if you want to display a thumbnail of the uploaded file instead of a filename. Default False

PLUPLOAD_THUMBNAIL_WIDTH: uploaded thumbnail width. Default 80 (px)

PLUPLOAD_THUMBNAIL_HEIGHT: uploaded thumbnail height. Default 80 (px)

PLUPLOAD_JQUERY_URL: set a default jquery version to load in case jquery is not present at the moment plupload is being
loaded. Default "https://ajax.googleapis.com/ajax/libs/jquery/1.10.3/jquery.min.js") # set a default jquery version to
load in case jquery is not present at the moment plupload is being loaded

PLUPLOAD_JQUERY_UI_URL: same as above for jquery-ui.
Default "http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/jquery-ui.min.js")

PLUPLOAD_JQUERY_UI_CSS_URL: same as above for jquery-ui css; indicating a theme here you can change the look of the
plupload js box. Default "http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/themes/smoothness/jquery-ui.min.css")

"""

MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', '')
MEDIA_URL = getattr(settings, 'MEDIA_URL', '')

STATIC_ROOT = getattr(settings, 'STATIC_ROOT', '')
STATIC_URL = getattr(settings, 'STATIC_URL', '')

MAX_FILE_SIZE = getattr(settings, 'PLUPLOAD_MAX_FILE_SIZE', None)  # Mb
CHUNK_SIZE = getattr(settings, 'PLUPLOAD_CHUNK_SIZE', 1)  # Mb
UNIQUE_NAMES = getattr(settings, 'PLUPLOAD_UNIQUE_NAMES', True)
UPLOAD_TO = getattr(settings, 'PLUPLOAD_UPLOAD_TO', '').lstrip('/')  # relative to MEDIA_ROOT
UPLOAD_CHMOD = getattr(settings, 'PLUPLOAD_UPLOAD_CHMOD', None)

RESIZE_TO = getattr(settings, 'PLUPLOAD_RESIZE_TO', '')
RESIZE_WIDTH, RESIZE_HEIGHT = split_resize_to(RESIZE_TO)
RESIZE_QUALITY = getattr(settings, 'PLUPLOAD_RESIZE_QUALITY', 90)  # %

EXTENSIONS = getattr(settings, 'PLUPLOAD_EXTENSIONS', None)

AUTO_START = getattr(settings, 'PLUPLOAD_AUTO_START', True)
SHOW_REMOVE = getattr(settings, 'PLUPLOAD_SHOW_REMOVE', True)
SHOW_THUMBNAIL = getattr(settings, 'PLUPLOAD_SHOW_THUMBNAIL', False)
THUMBNAIL_WIDTH = getattr(settings, 'PLUPLOAD_THUMBNAIL_WIDTH', 80)  # px
THUMBNAIL_HEIGHT = getattr(settings, 'PLUPLOAD_THUMBNAIL_HEIGHT', 80)  # px

# JQUERY URLS
JQUERY_URL = getattr(settings,
                     'PLUPLOAD_JQUERY_URL',
                     "https://ajax.googleapis.com/ajax/libs/jquery/1.10.3/jquery.min.js")
JQUERY_UI_URL = getattr(settings,
                        'PLUPLOAD_JQUERY_UI_URL',
                        "http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/jquery-ui.min.js")
JQUERY_UI_CSS_URL = getattr(settings,
                            'PLUPLOAD_JQUERY_UI_CSS_URL',
                            "http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/themes/smoothness/jquery-ui.min.css")
