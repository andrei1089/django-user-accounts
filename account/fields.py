from django.db import models

from account.conf import settings


class TimeZoneField(models.CharField):
    
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, *args, **kwargs):
        defaults = {
            "max_length": 100,
            "default": "",
            "choices": settings.ACCOUNT_TIMEZONES,
            "blank": True,
        }
        defaults.update(kwargs)
        return super(TimeZoneField, self).__init__(*args, **defaults)

try:
    from south.modelsinspector import add_introspection_rules
    rules = [
      (
        (TimeZoneField,),
        [],
        {
            "max_length": ["max_length", {"default": 100}],
            "default": ["default", {"default": ""}],
            "choices": ["choices", {"default": settings.ACCOUNT_TIMEZONES}],
            "blank": ["blank", {"default": True}],
        },
      )
    ]
    add_introspection_rules(rules, ["^account\.fields\.TimeZoneField"])
except ImportError:
    pass
