from django.shortcuts import render, redirect
from .forms import *
from .util import *
from .order import *
import json

def login(request):
	valid= "True"
	if request.method =="POST":
	    form = loginForm(request.POST)
	    if form.is_valid():
	    	check = doLogin(request,form.cleaned_data)
	    	if check:
	    		#print("Logging--",request.session['custid'],request.session['user'])
	    		return redirect("account:profile")
	    	else:
	    		valid = "False"
	else:
		form = loginForm()
		if 'valid' in request.GET:
			valid = "True"
	return render(request = request,template_name='account/login.html',
		context={'form': form, 'valid':valid ,'user':"None"})

def register(request):
	valid= "True"
	if request.method =="POST":
	    form = registerForm(request.POST)
	    if form.is_valid():
	        cd = form.cleaned_data
	        check = doRegister(request,form.cleaned_data)
	        if check:
	        	return redirect("account:profile")
	        else:
	        	valid = "False"
	else:
		form = registerForm()
		if 'valid' in request.GET:
			valid = "True"
	return render(request = request,template_name='account/register.html',
		context={'form': form, 'valid': valid})

def homepage(request):
	if request.method =="POST":
		if "barsearch" in request.POST:
			searchkey=request.POST['barsearch']
			request.session['search_spids'] = spidskey(searchkey)
			request.session.modified = True
			return redirect("account:showSearch")
	return render(request = request,template_name='account/homepage.html',
			context={'cats':getCategoriesWithServices()})


def searchInput(request):
	if request.session.get('user') is not None:
		user_ = request.session['user']
		cart, cartobjs, totalPending, totalAccepted, totalPast = getOrderStats(request.session.get('custid'),request)
	else:
		user_ = "None"
	if request.method =="POST":
		searchform = searchForm(request.POST)
		if searchform.is_valid():
			cd = searchform.cleaned_data
			if request.session.get('custid') is not None:
				insertSearchHistory(request.session.get('custid'),cd)
			searchRes = searchServProv(cd)
			request.session['search_spids'] = searchRes
			request.session['recommendFlag'] = False
			request.session.modified = True
			return redirect("account:showSearch")
		return redirect("account:searchInput")
	else:
		searchform = searchForm()
	return render(request = request,template_name='account/searchInput.html',
		context={'form':searchform,'user':user_})	

def showSearch(request):
	if request.session.get('user') is not None:
		user_ = request.session['user']
		cart, cartobjs, totalPending, totalAccepted, totalPast = getOrderStats(request.session.get('custid'),request)
	else:
		user_ = "None"
	searchRes = searchResult(request.session['search_spids'])
	if len(searchRes)==0:
		total = "0"
	else:
		total = "+"
	if request.method=="POST":
		searchform = filterForm(request.POST)
		if 'detail' in request.POST:
			request.session['spid'] = int(request.POST['detail'])
			request.session['recommendFlag'] = False
			request.session['modified'] = True
			return redirect("account:searchDetail")
		if searchform.is_valid():
			cd = searchform.cleaned_data
			searchRes = filterServProv(cd,request.session['search_spids'])
			request.session['search_spids'] = searchRes
			request.session['recommendFlag'] = False
			request.session.modified = True
			return redirect("account:showSearch")
	else:
		searchform = filterForm()
	if user_=="None":
		return render(request = request,template_name='account/searchHome.html',
			context= {'total':total,'sp':searchRes,'form':searchform})		
	return render(request = request,template_name='account/search.html',
		context= {'form':searchform,'user':user_,'total':total,'sp':searchRes,
		'cart':cart,'cartobjs':cartobjs,'totalPending':totalPending,
		'totalAccepted':totalAccepted,'totalPast':totalPast})

def profile(request):
	custid = request.session['custid']
	atleastOne,recValues = allRecommendations(custid)
	
	cart, cartobjs, totalPending, totalAccepted, totalPast = getOrderStats(custid,request)

	if request.method =="POST":
	    searchform = searchForm(request.POST)
	    if "barsearch" in request.POST:
	    	searchkey = request.POST['barsearch']
	    	request.session['search_spids'] = spidskey(searchkey)
	    	request.session['recommendFlag'] = False
	    	request.session.modified = True
	    	return redirect("account:showSearch")
	    if ('search' in request.POST) and searchform.is_valid():
	    	searchRes = searchServProv(searchform.cleaned_data)
	    	request.session['search_spids'] = [s.id for s in searchRes]
	    	request.session.modified = True
	    	return redirect("account:showSearch")
	else:
		searchform = searchForm()
	return render(request = request,template_name='account/profile.html',
		context= {'user':request.session['user'],'searchform':searchForm,
		'cart':cart,'cartobjs':cartobjs,'totalPending':totalPending,
		'totalAccepted':totalAccepted,'totalPast':totalPast,
		'CategoryServices':getCategoriesWithServices(),
		'recflag':atleastOne,
		'ordrec':recValues[0],'ordrectotal':len(recValues[0]),
		'comrec':recValues[1],'comrectotal':len(recValues[1]),
		'rangerec':recValues[2],'rangerectotal':len(recValues[2]),
		'provrec':recValues[3],'provrectotal':len(recValues[3]),
		'servrec':recValues[4],'servrectotal':len(recValues[4])})

