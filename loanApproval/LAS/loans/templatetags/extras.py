from django import template

register = template.Library()


@register.filter(name='lookup')
def lookup(value):
    return value.items()

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 