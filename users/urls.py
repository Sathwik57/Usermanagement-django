from django.urls import path
from .views import DelEmployee, EmployeeDetails, EmployeeList, Home,AddEmployee,Login, Profile
from django.contrib.auth.views import(
    LogoutView, PasswordResetCompleteView, 
    PasswordResetConfirmView, PasswordResetDoneView,
    PasswordResetView)


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('employee/',EmployeeList.as_view(),name='employee-list'),
    path('manager/',EmployeeList.as_view(),name='managers-list'),
    path('employee/details/<str:pk>',EmployeeDetails.as_view(),name='employee'),
    path('employee/add',AddEmployee.as_view(),name='employee-add'),
    path('employee/delete/<str:pk>',DelEmployee.as_view(),name='employee-delete'),
    path('login/',Login.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('profile/',Profile.as_view(),name='profile'),
    path('reset_password/',PasswordResetView.as_view(template_name = 'reset_password.html'),
        name  = 'reset_password'),
    path('reset_password_sent/',PasswordResetDoneView.as_view(template_name = 'reset_password_sent.html'),
        name  = 'password_reset_done'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name = 'reset_password_confirm.html'),
        name  = 'password_reset_confirm'),
    path('reset_password_complete/',PasswordResetCompleteView.as_view(template_name = 'reset_password_complete.html'),
        name  = 'password_reset_complete'),
]