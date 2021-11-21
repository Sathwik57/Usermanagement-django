from django.urls import path
from .views import ApprovalsList, ChangeReq, RequestList, SoftwareAdd,SoftwareList,VersionAdd,RaiseReq


urlpatterns = [
    path('add',SoftwareAdd.as_view(), name='software-add'),
    path('versionadd/<str:pk>/',VersionAdd.as_view(), name='version-add'),
    path('list',SoftwareList.as_view(), name='software-list'),
    path('raise-request/<str:req>',RaiseReq.as_view(), name='request-raise'),
    path('view-requests/',RequestList.as_view(), name='view-request'),
    path('view-approvals/',ApprovalsList.as_view(), name='view-approvals'),
    path('approve/<str:req>/<str:pk>/<str:action>',ChangeReq.as_view(), name='approve'),
]