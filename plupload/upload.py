# -*- coding: utf-8 -*-
from django.template import RequestContext
from plupload.settings import MEDIA_ROOT, MEDIA_URL, THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT
from plupload.models import PluploadControlCode
from plupload.forms import PluploadForm
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _
import tempfile
import os
import shutil
import json


def do_upload(request):
    """
    This function is called once for each chunk the file is divided into. It uploads the file, chunk by chunk to a
    temp file, then copies it to its final position. It doesn't resize the image, that's done by plupload client-side
    """
    resp = {
        "jsonrpc": "2.0",
        "result": {
            "filename": "",
            "msg": "",
            "error": "",
        },
        "id": "id",
    }
    if request.method == 'POST':
        form = PluploadForm(request.POST, request.FILES)
        if form.is_valid():
            show_thumbnail = request.POST.get('show_thumbnail', None)  # from widget.html > multipart_params
            upload_chmod = request.POST.get('upload_chmod', None)  # from widget.html > multipart_params
            uploaded_file = request.FILES.get('file')
            if uploaded_file:
                chunk = request.REQUEST.get('chunk', '0')
                chunks = request.REQUEST.get('chunks', '0')
                filename = request.REQUEST.get('name', '')
                plupload_tmp = request.session.get('plupload_tmp')
                # checking control code
                code = request.POST.get('control_code')
                if code:
                    try:
                        control_code = PluploadControlCode.objects.get(code=code)
                    except PluploadControlCode.DoesNotExist:
                        resp['result']['error'] = _(u"No files uploaded: wrong control code")
                        # this goes to pluploader_init.html -> init, FileUploaded
                        return HttpResponse(json.dumps(resp), content_type='application/json; charset=UTF-8')
                else:
                    resp['result']['error'] = _(u"No files uploaded: no control code provided")
                    # this goes to pluploader_init.html -> init, FileUploaded
                    return HttpResponse(json.dumps(resp), content_type='application/json; charset=UTF-8')
                upload_path = os.path.join(MEDIA_ROOT, control_code.upload_to)
                upload_url = os.path.join(MEDIA_URL, control_code.upload_to)
                if not filename:
                    filename = uploaded_file.name
                f = None
                if chunk == '0':
                    # uploading first chunk of the file, creating a temporary file to host it
                    try:
                        f = tempfile.NamedTemporaryFile(mode='wb+', delete=False)  # delete parameter on python >= 2.6
                        plupload_tmp = request.session['plupload_tmp'] = f.name
                    except TypeError:
                        # python <= 2.5
                        # f = tempfile.NamedTemporaryFile(mode = 'wb+')  # deleted as soon as it is closed, python < 2.6
                        try:
                            fd, fpath = tempfile.mkstemp(prefix=filename + '.')  # fd = int
                            os.chmod(fpath, 640)
                            os.close(fd)
                            plupload_tmp = request.session['plupload_tmp'] = fpath
                            f = open(plupload_tmp, 'ab+')
                        except Exception, err:
                            resp['result']['error'] = _(u"Server error, creating temporary file: %s") % err
                            return HttpResponse(json.dumps(resp), content_type='application/json; charset=UTF-8')
                    except Exception, err:
                        resp['result']['error'] = _(u"Server error, creating temporary file: %s") % err
                        return HttpResponse(json.dumps(resp), content_type='application/json; charset=UTF-8')
                elif plupload_tmp:
                    # uploading other chunks
                    try:
                        f = open(plupload_tmp, 'ab+')
                    except IOError:
                        resp['result']['error'] = _(u"Unable to (re)open temporary file for upload, chunk %s") % chunk
                        return HttpResponse(json.dumps(resp), content_type='application/json; charset=UTF-8')
                if f:
                    # writing the chunk to the temporary file
                    for content in uploaded_file.chunks():
                        try:
                            f.write(content)
                        except IOError:
                            resp['result']['error'] = _(u"Unable to write to temporary file, chunk %s") % chunk
                            return HttpResponse(json.dumps(resp), content_type='application/json; charset=UTF-8')
                    f.close()
                if int(chunk) + 1 >= int(chunks):
                    # upload done, all chunks uploaded, copying to final position, removing temp file
                    if plupload_tmp:
                        request.session.pop('plupload_tmp')
                        dest_path = os.path.join(upload_path, filename)
                        try:
                            shutil.copy(plupload_tmp, dest_path)
                        except IOError:
                            resp['result']['error'] = _(u"Unable to copy temporary file to its final position")
                            return HttpResponse(json.dumps(resp), content_type='application/json; charset=UTF-8')
                        except Exception, err:
                            resp['result']['error'] = _(
                                u"Server error, unable to copy temporary file to its final destination: %s"
                            ) % err
                            return HttpResponse(json.dumps(resp), content_type='application/json; charset=UTF-8')
                        if upload_chmod:
                            # attempting chmod
                            try:
                                os.chmod(dest_path, int(upload_chmod, 8))  # converting upload_chmod to octal number
                            except Exception, err:
                                resp['result']['error'] = _(
                                    u"Server error, unable to change permissions to uploadded file: %s"
                                ) % err
                                return HttpResponse(json.dumps(resp), content_type='application/json; charset=UTF-8')
                        try:
                            os.remove(plupload_tmp)
                        except Exception, err:
                            resp['result']['error'] = _(u"Server error, unable to remove temporary file: %s") % err
                            return HttpResponse(json.dumps(resp), content_type='application/json; charset=UTF-8')
                    control_code.upload_done = True
                    control_code.save()
                if show_thumbnail:
                    # showing a thumbnail of the uploaded file in the message (obviously works just with images)
                    wh = ''
                    if THUMBNAIL_WIDTH or THUMBNAIL_HEIGHT:
                        wh = ' style=\"'
                        if THUMBNAIL_WIDTH:
                            wh += 'width:%spx;' % THUMBNAIL_WIDTH
                        if THUMBNAIL_HEIGHT:
                            wh += 'height:%spx;' % THUMBNAIL_HEIGHT
                        wh += '\"'
                    current_file_html = '<a href=\"%s\" target=\"_blank\"><img src=\"%s\" alt=\"%s\"%s/></a>' % (
                        os.path.join(upload_url, filename), os.path.join(upload_url, filename), filename, wh)
                else:
                    # showing an anchor with the filename
                    current_file_html = '<a href=\"%s\" target=\"_blank\">%s</a>' % (
                        os.path.join(upload_url, filename), filename)
                resp['result']['filename'] = filename
                resp['result']['msg'] = _(u"Done. File uploaded: %s") % current_file_html

                response = HttpResponse(json.dumps(resp), content_type='application/json; charset=UTF-8')
                response['Expires'] = 'Mon, 1 Jan 2000 01:00:00 GMT'
                response['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
                response['Pragma'] = 'no-cache'
                return response
            else:
                resp['result']['error'] = _(u"Uploaded file missing.")
                return response
        else:
            # invalid form
            pass
    else:
        form = PluploadForm()
    return render_to_response('plupload/form.html', {'form': form}, context_instance=RequestContext(request))