def logout(request):
	#print(request.session['user'])
	del request.session['user']
	del request.session['custid']
	if request.session.get('cartadd'):
		del request.session['cartadd']
	request.session.modified = True
	return redirect("account:homepage")

def editcustomerprof(request):
	custid = request.session.get('custid')
	cart, cartobjs, totalPending, totalAccepted, totalPast = getOrderStats(custid,request)
	if request.method =="POST":
		form = EditCustomerForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user= editUser(request.session['custid'],cd)
			request.session['user']= user.firstname
			request.session['custid'] = user.custid
			request.session.modified = True
			return redirect("account:profile")

	else:
		form = EditCustomerForm()
	return render(request = request,template_name='account/custedit.html',
		context={'form': form, 'user':request.session['user'],'val':getCustInfo(custid),
				'cart':cart,'cartobjs':cartobjs,'totalPending':totalPending,
				'totalAccepted':totalAccepted,'totalPast':totalPast})

def searchDetail(request,spid):
	request.session['spid'] = spid
	request.session.modified = True
	pending =[]
	if request.session.get('custid'):
		cart, cartobjs, totalPending, totalAccepted, totalPast = getOrderStats(request.session.get('custid'),request)
	if request.session.get('user'):
		user = request.session['user']
	else:
		user = "None"
	valid= form_valid()
	if request.method =="POST":
	    searchform = searchForm(request.POST)
	    if ('search' in request.POST) and searchform.is_valid():
	    	searchRes = searchServProv(searchform.cleaned_data)
	    	request.session['search_spids'] = [s.id for s in searchRes]
	    	request.session.modified = True
	    	return redirect("account:showSearch")
	else:
		searchform = searchForm()
	servimg,servicename = retServNameImg(spid)
	if user=="None":
		return render(request = request,template_name='account/searchDetailHome.html',
		context={'user':user,'servimg':servimg,'servname':servicename,
		'val':searchSP(spid)})		
	else:
		return render(request = request,template_name='account/searchDetail.html',
		context={'user':user,'servimg':servimg,'servname':servicename,
		'val':searchSP(spid),'cart':cart,'cartobjs':cartobjs,'totalPending':totalPending,
		'totalAccepted':totalAccepted,'totalPast':totalPast})

def addtocart(request):

	if request.session.get('cartadd'):
		if request.session['spid'] not in request.session['cartadd']:
			request.session['cartadd'].append(request.session['spid'])
			del request.session['spid']
			if request.session.get('recommendFlag') is not None:
				if request.session['recommendFlag']:
					del request.session['recommendFlag']
					request.session.modified = True
					return redirect("account:recommend")
				else:
					del request.session['recommendFlag']
					request.session.modified = True
					return redirect("account:showSearch")					
	else:
		request.session['cartadd'] = [request.session['spid']]
		del request.session['spid']
		if request.session.get('recommendFlag') is not None:
			if request.session['recommendFlag']:
				del request.session['recommendFlag']
				request.session.modified = True
				return redirect("account:recommend")
			else:
				del request.session['recommendFlag']
				request.session.modified = True
				return redirect("account:showSearch")

	return redirect('account:showSearch')


def finishcart(request):
	print("cart is.. ",request.session['cartadd'])
	cartlist = getCartObj(request.session['cartadd'])
	custid = request.session['custid']
	cart, cartobjs, totalPending, totalAccepted, totalPast = getOrderStats(custid,request)
	if request.session.get('cartadd'):
		cart = str(len(request.session['cartadd']))
		cartobjs = getCartObj(request.session['cartadd'])
	else:
		cart = "None"
		cartobjs = None
	
	if request.method =="POST":
		form = cartForm(request.POST,total=len(cartlist))
		print(form.errors)
		if form.is_valid():
			cd = form.cleaned_data
			print(cd)
			if "getbtn" in request.POST :
				loc = request.POST['getbtn']
			print(loc)	
			insertOrder(custid,cartlist,cd,loc)
			del request.session['cartadd']
			return redirect('account:profile')
	else:
		form = cartForm(total=len(cartlist))
	return render(request = request,template_name='account/cartlist.html',
		context={'form': form, 'user':request.session['user'],
		'value':cartlist,'cart':cart,'cartobjs':cartobjs,'total':len(cartlist),
		'totalPending':totalPending,'totalAccepted':totalAccepted,'totalPast':totalPast
		})		

