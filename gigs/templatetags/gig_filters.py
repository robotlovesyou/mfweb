from django.template import Library

register = Library()


def set_widget_attribute(field, attribute, value):
    field.widget.attrs[attribute] = value


@register.filter(name='with_class', is_safe=True)
def with_class(boundfield, class_val):
    """
    render a field with the additional classes set
    """
    set_widget_attribute(boundfield.field, 'class', class_val)

    return boundfield
