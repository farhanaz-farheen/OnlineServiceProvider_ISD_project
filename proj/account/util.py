from .models import *
from provider.models import *
from datetime import datetime
import hashlib
from collections import Counter
from django.db.models import Q
from django.conf import settings
from datetime import datetime, timedelta

globalstat=8

class service_view:
	def __init__(self,id,servname,imgurl):
		self.id = id
		self.imgurl = imgurl
		self.servname = servname		

class category_view:
	def __init__(self,catname,imgurl,services):
		self.catname = catname
		self.imgurl = imgurl
		self.services = services

class order_view:
	def __init__(self):
		self.cost = 0
		self.ordser = []

class ordered_service_view:
	def __init__(self):
		self.provname=""
		self.desc = ""

def getCategoriesWithServices():
	cats = []
	for c in category.objects.all():
		services = [service_view(s.id,s.servname,s.servImage.url) for s in service.objects.filter(catname=c)]
		cats.append(category_view(c.catname,c.catImage.url,services))
	return cats

def hashpass(password):
	h = hashlib.md5(password.encode())
	return h.hexdigest()

def checkPass(custid,password):
	cust = customer.objects.filter(custid=custid)[0]
	passwd = hashpass(password)
	realpass = cust.password
	if passwd==realpass:
		return True
	return False

class form_valid:
	def __init__(self):
		self.logvalid = "True"
		self.regvalid = "True"

def isNewUser(email):
	user = customer.objects.filter(email=email)
	if len(user)==0:
		return True
	return False

class customerView():
	def __init__(self,fn,ln,email,phone):
		self.fn = fn
		self.ln = ln
		self.email = email
		self.phone = phone

def getCustInfo(custid):
	cust = customer.objects.filter(custid=custid)[0]
	ret = customerView(cust.firstname,cust.lastname,cust.email,cust.phone)
	return ret

def doRegister(request, cd):
	if isNewUser(cd['email']):
	    newUser = customer(firstname=cd['firstname'],lastname=cd['lastname'],email=cd['email'],
	    	phone=cd['phone'],password=hashpass(cd['password']))
	    newUser.save()
	    tempUser = customer.objects.filter(firstname=cd['firstname'],lastname=cd['lastname'],email=cd['email'],
	    	phone=cd['phone'],password=hashpass(cd['password']))[0]
	    print(newUser)
	    print(tempUser)
	    newSearch = search_history(custid=tempUser)
	    newSearch.save()
	    request.session['user']=newUser.firstname
	    request.session['custid'] = newUser.custid
	    request.session.modified = True
	    return True
	else:
		return False

def isUser(email,password):
	passwd = hashpass(password)
	user = customer.objects.filter(email=email,password=passwd)
	if len(user)==1:
		return user[0]
	return None

def doLogin(request,cd):
	print("Here in doLogin----",cd)
	loginuser = isUser(cd['email'], cd['password'])
	if loginuser is None:
		return False
	else:
		request.session['user']=loginuser.firstname
		request.session['custid'] = loginuser.custid
		request.session.modified = True
		return True

def editUser(custid,cd):
	user = customer.objects.filter(custid=custid)[0]
	email = cd['email']
	phone = cd['phone']
	if email!='' and isNewUser(email):
		user.email = email
	if cd['password']!='':
		user.password = hashpass(cd['password'])

	if cd['firstname']!='':
		user.firstname = cd['firstname']

	if cd['lastname']!='':
		user.lastname = cd['lastname']

	if (phone is not None) and (phone>=1000000000 and phone<=1999999999):
		user.phone = phone

	user.save()
	return user

class servview:
	def __init__(self,servname):
		self.servname = servname

class search_view:
	
	def __init__(self):
		self.provname = ""
		self.cost = 0
		self.rating = "" 
		self.desc = ""
		self.looking = ""

def spidskey(keywd):
	print(keywd)
	services = service.objects.filter(servname__icontains=keywd)
	spids = service_provider.objects.filter(servid__in=services)
	for r in spids:
		print(r.servid.servname)
	ret = [r.id for r in spids]
	provs = provider.objects.filter(Q(firstname__icontains=keywd) | Q(lastname__icontains=keywd))
	spids_ = service_provider.objects.filter(provid__in=provs)
	for r in spids_:
		if r.id not in ret:
			ret.append(r.id)
	return ret


