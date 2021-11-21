from django.db.models.signals import post_save,post_delete
from .models import ProManager, ProjectField, User,Employee
from django.contrib import messages




def delete_user(sender,instance,**kwargs):
    user = instance.user
    user.is_active = False
    user.save()

post_delete.connect(delete_user,sender = Employee, weak =False)

