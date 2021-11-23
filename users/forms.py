from django.forms.models import ModelForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from .models import Employee, ProManager
from django.utils.translation import gettext, gettext_lazy as _

User = get_user_model()


class EmpolyeeAddForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        

    def __init__(self, *args, **kwargs) -> None:
        super(EmpolyeeAddForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
        
            field.widget.attrs.update(
                {'class': 'form-control'})


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is deleted from system. Login restricted .. "),
    }

    def __init__(self, *args, **kwargs) -> None:
        super(LoginForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            
            field.widget.attrs.update(
                {'class': 'form-control', 'placeholder': field.label})

class UpdateEmpForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['intro' , 'skills']

    def __init__(self, *args, **kwargs) -> None:
        super(UpdateEmpForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            
            field.widget.attrs.update(
                {'class': 'form-control', 'placeholder': field.label})

class UpdateMgrForm(ModelForm):
    class Meta:
        model = ProManager
        fields = ['intro' , 'skills']

    def __init__(self, *args, **kwargs) -> None:
        super(UpdateMgrForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            
            field.widget.attrs.update(
                {'class': 'form-control', 'placeholder': field.label})