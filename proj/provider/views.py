from django.shortcuts import render, redirect
from .models import *
from .forms import *
from .util import *
from .format import *
import json
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

# Create your views here.
def homepage(request):
	return render(request = request,template_name='provider/homepage.html',
		context= {'user':"None"})

def register(request):
	trending = getTrendingServices()
	valid= "True"
	categories = getCategories()
	if request.method =="POST":
	    form = registerForm(request.POST, request.FILES)
	    if form.is_valid():
	        cd = form.cleaned_data	 
	        if isNewUser(cd['email']):
	        	formval=form.save()
	        	request.session['reqUserID'] = formval.id
	        	request.session.modified = True
	        	return redirect("provider:regService")
	        else:
	        	valid = "False"
	else:
		form = registerForm()
		if 'valid' in request.GET:
			valid = "True"
	return render(request = request,template_name='provider/register.html',
		context={'form': form, 'valid': valid, 'user':"None", 'categories': categories,'trend':trending,'trendlen':len(trending)})

def regService(request):
	trending = getTrendingServices()
	reqprovid = request.session['reqUserID']
	reqProvider = requested_provider.objects.filter(id=reqprovid)[0]
	category = getCatname(reqprovid)
	services = getServices(category)
	serviceDetails = services_images(reqProvider)
	if request.method =="POST":
	    form = requestServiceForm(request.POST, request.FILES, services=services)
	    
	    if form.is_valid():
	    	formval = form.save(commit = False)
	    	formval.provider = reqProvider
	    	formval.service = service.objects.filter(servname=form.cleaned_data['serviceName'])[0]
	    	formval.save()
	    	
	else:
		form = requestServiceForm(services = services)
		
	return render(request = request,template_name='provider/regService.html',
		context={'form': form,'user':"None",'trend':trending,'trendlen':len(trending)})

def regServiceEdit(request):
	reqprovid = request.session['reqUserID']
	reqProvider = requested_provider.objects.filter(id=reqprovid)[0]
	serviceDetails = services_images(reqProvider)
	if request.method =="POST":
	    servform = serviceDetForm(request.POST)
	    if servform.is_valid():
	    	cd = servform.cleaned_data
	    	requested_service.objects.filter(id=int(cd['btn'])).delete()
	    	return redirect("provider:regServiceEdit")
	else:
		servform = serviceDetForm()
	return render(request = request,template_name='provider/regServiceEdit.html',
		context={'user':"None",'fname':reqProvider.firstname,'lname':reqProvider.lastname,
					'email':reqProvider.email,'phone':reqProvider.phone,
					'desc':reqProvider.desc,'idimg':reqProvider.idImage.url,
					'catname':reqProvider.catname.catname,'services_images':serviceDetails})

def registerMsg(request):
	return render(request = request,template_name='provider/registerMsg.html',
		context={'user':"None"})

def login(request):
	valid= "True"
	if request.method =="POST":
	    form = loginForm(request.POST)
	    if form.is_valid():
	        cd = form.cleaned_data
	        provuser,isRegistered = isUser(cd['email'],cd['password'])
	        if provuser is None:
	        	valid = "False"
	        elif isRegistered:
	        	request.session['provid'] = provuser.provid
	        	request.session['provname'] = provuser.firstname
	        	request.session.modified = True
	        	return redirect("provider:setup")
	        else:
	        	return redirect("provider:registerMsg")
	else:
		form = loginForm()
		if 'valid' in request.GET:
			valid = "True"
	return render(request = request,template_name='provider/login.html',
		context={'form': form, 'valid':valid ,'user':"None"})

def setup(request):
	provid = request.session['provid']
	allowed = getAllowedServices(provid)
	if len(allowed)==0:
		return redirect("provider:profile")
	name,email,phone,desc = getProviderForSetup(provid)

	return render(request = request,template_name='provider/setup.html',
		context= {'name':name})	

