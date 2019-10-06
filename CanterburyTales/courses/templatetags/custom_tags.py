from django import template
from CanterburyTales.courses.models import Audience
import json

register = template.Library()


@register.simple_tag
def audience_map():
    aud = json.dumps(Audience().get_definitions())
    return aud


@register.simple_tag
def audience_breakpoints():
    return list(Audience().get_definitions().keys())


@register.simple_tag
def audience_special_map():
    return json.dumps(Audience().get_special_definitions())
