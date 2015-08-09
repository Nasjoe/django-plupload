# -*- coding: utf-8 -*-
from django.template import Library
from plupload.settings import STATIC_URL, JQUERY_URL, JQUERY_UI_URL, JQUERY_UI_CSS_URL

register = Library()


@register.inclusion_tag('plupload/plupload_head_init.html', takes_context=True)
def plupload_head_init(context):
    """
    To be added to your template's head section, as {% plupload_head_init %}, it initializes the js needed for plupload
    to work
    """
    return {
        'STATIC_URL': STATIC_URL,
        'jquery_url': JQUERY_URL,
        'jquery_ui_url': JQUERY_UI_URL,
        'jquery_ui_css_url': JQUERY_UI_CSS_URL,
    }
