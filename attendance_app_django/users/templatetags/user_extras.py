# Adds additional extras to use in templates - this Python logic is separate from the rest of the project Python code so it doesn't make the template vulnerable to external attacks
from django import template

register = template.Library() # Performs logic required in template in view

# Can let template check if logged in user is in a specific group
@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()