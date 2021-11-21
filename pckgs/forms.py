from django import forms
from django.db import models
from django.forms import ModelForm
from django.forms.widgets import DateInput
from .models import Leave, Req, Software, Version

class SoftwareForm(ModelForm):
    class Meta:
        model = Software
        fields = '__all__'

    def __init__(self, *args, **kwargs) -> None:
        super(SoftwareForm,self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class VersionForm(ModelForm):
    class Meta:
        model = Version
        fields = '__all__'

class RequestForm(ModelForm):
    class Meta:
        model = Req
        fields = ['name','version_name','is_licensed','description']

    def clean(self) :
        data = self.cleaned_data
        
        if  not data['version_name']  and data['name'].name.version_set.exists():
            raise forms.ValidationError('Please select the version')
        elif data['version_name'] not in  data['name'].version_set.all():
            raise forms.ValidationError('Please select correct version against the software selected')

        return super().clean()

class LeaveForm(ModelForm):
    class Meta:
        model = Leave
        fields = ['leave_type','start_date','end_date','description']
        widgets = {
            'start_date':  DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }
        help_texts = {
            'end_date' : '<p>Terms: CLs cant be applied for mor than 2 days consecutively</p>'
        }
    def clean(self) :
        data = self.cleaned_data
        
        if data['end_date'] < data['start_date']:
            raise forms.ValidationError('Please enter proper Start and End dates')
        elif data['leave_type'] == Leave.CASUAL  and ( data['end_date'] - data['start_date']).days > 2:
            raise forms.ValidationError('You cant apply assual leaves for more than 2 days consecutively')

        return super().clean()