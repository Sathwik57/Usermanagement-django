from django.core.mail import send_mail

from django.contrib  import messages
from django.contrib.auth.mixins import LoginRequiredMixin,AccessMixin
from django.contrib.auth.views import LoginView   
from django.views.generic import ListView,TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse
from pckgs.mixins import SuperOwnerMixin

from users.forms import EmpolyeeAddForm, LoginForm, UpdateEmpForm, UpdateMgrForm
from users.utils import generate_link
from .models import *
from django.conf import settings
# Create your views here.

class Home(TemplateView):
    template_name= 'home.html'

class EmployeeList(AccessMixin,ListView):
    template_name = 'users/employee_list.html'
    queryset = Employee.objects.all()
    context_object_name = 'employee'

    def dispatch(self, request, *args, **kwargs) :
        if not request.user.is_authenticated or request.user.is_employee:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = ProManager.objects.all() if 'manager' in self.request.path else Employee.objects.all()
        elif self.request.user.is_manager:
            mngr = ProManager.objects.get(user = self.request.user)
            queryset = Employee.objects.filter(reporting_manager= mngr)
        return queryset.all()

class EmployeeDetails(LoginRequiredMixin,DetailView):
    template_name = 'users/emp.html'
    context_object_name = 'employee'

    def get_queryset(self):
        if self.request.user.is_superuser:
            if self.request.path.split('/')[1] != 'employee':
                return ProManager.objects.all()
        return Employee.objects.all()
        # return emp

class AddEmployee(LoginRequiredMixin,CreateView):
    template_name = 'users/employee_add.html'

    form_class = EmpolyeeAddForm

    def get_success_url(self):
        messages.success(self.request, f'Employee{self.object} Created')
        return reverse('employee-list')
    
    def form_valid(self, form= EmpolyeeAddForm):
        temp = form.save(commit= False)
        user_name = int(User.objects.all().first().username[2:])
        user_name = 'CT' + str(user_name+1)
        temp.username = user_name
        temp.is_manager= False
        temp.is_employee = True
        from  string import ascii_letters
        from random import choices
        l = list(ascii_letters) + [str(i) for i in range(0,9)]
        pswd = ''.join(x for x in choices(l, k = 9))
        temp.set_password(pswd)
        form.save()
        print(temp,self.object)
        Employee.objects.create(
                user = temp,
                reporting_manager = ProManager.objects.get(user = self.request.user)
            )
        link = generate_link(temp,self.request)
        print(settings.EMAIL_HOST_USER,temp.email)
        send_mail(
            subject='Recruited to Crazy Tech!!',
            message = f"""Welcome to Crazy Tech!.. Please click below link to reset password and login 
            link: {link}
            User id : {temp.username}""",
            from_email= settings.EMAIL_HOST_USER,
            recipient_list=[temp.email]
        )


        return super().form_valid(form)

class UpdateEmployee(LoginRequiredMixin,UpdateView):
    
    def get_form_class(self) :
        return UpdateEmpForm if self.request.user.is_employee else UpdateMgrForm

    def get_queryset(self) :
        return Employee.objects.all() if self.request.user.is_employee else ProManager.objects.all()

class DelEmployee(LoginRequiredMixin,DeleteView):
    template_name = 'users/employee_delete.html'
    queryset = Employee.objects.all()

    def get_success_url(self):
        print(self.object)
        return reverse('employee-list')

class Login(LoginView):
    template_name = 'loginform.html'
    form_class = LoginForm
    redirect_authenticated_user = True
    # success_url = reverse('home')

class Profile(LoginRequiredMixin,SuperOwnerMixin,TemplateView):
    template_name = 'profile.html'
    
    def get_context_data(self, **kwargs):
        user = self.request.user
        if  user.is_manager:
            profile= ProManager.objects.get(user =user)
            role ='mgr'
        else :
            profile = Employee.objects.get(user =user) if not user.is_superuser else None
            role= None
        return {'user': self.request.user , 'role': role ,'profile': profile}
     
