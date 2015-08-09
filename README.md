# django-plupload
###A ready-to-use integration of plupload into django

Plupload is a javascript application for handling file uploads (http://www.plupload.com/). I had the need of using a javascript tool to upload files (images in particular), both from the admin and the site itself, doing some resizing before the file got uploaded, so the server won't run out of memory trying to resize Mbytes-large pictures. This is a quick ready-to-go integration of plupload in a django project.
It provides a `PluploadField` for models and a `PluploadFormField` for forms, customizable via settings and attributes.
Plupload files are included, you can replace them with newer versions in case. This application uses just html4 or html5 plupload runtimes (no flash, silverlight or others).


##WHAT DO YOU NEED

- Django 1.3-1.8
- python 2.4 or higher
- jquery
I actually haven't tested it with older versions.


##INSTALLATION

- add `'plupload'` to `INSTALLED_APPS` of your project
- add this to your `urls.py`
```
    urlpatterns += patterns('',
        (r'^plupload/', include('plupload.urls')),
    )
```
- define some django-plupload settings you might need, in your `settings.py` file (you can find a list below)
- add `{% load plupload_tags %}` and `{% plupload_head_init %}` within the `<head></head>` section of your base template, your admin's `base_site.html` template, or wherever the plupload window needs to be loaded. It will include the necessary javascript to run Plupload
- run `manage.py migrate` to create the required tables in your DB and `manage.py collectstatic` to collect static files
- now you can use `PluploadField` with your models, or `PluploadFormField` with your forms


##USAGE

In your models, you can use a `PluploadField`, defining an `upload_to` attribute, like the one used by Django's `FileField` (though it actually subclasses `FilePathField`). You can also define an `extensions` attribute (optional) with a list allowed file extensions. This defaults to the setting `PLUPLOAD_EXTENSIONS` in case it's not indicated. If you are using `PluploadField` to upload images you might want to add `resize_to` and/or `resize_quality` attributes. I.e.
```
    from plupload.models import PluploadField

    class MyModel(models.Model):
        image1 = PluploadField(u"Picture 1", upload_to='my_upload_dir/')
        image2 = PluploadField(u"Picture 2", upload_to='my_upload_dir/', resize_to='800', resize_quality='90')
        image3 = PluploadField(u"Picture 3", upload_to='my_upload_dir/', resize_to='640x480', resize_quality='85', extensions=['jpg', 'jpeg', 'png', 'gif', 'tiff'], max_file_size=10, show_remove=False, unique_names=False, upload_chmod='660', show_thumbnail=True)
        # Django >= 1.5:
        image4 = PluploadField(u"Picture 4", allow_files=True/False, allow_folders=True/False, upload_to='my_upload_dir/', resize_to='800', resize_quality='90')
        attachment = PluploadField(u"Some attachment", upload_to='my_upload_dir/', extensions=['rar', 'zip', 'pdf']) # no 'resize_to' 'resize_quality' for non image files
```

For your forms you can use `PluploadFormField` instead, basically the same way you do with `PluploadField`
```
    from plupload.forms import PluploadFormField

    class MyForm(forms.Form):
        image = PluploadFormField(upload_to='my_upload_dir/')
        file = PluploadFormField(upload_to='my_upload_dir/', extensions=['rar', 'zip', 'pdf'])
```

Attributes you can use with a `PluploadField`, besides conventional django ones. They override general settings below, see SETTINGS for a description:

- upload_to
- max_file_size
- unique_names
- upload_chmod
- extensions
- show_remove

Image-specific attributes, they make sense just with uploaded images, don't use it if you intend to use the field to upload non-image files:

- resize_to
- resize_quality
- show_thumbnail


##SETTINGS

- `PLUPLOAD_UPLOAD_TO`: path relative to MEDIA_ROOT, where files will be uploaded. General setting, you probably want to set 'upload_to' attribute for the PluploadField instead. Default ''
- `PLUPLOAD_MAX_FILE_SIZE`: Mb, maximum allowed file size for upload, accepts an integer or a float. General setting, you can also use 'max_file_size' field attribute. Default None
- `PLUPLOAD_CHUNK_SIZE`: Mb, dimension of each chunk the file is split into during upload, default 1 Mb
- `PLUPLOAD_UNIQUE_NAMES`: if True unique random names will be used for uploaded files; if False the original file name will be kept, but if a file with the same name exists it will be overwritten without advice. General setting, you can also use 'unique_names' field attribute. Default True
- `PLUPLOAD_UPLOAD_CHMOD`: tries to change file permissions to the uploaded file, after the file has been uploaded, must be an integer or a string (if it has leading zeros) representing the permissions; if set i.e. to '640', tries to chmod uploaded file to 0640 after upload is done. General setting, you can also use 'upload_chmod' field attribute. Default None
- `PLUPLOAD_RESIZE_TO`: image size, if the uploaded image is larger that this value, a resize will be tried. General setting, you can also use 'resize_to' field attribute
    allowed formats examples:
    "300" -> width:300 height:300 modifies aspect ratio
    "300x200" -> width:300 height:200 modifies aspect ratio
    "x200" -> width:undefined height:200 keeps aspect ratio
    "300x" -> width:300 height:undefined keeps aspect ratio
- `PLUPLOAD_RESIZE_QUALITY`: image quality, where applies. General setting, you can also use 'unique_names' field attribute. Default 90
- `PLUPLOAD_EXTENSIONS`: a list of valid file extensions for upload, case insensitive, if you haven't defined an 'extensions' attribute on field definition -> well, plupload extensions ARE case sensitive: but if you write 'jpg' here, 'jpg', 'JPG' and 'Jpg' will be added as valid file extensions.. General setting, you can also use 'extensions' field attribute. Default None = all file extensions allowed
- `PLUPLOAD_AUTO_START`: if True the file is uploaded as soon as it is added to the list of upload, otherwise an 'upload' button will show. Default True
- `PLUPLOAD_SHOW_REMOVE`: if you want to display the 'remove' checkbox once the file has been uploaded. General setting, you can also use 'show_remove' field attribute. Default True
- `PLUPLOAD_SHOW_THUMBNAIL`: if you want to display a thumbnail of the uploaded file instead of a filename. Default False
- `PLUPLOAD_THUMBNAIL_WIDTH`: uploaded thumbnail width. Default 80 (px)
- `PLUPLOAD_THUMBNAIL_HEIGHT`: uploaded thumbnail height. Default 80 (px)
- `PLUPLOAD_JQUERY_URL`: set a default jquery version to load in case jquery is not present at the moment plupload is being loaded. Default "https://ajax.googleapis.com/ajax/libs/jquery/1.10.3/jquery.min.js") # set a default jquery version to load in case jquery is not present at the moment plupload is being loaded
- `PLUPLOAD_JQUERY_UI_URL`: same as above for jquery-ui. Default "http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/jquery-ui.min.js")
- `PLUPLOAD_JQUERY_UI_CSS_URL`: same as above for jquery-ui css; indicating a theme here you can change the look of the plupload js box. Default "http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/themes/smoothness/jquery-ui.min.css")
