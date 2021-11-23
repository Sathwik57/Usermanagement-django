from datetime import date 
from copy import deepcopy
from django import template
from pckgs.models import Software

register = template.Library()



@register.filter
def fil(value):
    x = value.split()
    a = deepcopy(x)
    x.pop(1)
    d1 = date(year=int(x[2]),month=int(x[1]),day=int(x[0]))
    today = date.today()
    delta = (today - d1).days 
    year = delta//365
    months = (delta % 365)//30
    a.pop(2)
    return ' '.join(i for i in a) + f'({year}yrs {months}months)'

@register.filter
def req_count(user):
    l , c =[] , 0
    l += user.approver2.all()
    l += user.approver1.all()
    for req in l : 
        if not req.is_closed:
            c += 1
    return c if c != 0 else None