from plupload.models import PluploadField

# In case 'south' is in your INSTALLED_APPS, add to your models.py:
# from plupload import south_introspection_rules

rules = [
    (
        # Which classes this rule applies to
        (PluploadField,),
        # Rules to recover positional args
        [],
        # Rules to recover named args
        # "argument": ["variable where the argument is stores", {...}]
        {
            "upload_to": ["upload_to", {'default': None}],
            "resize_to": ["resize_to", {'default': None}],
            "resize_quality": ["resize_quality", {'default': None}],
        },
    ),
]
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules(rules, ['^plupload\.models\.PluploadField'])
except ImportError:
    pass