def pending_order(request):
	if request.session.get('user'):
		user = request.session['user']
	else:
		user = "None"
	custid = request.session['custid']
	pending,latlon = PendingOrders(custid)
	print(latlon)
	cart, cartobjs, totalPending, totalAccepted, totalPast = getOrderStats(custid,request)
	
	if request.method =="POST":
		form = homeForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			opt = cd['btn']
			if "cancel" in opt:
				cancel_osid = int(opt[opt.find("_")+1:])
				remove_os(cancel_osid)
				pending,latlon = PendingOrders(request.session['custid'])
			elif "edit" in opt:
				edit_osid = opt[opt.find("_")+1:]
				request.session['edit_osid'] = edit_osid
				request.session.modified = True
				return redirect("account:edit_ordered_service")
	else:
		form = homeForm()

	return render(request = request,template_name='account/pending_order.html',
		context={'form': form, 'user':user,'value':pending,
		'll':json.dumps(latlon),'cart':cart,'cartobjs':cartobjs,'totalPending':totalPending,
		'totalAccepted':totalAccepted,'totalPast':totalPast})

def edit_ordered_service(request):
	custid = request.session['custid']
	cart, cartobjs, totalPending, totalAccepted, totalPast = getOrderStats(custid,request)
	if request.session.get('user'):
		user = request.session['user']
	else:
		user = "None"
	osid =request.session['edit_osid']
	val,loc = getOsFromOsid(osid)
	msgs = getMsgs(osid)
	print(msgs)
	if msgs is None:
		totalmsg = "0"
	else:
		totalmsg = "+"
	#editosForm
	if request.method == "POST":
		#form = editosForm(request.POST)
		if "sendbtn" in request.POST:
			print(request.POST['sentmsg'])
			SendMessage(custid,osid,request.POST['sentmsg'])
			msgs = getMsgs(osid)
		else:
			changeOS(osid,request.POST['expDate'],request.POST['expTime'],request.POST['deliveryAddress'])
		return redirect('account:edit_ordered_service')	
	#else:
	#	form = editosForm()
	return render(request = request,template_name='account/edit_os.html',
		context={'os':val,'lat':loc[0],'lon':loc[1],'user':user,
					'totalmsg':totalmsg, 'msgs':msgs,
					'cart':cart,'cartobjs':cartobjs,'totalPending':totalPending,
					'totalAccepted':totalAccepted,'totalPast':totalPast
					})

def serviceDisplay(request,service):
	print(service)

def accepted_order(request):
	if request.session.get('user'):
		user = request.session['user']
	else:
		user = "None"
	custid = request.session['custid']
	pending,latlon = AcceptedOrders(custid)
	print(latlon)
	cart, cartobjs, totalPending, totalAccepted, totalPast = getOrderStats(custid,request)
	
	if request.method =="POST":
		form = homeForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			opt = cd['btn']
			if "cancel" in opt:
				cancel_osid = int(opt[opt.find("_")+1:])
				remove_os(cancel_osid)
				pending,latlon = AcceptedOrders(request.session['custid'])
			elif "accept" in opt:
				confirm_osid = int(opt[opt.find("_")+1:])
				request.session['confirm_osid'] = confirm_osid
				request.session.modified = True
				return redirect("account:ratefeed")

			elif "edit" in opt:
				edit_osid = opt[opt.find("_")+1:]
				request.session['edit_osid'] = edit_osid
				request.session.modified = True
				return redirect("account:edit_accepted_service")
	else:
		form = homeForm()

	return render(request = request,template_name='account/accepted_order.html',
		context={'form': form, 'user':user,'value':pending,
		'll':json.dumps(latlon),'cart':cart,'cartobjs':cartobjs,'totalPending':totalPending,
		'totalAccepted':totalAccepted,'totalPast':totalPast})

