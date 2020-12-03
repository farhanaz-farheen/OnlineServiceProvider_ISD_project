from django.shortcuts import render, redirect
from .models import *
from .forms import *
from .util import *
from provider.models import requested_provider, service,requested_service


# Create your views here.
def homepage(request):
	valid= "True"
	if request.method =="POST":
	    form = loginForm(request.POST)
	    if form.is_valid():
	        cd = form.cleaned_data
	        loginuser = isUser(cd['email'], cd['password'])
	        if loginuser is None:
	        	valid = "False"
	        else:
	        	request.session['adminuser']=loginuser.firstname
	        	request.session['adminid'] = loginuser.adminid
	        	request.session.modified = True
	        	return redirect("admins:profile")
	else:
		form = loginForm()
		if 'valid' in request.GET:
			valid = "True"
	return render(request = request,template_name='admins/login.html',
		context={'form': form, 'valid':valid})

def profile(request):
	categories = getCategories()
	if request.method =="POST":
		catform = categoryForm(request.POST, request.FILES)
		servform = serviceForm(request.POST, request.FILES)
		reqform = optionForm(request.POST)
		if catform.is_valid():
			formval =catform.save()
			print("catform: ",catform)
			#catform.reset()
			return redirect("admins:profile")
		elif servform.is_valid():
			print("servform: ",servform)
			formval =servform.save()
			return redirect("admins:profile")
		elif reqform.is_valid():
			cd = reqform.cleaned_data
			if len(cd['btn'])>0:
				request.session['reqProvId'] = int(cd['btn'])
				request.session.modified = True
				return redirect("admins:serviceReq")	    	
	else:
		catform = categoryForm()
		servform = serviceForm()
		reqform = optionForm()
		if 'valid' in request.GET:
			valid = "True"

	return render(request = request,template_name='admins/profile.html',
		context={'categories':categories , 'user':request.session['adminuser']
		,'totalreqs':totalProviderReqs(),'providers':getProviderReqs(),
		'catform':catform, 'servform':servform})

def editadminprof(request):
	adminid = request.session['adminid']
	prevprof = getProfileDetails(adminid)

	if request.method =="POST":
	    form = EditAdminForm(request.POST)
	    if form.is_valid():
	        cd = form.cleaned_data
	        adminuser = editUser(request.session['adminid'],cd)
	        request.session['adminuser'] = adminuser.firstname
	        request.session.modified = True
	        return redirect("admins:profile")

	else:
		form = EditAdminForm()
	return render(request = request,template_name='admins/editadmin.html',
		context={'form': form, 'user':request.session['adminuser']
				,'totalreqs':totalProviderReqs(),'providers':getProviderReqs(),'prev' : prevprof})

def addadmin(request):
	valid = "True"
	if request.method =="POST":
	    form = AddAdminForm(request.POST)
	    if form.is_valid():
	        cd = form.cleaned_data
	        if isNewUser(cd['email']):
	        	newUser = admin_model(firstname=cd['firstname'],lastname=cd['lastname'],email=cd['email'],
	        		phone=cd['phone'],password=cd['password'])
	        	newUser.save()
	        	return redirect("admins:profile")
	        else:
	        	valid = "False"
	        	return redirect("admins:AddAdminProfile")
	else:
		form = AddAdminForm()
		valid = "True"
	return render(request = request,template_name='admins/addadmin.html',
		context={'valid': valid, 'form': form, 'user':request.session['adminuser'],
					'totalreqs':totalProviderReqs(),'providers':getProviderReqs()})

def logout(request):
	#print(request.session['user'])
	del request.session['adminid']
	del request.session['adminuser']
	request.session.modified = True
	return redirect("admins:homepage")

def providerReq(request):
	
	if request.method =="POST":
		form = optionForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			if len(cd['btn'])>0:
				request.session['reqProvId'] = int(cd['btn'])
				request.session.modified = True
				return redirect("admins:serviceReq")		
	else:
		form = optionForm()

	return render(request = request,template_name='admins/providerReq.html',
		context={'form': form, 'user':request.session['adminuser'], 'providers':getProviderReqs()})

def serviceReq(request):
	reqprovid = request.session['reqProvId']
	reqProvider = requested_provider.objects.filter(id=reqprovid)[0]
	serviceDetails = services_images(reqProvider)
	invalid = "False"
	approved = []
	rejected = []
	correctId = False
	if request.method =="POST":
		form = ProviderRequestForm(request.POST,total=len(serviceDetails))
		print(form)
		if form.is_valid():
			cd = form.cleaned_data
			photoid = cd['idoption']
			print(cd)
			if photoid[-1]=="1":
				#request.session['photoid'] = True
				correctId = True
			else:
				correctId = False
			for i in range(1,len(serviceDetails)+1):
				choice = cd['serv_%s' %i]
				if len(choice)>0:
					if choice[-1]=="1":
						approved.append(choice[:-2])
					elif choice[-1]=="2":
						rejected.append(choice[:-2])

					
						#request.session['photoid'] = False
					#request.session['approved'] = approved.copy()
					#request.session['rejected'] = rejected.copy()
					#request.session.modified = True
					#return redirect("admins:sendmail")
					#providerRequestProcess(request.session['adminid'],reqProvider,request.session['photoid'],request.session['approved'],request.session['rejected'])
			stat=providerRequestProcess(request.session['adminid'],reqProvider,correctId,approved,rejected)
			del request.session['reqProvId']
			request.session.modified = True
			if stat==0:
				return redirect("admins:profile")
			else:
				return render(request = request,template_name='admins/emailFailed.html')
		
	else:
		form = ProviderRequestForm(total=len(serviceDetails))
		invalid = "False"	
	return render(request = request,template_name='admins/serviceReq.html',
		context={'form': form, 'user':request.session['adminuser'], 
		'services_images':serviceDetails,'prov':getRequestedProvider(reqprovid)})


def delCust(request):
	return render(request = request,template_name='admins/delCust.html',
		context={'user':request.session['adminuser'], 'orders':getDeletedCustomers(),'totalreqs':totalProviderReqs(),'providers':getProviderReqs()})


def delProv(request):
	return render(request = request,template_name='admins/delProv.html',
		context={'user':request.session['adminuser'], 'orders':getDeletedProviders(),'totalreqs':totalProviderReqs(),'providers':getProviderReqs()})