def searchkey(keywd):
	provs = []
	provfound = []
	servs = []
	services = service.objects.filter(servname__icontains=keywd)

	for sv in services:
		sview = servview(sv.servname)
		sview.imgurl = sv.servImage.url
		sps = service_provider.objects.filter(servid=sv)
		searchObj = []
		for r in sps:
			res = search_view()
			res.id = r.id
			res.cost = r.cost
			if r.ratecount==0:
				res.rating="No rating yet"
			else:
				res.rating=str(r.rating)
			provfound.append(r.provid.provid)
			res.provname = r.provid.firstname+" "+r.provid.lastname
			res.provimg = r.provid.provImage.url
			res.desc = r.desc
			res.service = r.servid.servname
			if r.looking:
				res.looking = "Looking for Work"
			searchObj.append(res)
		sps.sprovs = searchObj.copy()
		servs.append(sview)
	return servs

def insertSearchHistory(custid,cd):
	servHist = search_history.objects.filter(custid = customer.objects.filter(custid=custid)[0])[0]
	cmin = cd['cost_min']
	cmax = cd['cost_max']
	if (cmin is not None) and int(cmin)>0:
		print("ekhane nai")
		if servHist.mincost is None:
			servHist.mincost = str(cmin)
		elif len(servHist.mincost + "_" + str(cmin))>1000:
			startindx = servHist.mincost[300:].find('_')
			servHist.mincost = servHist.mincost[startindx+1:-1]+'_'+str(cmin)
		else:
		 	servHist.mincost = servHist.mincost + "_" + str(cmin)
	if (cmax is not None) and int(cmax)>0:
		if servHist.maxcost is None:
			servHist.maxcost = str(cmax)
		elif len(servHist.maxcost + "_" + str(cmax))>1000:
			startindx = servHist.maxcost[300:].find('_')
			servHist.maxcost = servHist.maxcost[startindx+1:-1]+'_'+str(cmax)
		else:
		 	servHist.maxcost = servHist.maxcost + "_" + str(cmax)
	if cd.get('service'):
		services = cd.get('service')
		servs  = services[0]
		if servHist.services is not None:
			servs = servHist.services + "_" + services[0]
		for s in services[1:]:
			servs = servs + "_" + s
		if len(servs)>1000:
			startindx = servs[300:].find('_')
			servs = servs[startindx+1:-1]
		servHist.services = servs

	if cd.get('provider'):
		provname = cd['provider']
		if servHist.keywd is None:
			servHist.keywd = provname
		elif len(servHist.keywd + "_" + provname)>1000:
			startindx = servHist.keywd[300:].find('_')
			servHist.keywd = servHist.keywd[startindx+1:-1]+'_'+provname
		else:
			servHist.keywd = servHist.keywd + "_" + provname
	servHist.save()

def filterServProv(cd,spids):
	print("\n\n\n")
	print(cd)
	print("\n\n\n")
	provs = []
	servs = []
	cmin=0
	cmax=1000000
	rmin=1
	rmax=5
	if cd.get('cost_min'):
		cmin = int(cd['cost_min'])
	if cd.get('cost_max'):
		cmax = int(cd['cost_max'])

	if cd.get('rating_min'):
		rmin = float(cd['rating_min'])
	if cd.get('rating_max'):
		rmax = float(cd['rating_max'])

	location = None
	if cd.get('district'):
		location = cd['district']

	sps = list(spids)
	ret = []
	for sp_ in sps:
		print("\n\n",sp_,"\n\n")
		sp = service_provider.objects.filter(id=sp_)[0]
		if cd.get('service'):
			services = cd.get('service')
			if sp.servid.servname not in services:
				continue
		if location is not None:
			if (len(location)!=0) and (sp.provid.location!=location):
				continue
		if cd['norating']:
			if (sp.ratecount==0) or (sp.rating>=rmin and sp.rating<=rmax):
				if sp.cost>=cmin and sp.cost<=cmax:
					ret.append(sp.id)

		else:
			print("\n\n\nsefneojfc",rmin,rmax,sp.rating)
			if sp.rating>=rmin and sp.rating<=rmax:
				print("\n\n\nsefneojdddddddddddddddddddfc\n\n\n")
				if sp.cost>=cmin and sp.cost<=cmax:
					print("\n\n\nsefneoooooooooooooooooooooojfc\n\n\n")
					ret.append(sp.id)

	return ret		 