def edit_accepted_service(request):
	if request.session.get('user'):
		user = request.session['user']
	custid = request.session['custid']
	cart, cartobjs, totalPending, totalAccepted, totalPast = getOrderStats(custid,request)
	osid =request.session['edit_osid']
	val,loc = getOsFromOsid(osid)
	msgs = getMsgs(osid)
	print(msgs)
	if msgs is None:
		totalmsg = "0"
	else:
		totalmsg = "+"
	#editosForm
	if request.method == "POST":
		#form = editosForm(request.POST)
		if "sendbtn" in request.POST:
			print(request.POST['sentmsg'])
			SendMessage(custid,osid,request.POST['sentmsg'])
			msgs = getMsgs(osid)
		else:
			changeOS(osid,request.POST['expDate'],request.POST['expTime'],request.POST['deliveryAddress'])
		return redirect("account:edit_accepted_service")	
	#else:
	#	form = editosForm()
	return render(request = request,template_name='account/edit_acc_os.html',
		context={'os':val,'lat':loc[0],'lon':loc[1],'user':user,
		'totalmsg':totalmsg, 'msgs':msgs,'cart':cart,'cartobjs':cartobjs,'totalPending':totalPending,
		'totalAccepted':totalAccepted,'totalPast':totalPast})


def ratefeed(request):
	custid = request.session['custid']
	user = request.session['user']
	osid =request.session['confirm_osid']
	provname = provider
	cart, cartobjs, totalPending, totalAccepted, totalPast = getOrderStats(custid,request)
	if request.method=="POST":

		if "rate" in request.POST:
			print("\n\n\nrating is ")
			rating = int(request.POST['rate'])
			print(rating)
			print("--")
		if "feedback" in request.POST:
			feedback = request.POST['feedback']
		else:
			feedback = ""
		confirm_os(osid,rating,feedback)
		return redirect("account:profile")
	return render(request = request,template_name='account/ratefeed.html',
		context={'user':user,'name':getProvnameForRating(osid),
		'cart':cart,'cartobjs':cartobjs,'totalPending':totalPending,
		'totalAccepted':totalAccepted,'totalPast':totalPast})


def recommend(request):
	custid = request.session['custid']
	cart, cartobjs, totalPending, totalAccepted, totalPast = getOrderStats(custid,request)
	commonProviders, commonServices, commonrange, common4 = showRecommends(custid)
	recOrders = recommendFromOrder(custid)
	orderObjs = getOrderRecommendation(recOrders)
	commonrec = getCommonRecommendation(common4)
	rangerec = getRangeRecommendation(commonrange)
	provrec = getProvidersRecommendation(commonProviders)
	servrec = getServicesRecommendation(commonServices)
	trending=getTrendingServices()
	request.session['recommendFlag'] = True
	request.session.modified = True
	if request.method=="POST":

		if "spid" in request.POST:
			print("details for ---------",request.POST['spid'])
			request.session['spid'] = int(request.POST['spid'])
			request.session.modified = True
			return redirect('account:searchDetail')
	return render(request = request,template_name='account/recommend.html',
		context={'user':request.session['user'],
				'orders':orderObjs,'ordlen':len(orderObjs),
				'common':commonrec,'comlen':len(commonrec),
				'range':rangerec,'rangelen':len(rangerec),
				'prov':provrec,'provlen':len(provrec),
				'serv':servrec,'servlen':len(servrec),
				'trend':trending,'trendlen':len(trending),
				'cart':cart,'cartobjs':cartobjs,'totalPending':totalPending,
				'totalAccepted':totalAccepted,'totalPast':totalPast})

def PastOrders(request):
	custid = request.session['custid']
	trending=getTrendingServices()
	orderservice = getPastOrderReqs(custid)
	cart, cartobjs, totalPending, totalAccepted, totalPast = getOrderStats(custid,request)
	return render(request = request,template_name='account/PastOrders.html',
		context= {'user':request.session['user'],'totalreqs':str(len(orderservice)),
			'orders':orderservice,'trend':trending,'trendlen':len(trending),
			'cart':cart,'cartobjs':cartobjs,'totalPending':totalPending,
			'totalAccepted':totalAccepted,'totalPast':totalPast})


def deleteCustomers(request):
	flag = False
	custid = request.session['custid']
	cart, cartobjs, totalPending, totalAccepted, totalPast = getOrderStats(custid,request)
	message = ""
	passmsg=""
	if request.method == 'POST':
		if (request.POST.get('password') is not None) and (len(request.POST.get('password'))>0):
			password = request.POST['password']
			if checkPass(custid,password):
				flag = True
			else:
				passmsg = "Incorrect password"
		else:
			passmsg = "Password is required"

		if (request.POST.get('message') is not None) and (len(request.POST.get('message'))>0):
			if flag:
				msg = request.POST['message']
				deleteAcc(custid,msg)
				del request.session['custid']
				del request.session['user']
				request.session.modified = True
				return redirect("account:homepage")
		else:
			message = "This field is required"


	return render(request = request,template_name='account/deleteCustomer.html',
		context={'user':request.session['user'],'msg':message,'passmsg':passmsg,
		'cart':cart,'cartobjs':cartobjs,'totalPending':totalPending,
		'totalAccepted':totalAccepted,'totalPast':totalPast})