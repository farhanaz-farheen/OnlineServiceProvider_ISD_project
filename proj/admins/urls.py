from django.urls import path
from . import views


app_name = 'admins'  # here for namespacing of urls.

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("profile/", views.profile, name="profile"),
    path("Editadmin/", views.editadminprof, name="EditAdminProfile"),
    path("Addadmin/", views.addadmin, name="AddAdminProfile"),
    path("logout/", views.logout, name="logout"),
    path("providerReq/", views.providerReq, name="providerReq"),
    path("serviceReq/", views.serviceReq, name="serviceReq"),
    path("delCust/", views.delCust, name="delCust"),
    path("delProv/", views.delProv, name="delProv"),
]

"""
path("sendmail/",views.sendmail, name = "sendmail")
    path("", views.homepage, name="homepage"),
    path("profile/", views.profile, name="profile"),
    path("Editadmin/", views.editadminprof, name="EditAdminProfile"),
    path("Addadmin/", views.addadmin, name="AddAdminProfile"),
    path("logout/", views.logout, name="logout")
"""