def searchServProv(cd):
	print("\n\n\n")
	print(cd)
	print("\n\n\n")
	provs = []
	servs = []
	cmin=0
	cmax=1000000
	rmin=1
	rmax=5
	if cd.get('cost_min'):
		cmin = cd['cost_min']
	if cd.get('cost_max'):
		cmax = cd['cost_max']

	if cd.get('rating_min'):
		rmin = cd['rating_min']
	if cd.get('rating_max'):
		rmax = cd['rating_max']

	location = None
	if cd.get('district'):
		if len(cd['district'])>0:
			location = cd['district']

	servs = []
	provs = []
	sps = []

	if cd.get('service'):
		servs = service.objects.filter(servname__in=cd.get('service'))

	if cd.get('provider'):
		provname = cd['provider']
		if location is not None:
			provs = provider.objects.filter(Q(Q(firstname__icontains=provname) | Q(lastname__icontains=provname)) & Q(location=location))
		else:
			provs = provider.objects.filter(Q(firstname__icontains=provname) | Q(lastname__icontains=provname))

	if cd['norating']:
		sps = service_provider.objects.filter(Q(Q(servid__in=servs) | Q(provid__in=provs)) & 
			Q(cost__gte=cmin) & Q(cost__lte=cmax) & Q(Q(Q(rating__gte=rmin) & Q(rating__lte=rmax)) | Q(ratecount=0)))
	else:
		print("\n\n\n----------3iucueriocbroc---\n")
		sps = service_provider.objects.filter(Q(Q(servid__in=servs) | Q(provid__in=provs)) & 
			Q(cost__gte=cmin) & Q(cost__lte=cmax) & Q(rating__gte=rmin) & Q(rating__lte=rmax) & Q(ratecount__gt=0))		

	print(sps)
	ret = []

	if location is not None:
		for sp in sps:
			if sp.provid.location==location:
				ret.append(sp.id)
		return ret

	return [sp.id for sp in sps]



def searchResult(results):
	#result = searchServProv(cd)
	result = [service_provider.objects.filter(id=r)[0] for r in results]
	searchObj = []
	for r in result:
		res = search_view()
		res.id = r.id
		res.cost = r.cost
		if r.ratecount==0:
			res.rating="No rating yet"
		else:
			res.rating=str(round(r.rating,2))
		res.provname = r.provid.firstname+" "+r.provid.lastname
		res.provimg = r.provid.provImage.url
		res.desc = r.desc
		res.service = r.servid.servname
		if r.looking:
			res.looking = "Looking for Work"
		searchObj.append(res)
	return searchObj	

"""
def cost_filter(sp,cmin,cmax):
	ret_sp = sp.copy()
	if (cmin is not None) and int(cmin)>=0:
		cost = int(cmin)
		for s_p in sp:
			if s_p.cost < cost:
				ret_sp.remove(s_p)
	if (cmax is not None) and int(cmax)>=0:
		cost = int(cmax)
		for s_p in sp:
			if (s_p.cost > cost) and (s_p in ret_sp):
				ret_sp.remove(s_p)		
	return ret_sp
"""
"""
	searchObj = []
	result = service_provider.objects.all()
	for r in result:
		res = search_view()
		res.id = r.id
		res.cost = r.cost
		if r.ratecount==0:
			res.rating="No rating yet"
		else:
			res.rating=str(r.rating)
		res.provname = r.provid.firstname+" "+r.provid.lastname
		res.desc = r.desc
		res.service = r.servid.servname
		if r.looking:
			res.looking = "Looking for Work"
		searchObj.append(res)
	return searchObj
"""

class feedback_view:
	def __init__(self,custname,feedback):
		self.custname = custname
		self.feedback = feedback

