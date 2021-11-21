from django.contrib import admin
from .models import Leave, Req, Software,Version


# Register your models here.
admin.site.register(Software)
admin.site.register(Version)
admin.site.register(Leave)
admin.site.register(Req)