def setup2(request):
	provid = request.session['provid']
	name,email,phone,desc = getProviderForSetup(provid)
	provObj = provider.objects.filter(provid=provid)[0]
	prev_path = provObj.provImage.path
	print("Previous dp ",provObj.provImage,provObj.provImage.name,prev_path,provObj.provImage.url)
	if request.method == 'POST':
		print(request.POST.get('location'))
		provObj.location=request.POST['location']
		provObj.save()
		if request.FILES.get('dp'):
			newdp = request.FILES.get('dp')
			fs = FileSystemStorage()
			filename = fs.save(newdp.name, newdp)
			#uploaded_file_url = fs.url(filename)
			provObj.provImage = filename
			new_path = settings.MEDIA_ROOT + "/providerImage/" + newdp.name
			#os.rename(prev_path, new_path)
			provObj.path=new_path
			provObj.save()
		return redirect('provider:setup3')


	return render(request = request,template_name='provider/setup2.html',
		context= {'user':request.session['provname'],
					'name':name,'email':email,'phone':phone,'desc':desc})

def setup3(request):
	provid = request.session['provid']
	allowed = getAllowedServices(provid)
	if request.method=="POST":
		form = setupForm(request.POST,total=len(allowed))
		if form.is_valid():
			cd = form.cleaned_data
			print(cd)
			setupProv(provid,cd,len(allowed))
			return redirect("provider:profile")

	form = setupForm(total=len(allowed))

	return render(request = request,template_name='provider/setup3.html',
		context= {'form':form,'als':allowed,'user':request.session['provname']})

def setup4(request):
	provid = request.session['provid']
	provider_ = provider.objects.filter(provid=provid)[0]
	spids = [s.id for s in service_provider.objects.filter(provid=provider_)]
	servs = getServicesForSetupPage(spids)
	total = len(spids)
	forms = []
	for i in range(total):
		servs[i].form = serviceImageForm()

	if request.method=="POST":
		if "done" in request.POST:
			return redirect('provider:profile')
		for i in range(total):
			servs[i].form = serviceImageForm(request.POST,request.FILES)
			if servs[i].form.is_valid():
				servs[i].form.cleaned_data['spid'] = service_provider.objects.filter(id=spids[i])[0]
				print(servs[i].form.cleaned_data)
				formval = servs[i].form.save(commit=False)
				formval.spid=  service_provider.objects.filter(id=spids[i])[0]
				formval.save()

		return redirect('provider:setup4')





	return render(request = request,template_name='provider/setup4.html',
		context= {'val':servs,'user':request.session['provname']})
	


def profile(request):
	provid = request.session['provid']
	provuser = provider.objects.filter(provid=provid)[0]
	imgpath = getImgPath(provid)
	
	return render(request = request,template_name='provider/homeLogged.html',
		context= {'user':request.session['provname'],'photo' : imgpath})


def edit(request):
	print("\nTHe image path now:::\n")
	imgPath = None
	print("\nthe provid is: ",request.session['provid'])
	imgPath = getImgPath(request.session['provid'])
	print("\nThe image path is: ",imgPath)
	print("\ndfdfdhg---------")
	details = getProfileDetails(request.session['provid'])
	provphone = details.phone
	provemail = details.email
	provdesc = details.desc
	Name = details.name
	print("lallagafhg---------")
	fname = details.firstname
	lname = details.lastname
	print("rtrtgafhg---------")
	print("lallagafhg---------",fname,lname)
	loc = details.location
	if request.method =="POST":
		print("\nChecking edit\n")
		form = EditProviderForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user= editUser(request.session['provid'],cd)
			request.session['provname']= user.firstname
			request.session['provid'] = user.provid
			print("\nChecking edit profile\n")
			request.session.modified = True
			return redirect("provider:profile")

	else:
		form = EditProviderForm()
	return render(request = request,template_name='provider/editprovider.html',
		context={'firstname':fname,'lastname':lname,'form': form, 'user':request.session['provname'],'name' : Name,'imgpath' : imgPath,'phone' : provphone, 'email' : provemail,'desc' : provdesc, 'loc':loc})

def logout(request):
	del request.session['provid']
	del request.session['provname']
	request.session.modified = True
	return redirect("provider:homepage")

def showReqs(request):
	trending= getTrendingServices()
	provid = request.session['provid']
	provuser = provider.objects.filter(provid=provid)[0]
	if request.method =="POST":
		form = detForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			if len(cd['btn'])>0:
				print(cd['btn'])
				request.session['orderid'] = int(cd['btn'])
				print("req custid is ",request.session['orderid'])
				request.session.modified = True
				return redirect("provider:orderDetails")		
	else:
		form = detForm()
	return render(request = request,template_name='provider/inbox.html',
		context= {'user':request.session['provname'],'totalreqs':str(len(getOrderReqs(provid))),'orders':getOrderReqs(provid),
		'trend':trending,'trendlen':len(trending)})

	'''
	return render(request = request,template_name='admins/profile.html',
		context={'categories':categories , 'user':request.session['adminuser']
		,'totalreqs':totalProviderReqs(),'providers':getProviderReqs(),
		'catform':catform, 'servform':servform})
		'''

