from django.template import Library

register = Library()


@register.filter(name='with_classes', is_safe=True)
def with_classes(field, classes):
    """
    render a field with the additional classes set
    """
    if field.field.widget.attrs.get('class'):
        field.field.widget.attrs['class'] += ' ' + classes
    else:
        field.field.widget.attrs['class'] = classes

    return field
