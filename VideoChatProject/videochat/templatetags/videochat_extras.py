from django.template import Library

register = Library()


@register.filter
def get_tuples(lst):
    res = []
    for e in lst:
        print(e.object.title)
    while lst:
        sl = lst[:4]
        res.append(tuple(sl))
        lst = lst[4:]
    return res
