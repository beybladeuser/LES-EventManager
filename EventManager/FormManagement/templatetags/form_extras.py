from django import template
from FormManagement.models import *

register = template.Library()

@register.filter(name='can_display_form')
def can_display_form(value, user):
    return value.canDisplay(user)

@register.filter(name='can_edit_form')
def can_edit_form(value, user):
    return Form.objects.get(pk=value.id).canEdit(user)

@register.filter(name='can_unarchive_form')
def can_unarchive_form(value, user):
    return Form.objects.get(pk=value.id).canUnarchive(user)

@register.filter(name='can_archive_form')
def can_archive_form(value, user):
    return Form.objects.get(pk=value.id).canArchive(user)

@register.filter(name='can_publish_form')
def can_publish_form(value, user):
    return Form.objects.get(pk=value.id).canPublish(user)
    
@register.filter(name='can_create_form_fromType')
def can_create_form_fromType(value, user):
    return value.canCreate(user)

@register.filter(name='can_associate_with_questionType')
def can_associate_with_questionType(value, questionType):
    return value.canAssociateQuestionType(questionType)