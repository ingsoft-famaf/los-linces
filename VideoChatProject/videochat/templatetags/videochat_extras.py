from django.template import Library

register = Library()


@register.filter
def get_tuples(value, arg):
    lst = value
    size = arg
    res = []
    while lst:
        sl = lst[:size]
        res.append(tuple(sl))
        lst = lst[size:]
    return res

