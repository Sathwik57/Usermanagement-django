from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    first_name =models.CharField(max_length=20)
    last_name =models.CharField(max_length=20,null=True,blank= True) 
    username = models.CharField(max_length=10,unique=True)
    email = models.EmailField(_('email address'), unique=True)
    is_manager = models.BooleanField(default=True)
    is_employee = models.BooleanField(default=False)
    profile_image = models.ImageField(default = 'default.png',null=True,blank =True)

    id = models.UUIDField(default = uuid.uuid4 ,unique= True,editable= False ,primary_key=True)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}({self.username})' if self.last_name else f'{self.first_name}({self.username})'

    class Meta:
        # order_with_respect_to = 'username'
        ordering = ['-username']   

class ProjectField(models.Model):
    category = models.CharField(max_length=20)
    id = models.UUIDField(default = uuid.uuid4 ,unique= True,editable= False,primary_key=True)


    def __str__(self) -> str:
        return "%s" %self.category


class ProManager(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    project = models.OneToOneField(ProjectField , on_delete=models.CASCADE)
    intro = models.CharField(max_length=200,null=True,blank=True)
    skills = models.TextField(null=True,blank=True)
    experience = models.FloatField(default=0)
    def __str__(self) -> str:
        return "%s" %self.user


class Employee(models.Model): 
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    reporting_manager = models.ForeignKey(ProManager, on_delete= models.SET_NULL,null=True)
    intro = models.CharField(max_length=200,null=True,blank=True)
    skills = models.TextField(null=True,blank=True)
    experience = models.FloatField(default=0)


    def __str__(self) -> str:
        return "%s" %self.user

    def skill_set(self):
        if self.skills:
            skill = self.skills.split(',')
            return ['#'+x.title() for x in skill]
        return None