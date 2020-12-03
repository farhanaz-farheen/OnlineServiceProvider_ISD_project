from django.urls import path
from . import views


app_name = 'account'  # here for namespacing of urls.

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("profile/", views.profile, name="profile"),
    path("logout/",views.logout,name="logout"),
    path("Editcustomer/", views.editcustomerprof, name="editcustomer"),
    path("showSearch/", views.showSearch, name="showSearch"),
    #path("searchDetail/", views.searchDetail, name="searchDetail"),
    path("searchDetail/<int:spid>", views.searchDetail, name="searchDetail"),
    path("searchInput/", views.searchInput, name="searchInput"),
    path("finishcart/", views.finishcart, name="finishcart"),
    path("addtocart/", views.addtocart, name="addtocart"),
    path("pending_order/", views.pending_order, name="pending_order"),
    path("accepted_order/", views.accepted_order, name="accepted_order"),
    path("PastOrders/", views.PastOrders, name="PastOrders"),
    path("edit_ordered_service/", views.edit_ordered_service, name="edit_ordered_service"),
    path("edit_accepted_service/", views.edit_accepted_service, name="edit_accepted_service"),
    path("service/<str:service>/",views.serviceDisplay,name="serviceDisplay"),
    path("ratefeed/", views.ratefeed, name="ratefeed"),
    path("recommend/", views.recommend, name="recommend"),
    path("deleteCustomers/",views.deleteCustomers,name = "deleteCustomers"),
]