def searchSP(id):
	r = service_provider.objects.filter(id=id)[0]
	res = search_view()
	res.id = r.id
	res.cost = r.cost
	res.ratecount = r.ratecount
	fdbks = []
	if r.ratecount==0:
		res.rating="No rating yet"
	else:
		#res.rating=str(r.rating)
		res.rating = int(r.rating * 100/5)
		os_feed = ordered_service.objects.filter(spid=r,status__in=[2,4])
		for of in os_feed:
			if (of.feedback_prov is not None) and (len(of.feedback_prov)>0):
				custobj = of.orderid.custid
				cn = custobj.firstname + ' ' + custobj.lastname
				fdbks.append(feedback_view(cn,of.feedback_prov))
	if len(fdbks)>0:
		res.totalfeed = "+"
	else:
		res.totalfeed = "0"
	fdbks.reverse()
	res.feedback = fdbks[0:3]
	for fd in fdbks:
		print(fd.custname,fd.feedback)
	res.provname = r.provid.firstname+" "+r.provid.lastname
	res.provimg = r.provid.provImage.url
	res.desc = r.desc
	res.service = r.servid.servname
	if r.looking:
		res.looking = "Looking for Work"

	spimgs = sp_images.objects.filter(spid=r)
	res.images = []
	for img in spimgs:
		res.images.append(img.spImage.url)
	res.totalimages = len(res.images) 
	res.location = r.provid.location
	return res

class cart_view:
	def __init__(self):
		self.provname = ""
		self.servname = ""
		self.cost = 0
		self.desc = ""
		self.id=-1

def getCartObj(spids):
	cartobj = []
	for spid in spids:
		r = service_provider.objects.filter(id=spid)[0]
		res = cart_view()
		res.id = r.id
		res.cost = r.cost
		res.provname = r.provid.firstname+" "+r.provid.lastname
		res.provimg = r.provid.provImage.url
		res.desc = r.desc
		res.service = r.servid.servname
		cartobj.append(res)
	return cartobj


def retServNameImg(spid):
	r = service_provider.objects.filter(id=spid)[0].servid
	return r.servImage.url, r.servname

def getOsFromOsid(osid):
	ordser_obj = ordered_service_view()
	ordser = ordered_service.objects.filter(id = osid)[0]
	ordser_obj.id = ordser.id
	ordser_obj.spid = ordser.spid
	ordser_obj.provname = ordser.spid.provid.firstname + " " + ordser.spid.provid.lastname
	ordser_obj.servname = ordser.spid.servid.servname
	ordser_obj.cost = ordser.cost
	ordser_obj.lat = ordser.lat
	ordser_obj.lon = ordser.lon
	retmap = [ordser_obj.lat,ordser_obj.lon]
	if ordser.desc is not None:
		ordser_obj.desc = ordser.desc
	ordser_obj.deliveryAddress = ordser.deliveryAddress
	ordser_obj.dtime = ordser.expDate
	return ordser_obj,retmap

class msgView:
	def __init__(self,who,time,msgtxt):
		self.who = str(who)
		self.time = time
		self.msgtxt = msgtxt
def messages(inboxid):
	msgs = message.objects.filter(inboxid=inboxid)
	ret = []
	for m in msgs:
		ret.append(msgView(m.who,m.time + timedelta(hours=6),m.msg))
	return ret

def getMsgs(osid):
	os = ordered_service.objects.filter(id=osid)[0]
	inbx = inbox.objects.filter(osid=osid)
	ase = False
	for i in inbx:
		ase=  True
		break
	if ase:
		return messages(inbx[0].id)
	return None

def changeOS(osid,date,time,addr):
	
	osObj = ordered_service.objects.filter(id=osid)[0]
	if len(date)>0:
		dt = datetime.strptime(date, '%Y-%m-%d').date()
	else:
		dt = osObj.expDate.date()
	if len(time)>0:
		tm = datetime.strptime(time, '%H:%M').time()
	else:
		tm = osObj.expDate.time()
	print(dt)
	print(tm)
	osObj.expDate = datetime.combine(dt,tm)
	if len(addr)>0:
		osObj.deliveryAddress = addr
	osObj.save()

