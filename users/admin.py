from django.contrib import admin
from .models import User,ProManager,ProjectField,Employee
# Register your models here.


admin.site.register(User)
admin.site.register(ProManager)
admin.site.register(ProjectField)
admin.site.register(Employee)
