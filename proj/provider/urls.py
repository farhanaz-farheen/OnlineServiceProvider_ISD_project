from django.urls import path
from . import views


app_name = 'provider'  # here for namespacing of urls.

urlpatterns = [
	path("", views.homepage, name="homepage"),
	path("register/", views.register, name="register"),
	path("login/", views.login, name="login"),
	path("setup/", views.setup, name="setup"),
	path("setup2/", views.setup2, name="setup2"),
	path("setup3/", views.setup3, name="setup3"),
	path("setup4/", views.setup4, name="setup4"),
	path("profile/", views.profile, name="profile"),
	path("regService/",views.regService, name="regService"),
	path("regServiceEdit/",views.regServiceEdit, name="regServiceEdit"),
	path("registerMsg/", views.registerMsg, name="registerMsg"),
	path("inbox/",views.showReqs,name="inbox"),
	path("orderDetails/",views.orderDetails,name = "orderDetails"),
	path("edit/",views.edit,name = "edit"),
	path("deleteProvider/",views.deleteProvider,name = "deleteProvider"),
	path("logout/",views.logout,name = "logout"),
	path("addpromo/",views.addpromo,name = "addpromo"),
	path("editcost/",views.editcost,name="editcost"),
	path("negotiate/",views.negotiate,name="negotiate"),
	path("AcceptOrder/",views.AcceptOrder,name="AcceptOrder"),
	path("RejectOrder/",views.RejectOrder,name="RejectOrder"),
	path("Processing/",views.Processing,name="Processing"),
	path("AcceptedOrders/",views.AcceptedOrders,name="AcceptedOrders"),
	path("negotiate2/",views.negotiate2,name="negotiate2"),
	path("CancelOrder/",views.CancelOrder,name="CancelOrder"),
	path("CompletedOrder/",views.CompletedOrder,name="CompletedOrder"),
	path("PastOrders/",views.PastOrders,name="PastOrders"),
	path("editDP/",views.editDP,name="editDP"),
]

#    path("provider1/", views.providerHome, name="providerHome"),
"""
	path("", views.homepage, name="homepage"),
	path("register/", views.register, name="register"),
	path("login/", views.login, name="login"),
	path("profile/", views.profile, name="profile"),
	path("edit/", views.editproviderprof , name="editproviderprof"),
	path("logout/", views.logout , name="logout"),
	path("promo/", views.addpromo, name="addpromo"),
	path("editcost/", views.editcost , name="editcost"),"""