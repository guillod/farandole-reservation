from django import template

register = template.Library()

@register.filter
def chunks(lst, chunk_size):
    limit = len(lst) // chunk_size
    for idx in range(limit):
        yield lst[chunk_size * idx : chunk_size * (idx + 1)]

@register.filter
def columns(lst, nb):
    # number of elements in a column
    chunk_size = (len(lst)-1) // nb + 1
    # actual number of colums (can be smaller than nb)
    limit = (len(lst)-1) // chunk_size + 1
    for idx in range(limit):
        yield lst[chunk_size * idx : chunk_size * (idx+1)]