def orderDetails(request):

	ordid = request.session['orderid']
	orderservice, ll = getOrderServReqs(ordid,request.session['provid'])
	return render(request = request,template_name='provider/orderDetails.html',
		context= {'user':request.session['provname'],'totalreqs':len(orderservice),
			'orderservice':orderservice , 'll':json.dumps(ll)})

def addpromo(request):
	if request.method =="POST":
		form = AddPromoForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			#user= editUser(request.session['provid'],cd)
			#request.session['provname']= user.firstname
			#request.session['provid'] = user.provid
			#request.session.modified = True
			#return redirect("provider:profile")

	else:
		form = AddPromoForm()
	return render(request = request,template_name='provider/addpromo.html',
		context={'form': form, 'user':request.session['provname']})



def editcost(request):
	trending=getTrendingServices()
	provID = request.session['provid']
	strtemp = getServicesProvided(provID)
	print("PRINTING.. ",strtemp)
	if request.method =="POST":
		form = costEditForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			editCost(provID,cd)
	else:
		form = costEditForm()
	return render(request = request,template_name='provider/editcost.html',
		context={'form': form, 'user':request.session['provname'],'services':getServicesProvided(provID)
					,'trend':trending,'trendlen':len(trending)})

def negotiate(request):
	provID = request.session['provid']
	ordid = request.session['orderid']
	Custid = getServReqs(ordid,provID)
	orderservice = getOrderServReqs(ordid,provID)
	orderservID = orderservice[0][0].id
	msgs = getMsgs(orderservID)
	if request.method =="POST":
		form = negotiateForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			#insert into database
			print("orderservid is: ",orderservID)
			#custID = orderCust.custid
			if Custid is not None:
				SendMessage(Custid,provID,orderservID,cd)
				msgs = getMsgs(orderservID)
				return redirect("provider:negotiate")

	else:
		form = negotiateForm()
	return render(request = request,template_name='provider/negotiate.html',
		context={'form': form, 'user':request.session['provname'],'msgs':msgs})

def RejectOrder(request):
	provID = request.session['provid']
	ordid = request.session['orderid']
	orderservice = getOrderServReqs(ordid,provID)
	orderservID = orderservice[0][0].id
	Custid = getServReqs(ordid,provID)
	rejectOrder(Custid,provID,orderservID)

	del request.session['orderid']
	request.session.modified = True
	return redirect("provider:inbox")

def CancelOrder(request):
	provID = request.session['provid']
	ordid = request.session['orderid']
	orderservice = getAccOrderServReqs(ordid,provID)
	orderservID = orderservice[0][0].id
	Custid = getAccServReqs(ordid,provID)
	rejectOrder(Custid,provID,orderservID)

	del request.session['orderid']
	request.session.modified = True
	return redirect("provider:Processing")

def CompletedOrder(request):
	return redirect("provider:Processing")


def AcceptOrder(request):
	provID = request.session['provid']
	ordid = request.session['orderid']
	orderservice = getOrderServReqs(ordid,provID)
	orderservID = orderservice[0][0].id
	Custid = getServReqs(ordid,provID)
	acceptOrder(Custid,provID,orderservID)

	del request.session['orderid']
	request.session.modified = True
	return redirect("provider:inbox")

def Processing(request):
	trending = getTrendingServices()
	provid = request.session['provid']
	provuser = provider.objects.filter(provid=provid)[0]
	if request.method =="POST":
		form = detForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			if len(cd['btn'])>0:
				print(cd['btn'])
				request.session['orderid'] = int(cd['btn'])
				print("req custid is ",request.session['orderid'])
				request.session.modified = True
				return redirect("provider:AcceptedOrders")		
	else:
		form = detForm()
	return render(request = request,template_name='provider/Accepted.html',
		context= {'trend':trending,'trendlen':len(trending),'user':request.session['provname'],'totalreqs':str(len(getAccOrderReqs(provid))),'orders':getAccOrderReqs(provid)})

