from django.template.defaulttags import register
import json
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def parse(value):
    return json.loads(value)