def remove_os(osid):
	print("removing ",osid)
	osObj = ordered_service.objects.filter(id=osid)[0]
	if (osObj.status==0) or (osObj.status==1):
		osObj.status = 5
		osObj.save()
		inbox.objects.filter(osid=osid).delete()

def SendMessage(custID,ordservid,msgs):

	Inbox = inbox.objects.filter(osid=ordservid)

	if len(Inbox)>0:
		inboxID = Inbox[0]
		newMsg = message(inboxid=inboxID,msg=msgs,who=0)
		newMsg.save()
	else:
		custid = customer.objects.filter(custid=custID)[0]
		osid = ordered_service.objects.filter(id = ordservid)[0]
		provid = osid.spid.provid

		newInbox = inbox(custid=custid,provid=provid,osid=osid,who=0)
		newInbox.save()

		OldInboxID = inbox.objects.filter(osid=ordservid)[0]
		newmsg = message(inboxid=OldInboxID,msg=msgs,who=0)
		newmsg.save()

'''
def confirm_os(osid,rating,feedback):
	print("confirming..")
	print(osid)
	osObj = ordered_service.objects.filter(id=osid)[0]
	#osObj.rating_cust = rating
	osObj.rating_prov = rating
	if len(feedback)>0:
		osObj.feedback_prov = feedback
	osObj.status = 8
	prevrating = osObj.spid.rating
	prevrc = osObj.spid.ratecount
	osObj.spid.ratecount = prevrc+1
	osObj.spid.rating = (prevrating*prevrc + rating)/(prevrc+1)
	osObj.spid.save()
	osObj.save()
'''

def showRecommends(custid):
	searchHist = search_history.objects.filter(custid=customer.objects.filter(custid = custid)[0])[0]
	mincosts = []
	maxcosts = []
	services = []
	keywds = []
	if searchHist.mincost is not None:
		mincosts = Counter(searchHist.mincost.split('_')).most_common()
	if searchHist.maxcost is not None:
		maxcosts = Counter(searchHist.maxcost.split('_')).most_common()
	if searchHist.services is not None:
		services = Counter(searchHist.services.split('_')).most_common()
	if searchHist.keywd is not None:
		keywds = Counter(searchHist.keywd.split('_')).most_common()
	print(mincosts)
	print(maxcosts)
	print(services)
	print(keywds)
	rangemin = None
	if len(mincosts)>0:
		if len(mincosts)==1:
			rangemin = mincosts[0][0]
		notalleq = False
		prev = mincosts[0][1]
		for i in mincosts[1:]:
			if i[1]!=prev:
				notalleq = True
				break
			prev = i[1]
		if notalleq:
			rangemin = mincosts[0][0]

	rangemax = None
	if len(maxcosts)>0:
		if len(maxcosts)==1:
			rangemax = maxcosts[0][0]
		notalleq = False
		prev = maxcosts[0][1]
		for i in maxcosts[1:]:
			if i[1]!=prev:
				notalleq = True
				break
			prev = i[1]
		if notalleq:
			rangemax = maxcosts[0][0]

	serviceName = None
	if len(services)>0:
		if len(services)==1:
			serviceName = services[0][0]
		notalleq = False
		prev = services[0][1]
		for i in services[1:]:
			if i[1]!=prev:
				notalleq = True
				break
			prev = i[1]
		if notalleq:
			serviceName = services[0][0]
	keyWord = None
	if len(keywds)>0:
		if len(keywds)==1:
			keyWord = keywds[0][0]
		notalleq = False
		prev = keywds[0][1]
		for i in keywds[1:]:
			if i[1]!=prev:
				notalleq = True
				break
			prev = i[1]
		if notalleq:
			keyWord = keywds[0][0]


	print(rangemin,rangemax,serviceName,keyWord)


	commonProviders = None
	commonServices = None
	commonrange = None
	common4 = None

	if keyWord is not None:
		commonProviders = provider.objects.filter(Q(firstname__icontains=keyWord) | Q(lastname__icontains=keyWord))
		print("-----------keyWord--------")
		print(commonProviders)

	if serviceName is not None:
		commonServices = service.objects.filter(servname__icontains=serviceName)		
		
		#print(commonServices)

	if (rangemin is not None) and (rangemax is not None):
		commonrange = service_provider.objects.filter(cost__gt=int(rangemin),cost__lt=int(rangemax))		
		
		if (commonProviders is not None) and (commonServices is not None):
			common4 = service_provider.objects.filter(cost__gt=int(rangemin),cost__lt=int(rangemax),provid__in=commonProviders,servid__in=commonServices)		
			print(common4)
	'''
	if rangemax is not None:
		commonMax = service_provider.objects.filter(cost__lt=rangemax)		
		print(commonMax)
	'''
	return commonProviders, commonServices, commonrange, common4