def AcceptedOrders(request):
	ordid = request.session['orderid']
	orderservice, ll = getAccOrderServReqs(ordid,request.session['provid'])
	return render(request = request,template_name='provider/AcceptedOrders.html',
		context= {'user':request.session['provname'],'totalreqs':len(orderservice),
			'orderservice':orderservice , 'll':json.dumps(ll)})

def negotiate2(request):
	provID = request.session['provid']
	ordid = request.session['orderid']
	Custid = getAccServReqs(ordid,provID)
	orderservice = getAccOrderServReqs(ordid,provID)
	orderservID = orderservice[0][0].id
	msgs = getMsgs(orderservID)
	if request.method =="POST":
		form = negotiate2Form(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			#insert into database
			print("orderservid is: ",orderservID)
			#custID = orderCust.custid
			print("ok so custid is: ",Custid)
			if Custid is not None:
				SendMessageAcc(Custid,provID,orderservID,cd)
				msgs = getMsgs(orderservID)
				return redirect("provider:negotiate2")

	else:
		form = negotiate2Form()
	return render(request = request,template_name='provider/negotiate2.html',
		context={'form': form, 'user':request.session['provname'],'msgs':msgs})

def CompletedOrder(request):
	provID = request.session['provid']
	ordid = request.session['orderid']
	
	Custid = getAccServReqs(ordid,provID)
	orderservice = getAccOrderServReqs(ordid,provID)
	orderservID = orderservice[0][0].id
	custname = orderservice[0][0].custname
	#insert into database
	#print("customer's name is: ",custname)
	
	if request.method =="POST":
		if "rate" in request.POST:
			print("\n\n\nrating is ")
			rate = int(request.POST['rate'])
			print(rate)
			print("--")
		if "feedback" in request.POST:
			feedback = request.POST['feedback']
		else:
			feedback = ""

		setFeedback(feedback,rate,orderservID,Custid)
		return redirect("provider:profile")

	return render(request = request,template_name='provider/feedback.html',
		context={'user':request.session['provname'], 'custname':custname})

def PastOrders(request):
	trending = getTrendingServices()
	orderservice = getPastOrderReqs(request.session['provid'])
	return render(request = request,template_name='provider/PastOrders.html',
		context= {'trend':trending,'trendlen':len(trending),'user':request.session['provname'],'totalreqs':str(len(orderservice)),
			'orders':orderservice})

def editDP(request):
	print("\nTHe image path now:::\n")
	imgPath = None
	print("\nthe provid is: ",request.session['provid'])
	imgPath = getImgPath(request.session['provid'])
	print("\nThe image path is: ",imgPath)
	provid = request.session['provid']
	provObj = provider.objects.filter(provid=provid)[0]
	prev_path = provObj.provImage.path
	if request.method == 'POST':
		if request.FILES.get('dp'):
			print("\nI came here to change photo\n")
			newdp = request.FILES.get('dp')
			fs = FileSystemStorage()
			filename = fs.save(newdp.name, newdp)
			#uploaded_file_url = fs.url(filename)
			provObj.provImage = filename
			new_path = settings.MEDIA_ROOT + "/providerImage/" + newdp.name
			provObj.path = new_path
			#os.rename(prev_path, new_path)
			provObj.save()
			return redirect("provider:profile")
	return render(request = request,template_name='provider/editphoto.html',
		context={'user':request.session['provname'],'photo' : imgPath})

def deleteProvider(request):
	flag = False
	provid = request.session['provid']
	message = ""
	passmsg=""
	if request.method == 'POST':
		if (request.POST.get('password') is not None) and (len(request.POST.get('password'))>0):
			password = request.POST['password']
			if checkPass(provid,password):
				flag = True
			else:
				passmsg = "Incorrect password"
		else:
			passmsg = "Password is required"

		if (request.POST.get('message') is not None) and (len(request.POST.get('message'))>0):
			if flag:
				msg = request.POST['message']
				deleteAcc(provid,msg)
				del request.session['provid']
				del request.session['provname']
				request.session.modified = True
				return redirect("provider:homepage")
		else:
			message = "This field is required"


	return render(request = request,template_name='provider/deleteProvider.html',
		context={'user':request.session['provname'],'msg':message,'passmsg':passmsg})