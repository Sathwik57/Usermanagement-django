from django.contrib.auth.mixins import AccessMixin

class SuperOwnerMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class EmployeeAcessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if  request.user.is_employee:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

