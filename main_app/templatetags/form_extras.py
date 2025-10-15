from django import template

register = template.Library()


@register.filter(name="add_class")
def add_class(value, css):
    try:
        return value.as_widget(attrs={"class": css})
    except AttributeError:
        return value  
