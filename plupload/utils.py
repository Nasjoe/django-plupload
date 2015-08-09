# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
import re
from types import StringType, IntType


def split_resize_to(resize_to):
    width = height = ''
    if resize_to:
        assert type(resize_to) is StringType or IntType, _("RESIZE_TO setting, it must be a string or an integer")
        if type(resize_to) is StringType:
            if resize_to.lower().find('x') >= 0:
                pattern = re.compile('^[0-9]*[xX]{1}[0-9]*$')
                assert resize_to.lower() != 'x' and (pattern.match(resize_to) or False), _(
                    """RESIZE_TO setting, 'resize_width' and 'resize_height' field arguments must be an integer
                    or a string in '<width>x<height>' format""")
                width, height = resize_to.lower().split('x')
            else:
                pattern = re.compile('^[0-9]+$')
                assert pattern.match(resize_to) or False, _(
                    """RESIZE_TO setting, 'resize_width' and 'resize_height' field arguments must be an integer
                    or a string in '<width>x<height>' format""")
                width, height = (resize_to, resize_to)
            width = int(width) if width else ''
            height = int(height) if height else ''
        else:
            width, height = (int(resize_to), int(resize_to))
        assert resize_to == '' or resize_to > 0, _("Resize parameters must be positive numbers")
    return (width, height)
