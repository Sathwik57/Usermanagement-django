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