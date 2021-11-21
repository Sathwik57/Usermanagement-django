from django.db import models
from django.utils.translation import gettext_lazy as _ 
import uuid
from users.models import User

# Create your models here.

class Software(models.Model):
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=100,unique=True)
    id = models.UUIDField(default = uuid.uuid4 ,unique= True,editable= False,primary_key=True)

    def __str__(self) -> str:
        return self.category + '-' +self.name
    
    class Meta:
        ordering = ['-category','-name']

class Version(models.Model):
    name = models.ForeignKey(Software,max_length=50,on_delete=models.CASCADE)
    version = models.CharField(max_length=100)
    is_licensed = models.BooleanField(default=False)   
    id = models.UUIDField(default = uuid.uuid4 ,unique= True,editable= False,primary_key=True)

    def __str__(self) -> str:
        return self.version.title()+'('+self.name.name+')'

class Leave(models.Model):
    SICK = 'SL'
    CASUAL = 'CL'
    EARNED = 'EL'
    LEAVE_CHOICES = [
        (SICK,'Sick Leave'),
        (CASUAL,'Casual Leave'),
        (EARNED,'Earned Leave')
    ]
    leave_type = models.CharField(max_length=15,choices=LEAVE_CHOICES,default=SICK)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.CharField(max_length=200,verbose_name= _('Remarks'))

    is_approved = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)

    raised_by = models.ForeignKey(User, on_delete=models.CASCADE , related_name='raised_by1',null=True)
    approver = models.ForeignKey(User, on_delete=models.CASCADE , related_name='approver1',null=True)

    id = models.UUIDField(default = uuid.uuid4 ,max_length=36, unique= True,editable= False,primary_key=True)

    def __str__(self) -> str:
        return str(self.start_date) + ' to ' + str(self.end_date)

class Req(models.Model):
    name = models.ForeignKey(Software,on_delete=models.CASCADE)
    version_name = models.ForeignKey(
        Version,on_delete=models.CASCADE,related_name='versionname',null=True,blank=True
    )
    description = models.CharField(max_length=200,verbose_name= _('Remarks'))

    is_approved = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    is_licensed = models.BooleanField(default=False)
    
    raised_by = models.ForeignKey(User, on_delete=models.CASCADE , related_name='raised_by2',null=True)
    approver = models.ForeignKey(User, on_delete=models.CASCADE , related_name='approver2',null=True)
    
    id = models.UUIDField(default = uuid.uuid4 ,unique= True,editable= False,primary_key=True)

    def __str__(self) -> str:
        return f'{self.name}-{self.version_name}'