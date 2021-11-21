from django.http.response import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.views.generic.base import TemplateView
from django.urls import reverse 
from django.views.generic import CreateView ,ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import LeaveForm, RequestForm, SoftwareForm, VersionForm
from .models import Leave, Req, Software
from users.models import User
from .mixins import EmployeeAcessMixin, SuperOwnerMixin
from .utils import approve_reject
# Create your views here.

class SoftwareAdd(LoginRequiredMixin,EmployeeAcessMixin,CreateView):
    template_name = 'pckgs/formadd.html'
    form_class = SoftwareForm
    

    def get_success_url(self):
        print(self.object.id)
        return reverse('version-add',kwargs=  {'pk':self.object.id})

class VersionAdd(LoginRequiredMixin,EmployeeAcessMixin,CreateView):
    template_name = 'pckgs/formadd.html'
    form_class = VersionForm
    def get_success_url(self):
        print(self.object)
        return reverse('software-list')

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        data = {'name': Software.objects.get( id  = self.kwargs['pk'])}
        return data


class SoftwareList(LoginRequiredMixin,ListView):
    template_name = 'pckgs/software-list.html'
    queryset = Software.objects.all()
    context_object_name = 'softwares'

    def get_context_data(self, **kwargs):
        queryset = []
        #Using below query as Distinct on values is not supported in Sqlite
        #else Software.objects.values('category').distinct('category') can be used
        x = list(set([i['category'] for i  in Software.objects.values('category')]))
        print(x)
        for category in sorted(x, reverse=True) :
            queryset += tuple((Software.objects.filter(category= category),False))
        context ={'itemlist': queryset}
        context.update(kwargs)
        return super().get_context_data(**context)

class RaiseReq(LoginRequiredMixin,SuperOwnerMixin, CreateView):
    template_name = 'pckgs/requestform.html'

    def get_success_url(self):
        return reverse('software-list')
  
    def get_form_class(self):
        if self.kwargs['req'] == 'Leave':
            self.page = 'Leave'
            return LeaveForm
        else:
            self.page = 'Software'
            return RequestForm

    def get_context_data(self, **kwargs):
        owner = self.request.user.is_superuser
        context = {'form' : self.get_form() , 'page': self.page,'access': owner }
        return super().get_context_data(**context)

    def form_valid(self, form ):
        self.user = self.request.user
        temp = form.save(commit = False)
        temp.raised_by = self.user
        try:
            temp.approver = self.user.employee.reporting_manager
        except :
            temp.approver = User.objects.get(is_superuser = True)                
        return super().form_valid(form)

    def post(self, request, *args: str, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class RequestList(LoginRequiredMixin,SuperOwnerMixin,TemplateView):
    template_name = 'pckgs/request_list.html'

    def get_context_data(self, **kwargs):
        kwargs['user']= self.request.user 
        return super().get_context_data(**kwargs)


class ApprovalsList(LoginRequiredMixin,EmployeeAcessMixin,TemplateView):
    template_name = 'pckgs/approvals_list.html'

    def get_context_data(self, **kwargs):
        kwargs['user']= self.request.user 
        return super().get_context_data(**kwargs)

class ChangeReq(LoginRequiredMixin,EmployeeAcessMixin,TemplateView):
    next_page = 'view-approvals'
    
    def get_queryset(self) :
        if 'L' in self.kwargs['req']:
            return Leave.objects.get(id = self.kwargs['pk'])
        else:
            return Req.objects.get(id = self.kwargs['pk'])

    def get_next_page(self):
        next_page = resolve_url( self.next_page) if self.next_page else None
        return next_page

    def dispatch(self, request, *args, **kwargs) :
        req = self.get_queryset()
        status = approve_reject(req,self.kwargs['action'])
        print(status)
        next_page = self.get_next_page()
        if  next_page:
            return HttpResponseRedirect(next_page)
        return super().dispatch(request, *args, **kwargs)
