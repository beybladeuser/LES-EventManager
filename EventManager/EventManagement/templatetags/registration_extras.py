from django import template
from EventManagement.models import *

register = template.Library()

@register.filter(name='can_erase_registration')
def can_erase_registration (value,user) :
    return value.canCancel(user) 