def recommendFromOrder(custid):
	orders = order.objects.filter(custid=customer.objects.filter(custid=custid)[0])
	spids = []
	addedids = []
	for orderObj in orders:
		
		#spids.append(sp.spid for sp in ordered_service.objects.filter(orderid=orderObj))
		for sp in ordered_service.objects.filter(orderid=orderObj):
			if sp.spid.id not in addedids:
				spids.append(sp.spid)
				addedids.append(sp.spid.id)
	print(addedids)
	print(spids)
	return spids
	allservs = Counter(spids).most_common()
	rangemax = None
	if len(allservs)>0:
		notalleq = False
		prev = allservs[0][1]
		for i in allservs[1:]:
			if i[1]!=prev:
				notalleq = True
				break
			prev = i[1]
		if notalleq:
			rangemax = allservs[0][0]	
	print(rangemax)
	return rangemax 	

class recommendView:
	def __init__(self,spid,provname,servname,imgurl):
		self.id = spid
		self.provname=  provname
		self.servname= servname
		self.url = imgurl

def getOrderRecommendation(recOrders):
	orderObjs = []
	if recOrders is not None:
		for ro in recOrders:
			recOrder = recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url)
			orderObjs.append(recOrder)
	return orderObjs

def getCommonRecommendation(common):
	if common is None:
		return []
	com = []
	for ro in common:
		com.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
	return com

def getRangeRecommendation(commonrange):
	if commonrange is None:
		return []
	com = []
	for ro in commonrange:
		com.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
	return com

def getProvidersRecommendation(commonProviders):
	if commonProviders is None:
		return []
	com = []
	csp = service_provider.objects.filter(provid__in=commonProviders)
	for ro in csp:
		com.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))

	return com

def getServicesRecommendation(commonServices):
	if commonServices is None:
		return []
	com = []
	csp = service_provider.objects.filter(servid__in=commonServices)
	for ro in csp:
		com.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
	return com	

def allRecommendations(custid):
	recOrder = getOrderRecommendation(recommendFromOrder(custid))
	commonProviders, commonServices, commonrange, common4 = showRecommends(custid)
	recCommon = getCommonRecommendation(common4)
	recRange = getRangeRecommendation(commonrange)
	recProvider = getProvidersRecommendation(commonProviders)
	recService = getServicesRecommendation(commonServices)
	ret=[recOrder,recCommon,recRange,recProvider,recService]
	atleastOne = 0
	for r in ret:
		if len(r)>0:
			atleastOne = 1
			break
	return atleastOne, ret

def getTrendingServices():
	sps = service_provider.objects.filter(ratecount__gt=0).order_by('-rating')
	trending = [recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url) for ro in sps][0:5]
	print(trending)
	return trending

def getProvnameForRating(osid):
	osobj = ordered_service.objects.filter(id=osid)[0]
	prov = osobj.spid.provid
	provname = prov.firstname + ' ' + prov.lastname
	return provname

def deleteAcc(custid,msg):
	print(msg)
	custobj = customer.objects.filter(custid=custid)[0]
	firstname = custobj.firstname
	lastname = custobj.lastname
	email = custobj.email
	phone = custobj.phone
	obj = deletedcustomer(firstname=firstname,lastname=lastname,email=email,phone=phone,msg=msg)
	obj.save()
	customer.objects.filter(custid=custid).delete()
