from .models import *
from account.models import order, ordered_service,customer
from admins.models import allowed_services
from datetime import datetime, timedelta

def isNewUser(email):
	user = provider.objects.filter(email=email)
	if len(user)==0:
		user = requested_provider.objects.filter(email=email)
		if len(user)==0:
			return True
	return False

def isUser(email,password):
	user = provider.objects.filter(email=email,password=password)
	if len(user)==1:
		return user[0],True
	else:
		user = requested_provider.objects.filter(email=email,password=password)
		if len(user)==1:
			return user[0],False
	return None,None

def getProviderForSetup(provid):
	prov = provider.objects.filter(provid=provid)[0]
	name = prov.firstname + ' ' + prov.lastname
	email = prov.email
	phone = prov.phone
	desc = prov.desc
	return name,email,phone,desc


def getAllowedServices(provid):
	provid = provider.objects.filter(provid=provid)[0]
	ret = []
	als = allowed_services.objects.filter(provider=provid)
	ret = [a.service for a in als]
	return ret

def setupProv(provid,cd,total):
	provid = provider.objects.filter(provid=provid)[0]
	for i in range(1,total+1):
		cost = int(cd['cost_'+str(i)])
		desc = cd['desc_'+str(i)]
		servid = service.objects.filter(servname=cd['service_'+str(i)])[0]
		newsp = service_provider(servid=servid,provid=provid,cost=cost,desc=desc)
		newsp.save()
	allowed_services.objects.filter(provider=provid).delete()


def getCategories():
	#print(type(category.objects.all()))
	return [i.catname for i in category.objects.all()]

def getServices(catname=None):
	return tuple([(i,i.servname) for i in service.objects.filter(catname=catname)])

def getCatname(reqprovid):
	return requested_provider.objects.filter(id=reqprovid)[0].catname

class orders:
	def __init__(self,id,name,time_order,customid,cost):
		self.id = id
		self.name = name
		self.time_order = time_order
		self.customid = customid
		self.cost = cost

def totalOrderReqs(provid):

	return order.objects.all().count()

def getOrderReqs(provid):
	ret = []
	"""
	for i in order.objects.all():

		tempname = customer.objects.filter(custid=i.custid)[0].firstname + " " + customer.objects.filter(custid = i.custid)[0].lastname
		tempid = customer.objects.filter(custid=i.custid)[0].custid
		
		print("Name is.. ",tempname)
		ret.append(orders(i.id,tempname,i.time_order,tempid,i.cost))
	return ret
	"""
	sp = service_provider.objects.filter(provid = provider.objects.filter(provid=provid)[0])
	os = ordered_service.objects.filter(spid__in=sp,status=0)
	#os = [oserv for oserv in ordered_service.objects.filter(spid__in=sp,status=0)]
	order_ = [o_s.orderid for o_s in os]

	for ordr in order_:
		cust = ordr.custid
		tempname = cust.firstname + " " + cust.lastname
		tempid = cust.custid
		#print("id is.. ",ordr.id)
		ret.append(orders(ordr.id,tempname,ordr.time_order+timedelta(hours=6),tempid,ordr.cost))
	return ret

def getAccOrderReqs(provid):
	ret = []
	"""
	for i in order.objects.all():

		tempname = customer.objects.filter(custid=i.custid)[0].firstname + " " + customer.objects.filter(custid = i.custid)[0].lastname
		tempid = customer.objects.filter(custid=i.custid)[0].custid
		
		print("Name is.. ",tempname)
		ret.append(orders(i.id,tempname,i.time_order,tempid,i.cost))
	return ret
	"""
	sp = service_provider.objects.filter(provid = provider.objects.filter(provid=provid)[0])
	os = ordered_service.objects.filter(spid__in=sp,status__in=[1,2])
	#os = [oserv for oserv in ordered_service.objects.filter(spid__in=sp,status=0)]
	order_ = [o_s.orderid for o_s in os]

	for ordr in order_:
		cust = ordr.custid
		tempname = cust.firstname + " " + cust.lastname
		tempid = cust.custid
		#print("id is.. ",ordr.id)
		ret.append(orders(ordr.id,tempname,ordr.time_order+timedelta(hours=6),tempid,ordr.cost))
	return ret

class orderservice:
	def __init__(self,id,custname,serv,cost,custrating,time_order,address):
		self.id = id
		self.serv = serv
		self.custname = custname
		self.cost = cost
		self.time_order = time_order
		self.address = address;
		self.custrating = custrating
			

def totalOrderservReqs(orderid):
	numOrders = ordered_service.objects.filter(orderid_id = orderid).all().count()
	
	return numOrders	
	#return ordered_service.objects.all().count()

def getOrderServReqs(ordid,provid):
	ret = []
	retmap = {}
	for i in ordered_service.objects.all():
		if (i.orderid_id == ordid) and (i.spid.provid.provid == provid) and (i.status == 0):
			#tempname = customer.objects.filter(custid=i.id)[0].firstname + " " + customer.objects.filter(custid = i.id)[0].lastname
			reqtime = order.objects.filter(id=i.orderid_id)[0].time_order
			servid = service_provider.objects.filter(id = i.spid_id)[0].servid_id
			serv = service.objects.filter(id = servid)[0].servname


			custID = order.objects.filter(id = ordid)[0].custid_id
			custname = customer.objects.filter(custid = custID)[0].firstname + " " + customer.objects.filter(custid = custID)[0].lastname
			#print("Name is.. ",tempname)
			custrate = customer.objects.filter(custid = custID)[0].rating*20
			ret.append(orderservice(i.id,custname,serv,i.cost,int(custrate),reqtime+timedelta(hours=6),i.deliveryAddress))
			retmap[i.id] = [i.lat,i.lon]
	return ret, retmap


def getAccOrderServReqs(ordid,provid):
	ret = []
	retmap = {}
	for i in ordered_service.objects.all():
		if (i.orderid_id == ordid) and (i.spid.provid.provid == provid) and ((i.status == 1) or (i.status == 2)):
			#tempname = customer.objects.filter(custid=i.id)[0].firstname + " " + customer.objects.filter(custid = i.id)[0].lastname
			
			servid = service_provider.objects.filter(id = i.spid_id)[0].servid_id
			serv = service.objects.filter(id = servid)[0].servname
			reqtime = order.objects.filter(id=i.orderid_id)[0].time_order
			

			custID = order.objects.filter(id = ordid)[0].custid_id
			custname = customer.objects.filter(custid = custID)[0].firstname + " " + customer.objects.filter(custid = custID)[0].lastname
			#print("Name is.. ",tempname)
			custrate = customer.objects.filter(custid = custID)[0].rating*20
			ret.append(orderservice(i.id,custname,serv,i.cost,int(custrate),reqtime+timedelta(hours=6),i.deliveryAddress))
			retmap[i.id] = [i.lat,i.lon]
	return ret, retmap

def getServicesProvided(provid):
	ret = []
	for i in service_provider.objects.all():
		print("CAME HERE")
		print("provid is ",provid," ",i.provid.provid)
		if i.provid.provid == provid:
			print("CAME HERE")
			#tempname = customer.objects.filter(custid=i.id)[0].firstname + " " + customer.objects.filter(custid = i.id)[0].lastname
			serv = service.objects.filter(id = i.servid_id)[0].servname

			ret.append(serv)
	return ret	






#edited


class orderCust:
	def __init__(self,id,custid):
		self.id = id
		self.custid = custid



def getServReqs(ordid,provid):
	ret = []
	for i in ordered_service.objects.all():
		if (i.orderid_id == ordid) and (i.spid.provid.provid == provid) and (i.status == 0):


			custID = order.objects.filter(id = ordid)[0].custid_id
			print("the custid is: ",custID)
			#custname = customer.objects.filter(custid = custID)[0].firstname + " " + customer.objects.filter(custid = custID)[0].lastname
			#print("Name is.. ",tempname)
			return custID
	return None

def getAccServReqs(ordid,provid):
	ret = []
	for i in ordered_service.objects.all():
		if (i.orderid_id == ordid) and (i.spid.provid.provid == provid) and ((i.status == 1) or (i.status == 2)):


			custID = order.objects.filter(id = ordid)[0].custid_id
			print("the custid is: ",custID)
			#custname = customer.objects.filter(custid = custID)[0].firstname + " " + customer.objects.filter(custid = custID)[0].lastname
			#print("Name is.. ",tempname)
			return custID
	return None




def editUser(provid,cd):
	user = provider.objects.filter(provid=provid)[0]
	email = cd['email']
	phone = cd['phone']
	if email!='' and isNewUser(email):
		user.email = email
	if cd['password']!='':
		user.password = cd['password']

	if cd['firstname']!='':
		user.firstname = cd['firstname']

	if cd['lastname']!='':
		user.lastname = cd['lastname']

	if (phone is not None) and (phone>=1000000000 and phone<=1999999999):
		user.phone = phone

	if cd['desc']!='':
		user.desc = cd['desc']
	#condition of location
	if cd['location']!='':
		user.location = cd['location']

	user.save()
	return user

def editCost(provid,cd):
	print(cd)
	ServObj = service.objects.filter(servname = cd['servname'])[0]
	ProvObj = provider.objects.filter(provid = provid)[0]

	spid = service_provider.objects.filter(servid = ServObj,provid = ProvObj)[0]
	cost = 0
	if cd['cost']:
		cost = int(cd['cost'])
	if cost >0:
		spid.cost = cd['cost']
	spid.save()
	
	if cd['desc']:
		desc = cd['desc']
		spid.desc = desc
	spid.save()

	stat = 2;

	if cd['looking']:
		looking = cd['looking']
		print("~~~~~~~~~!!!!!!!!!!!!!!!_______________")
		print(looking)

		if looking == "available":
			stat = 1;
		else:
			if looking == "busy":
				stat = 0;

	if stat!=2:
		spid.looking = stat
		spid.save()

		
def SendMessage(custID,provID,ordservid,cd):
	print("\nCame here\n",custID," ",provID)
	msgs = cd['message']
	cost = cd['cost']

	print("the message and cost are: ",msgs," ",cost)


	#edit cost

	osID = ordered_service.objects.filter(id = ordservid)[0]
	
	if cost is not None:
		if cost >0:
			osID.cost = cost
		osID.save()


	Inbox = inbox.objects.filter(osid=ordservid)

	if len(Inbox)>0:
		inboxID = Inbox[0]
		newMsg = message(inboxid=inboxID,msg=msgs)
		newMsg.save()
	else:
		custid = customer.objects.filter(custid=custID)[0]
		provid = provider.objects.filter(provid = provID)[0]
		osid = ordered_service.objects.filter(id = ordservid)[0]

		newInbox = inbox(custid=custid,provid=provid,osid=osid)
		newInbox.save()

		OldInboxID = inbox.objects.filter(osid=ordservid)[0]
		newmsg = message(inboxid=OldInboxID,msg=msgs)
		newmsg.save()


def SendMessageAcc(custID,provID,ordservid,cd):
	print("\nCame here\n",custID," ",provID)
	msgs = cd['message']


	Inbox = inbox.objects.filter(osid=ordservid)

	if len(Inbox)>0:
		inboxID = Inbox[0]
		newMsg = message(inboxid=inboxID,msg=msgs)
		newMsg.save()
	else:
		custid = customer.objects.filter(custid=custID)[0]
		provid = provider.objects.filter(provid = provID)[0]
		osid = ordered_service.objects.filter(id = ordservid)[0]

		newInbox = inbox(custid=custid,provid=provid,osid=osid)
		newInbox.save()

		OldInboxID = inbox.objects.filter(osid=ordservid)[0]
		newmsg = message(inboxid=OldInboxID,msg=msgs)
		newmsg.save()

def rejectOrder(custid,provid,ordservid):
	osID = ordered_service.objects.filter(id = ordservid)[0]
	if (osID.status==0) or (osID.status==1):
		osID.status = 5
		osID.save()


		Inbox = inbox.objects.filter(osid=ordservid)

		if len(Inbox)>0:
			inboxID = Inbox[0].id

			message.objects.filter(inboxid = inboxID).delete()


def acceptOrder(custid,provid,ordservid):

	msgs = "Your order has been accepted and is being processed currently."

	osID = ordered_service.objects.filter(id = ordservid)[0]
	osID.status = 1
	osID.save()

	Inbox = inbox.objects.filter(osid=ordservid)

	if len(Inbox)>0:
		inboxID = Inbox[0]
		newMsg = message(inboxid=inboxID,msg=msgs)
		newMsg.save()
	else:
		custid = customer.objects.filter(custid=custid)[0]
		provid = provider.objects.filter(provid = provid)[0]
		osid = ordered_service.objects.filter(id = ordservid)[0]

		newInbox = inbox(custid=custid,provid=provid,osid=osid)
		newInbox.save()

		OldInboxID = inbox.objects.filter(osid=ordservid)[0]
		newmsg = message(inboxid=OldInboxID,msg=msgs)
		newmsg.save()


class msgView:
	def __init__(self,who,time,msgtxt):
		self.who = str(who)
		self.time = time
		self.msgtxt = msgtxt
def messages(inboxid):
	msgs = message.objects.filter(inboxid=inboxid)
	ret = []
	for m in msgs:
		ret.append(msgView(m.who,m.time+timedelta(hours=6),m.msg))
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

'''
def getPastOrderReqs(provid):
	ret = []
	"""
	for i in order.objects.all():

		tempname = customer.objects.filter(custid=i.custid)[0].firstname + " " + customer.objects.filter(custid = i.custid)[0].lastname
		tempid = customer.objects.filter(custid=i.custid)[0].custid
		
		print("Name is.. ",tempname)
		ret.append(orders(i.id,tempname,i.time_order,tempid,i.cost))
	return ret
	"""
	sp = service_provider.objects.filter(provid = provider.objects.filter(provid=provid)[0])
	os = ordered_service.objects.filter(spid__in=sp,status=4)
	#os = [oserv for oserv in ordered_service.objects.filter(spid__in=sp,status=0)]
	order_ = [o_s.orderid for o_s in os]

	for ordr in order_:
		cust = ordr.custid
		tempname = cust.firstname + " " + cust.lastname
		tempid = cust.custid

		#print("id is.. ",ordr.id)
		orders_obj = orders(ordr.id,tempname,ordr.time_order,tempid,ordr.cost)
		orders_obj.rate = ordr.rating_prov
		orders_obj.feedback = ordr.feedback_prov
		ret.append(orders)
	return ret

'''

def getPastOrderReqs(provid):
	ret = []
	"""
	for i in order.objects.all():

		tempname = customer.objects.filter(custid=i.custid)[0].firstname + " " + customer.objects.filter(custid = i.custid)[0].lastname
		tempid = customer.objects.filter(custid=i.custid)[0].custid
		
		print("Name is.. ",tempname)
		ret.append(orders(i.id,tempname,i.time_order,tempid,i.cost))
	return ret
	"""
	sp = service_provider.objects.filter(provid = provider.objects.filter(provid=provid)[0])
	os = ordered_service.objects.filter(spid__in=sp,status__in=[3,4])
	

	for ordr in os:
		cust = ordr.orderid.custid
		
		tempname = cust.firstname + " " + cust.lastname
		tempid = cust.custid

		#print("id is.. ",ordr.id)
		orders_obj = orders(ordr.id,tempname,ordr.orderid.time_order+timedelta(hours=6),tempid,ordr.cost)
		orders_obj.rate = ordr.rating_cust
		orders_obj.feedback = ordr.feedback_cust
		ret.append(orders_obj)
	return ret


def getPastOrderServReqs(ordid,provid):
	ret = []
	
	for i in ordered_service.objects.all():
		if (i.orderid_id == ordid) and (i.spid.provid.provid == provid) and (i.status == 4):
			#tempname = customer.objects.filter(custid=i.id)[0].firstname + " " + customer.objects.filter(custid = i.id)[0].lastname
			
			servid = service_provider.objects.filter(id = i.spid_id)[0].servid_id
			serv = service.objects.filter(id = servid)[0].servname


			custID = order.objects.filter(id = ordid)[0].custid_id
			custname = customer.objects.filter(custid = custID)[0].firstname + " " + customer.objects.filter(custid = custID)[0].lastname
			#print("Name is.. ",tempname)
			ret.append(orderservice(i.id,custname,serv,i.cost,i.rating_cust))
			
	return ret

def setFeedback(msg,rating,osid,custID):
	osID = ordered_service.objects.filter(id = osid)[0]
	osID.rating_cust = rating
	osID.save()
	osID.feedback_cust = msg
	osID.save()

	cust = customer.objects.filter(custid = custID)[0]
	count = cust.ratecount
	oldrating = cust.rating

	totalrating = oldrating*count
	totalrating += rating
	newrating = totalrating/(count+1)

	cust.rating = newrating

	cust.save()

	cust.ratecount = count+1

	cust.save()

	currstatus = osID.status
	if currstatus==1:
		osID.status=3
	elif currstatus==2:
		osID.status=4
	else:
		print("\n\n\n\n\nEEEEERRRROOOORRRRR\n\n\n\n\n")



	osID.save()

class servicesByProv():
	def __init__(self,servname,cost,desc):
		self.servname = servname
		self.cost=  cost
		self.desc = desc

def getServicesForSetupPage(spids):
	sps = []
	for spid in spids:
		servObj = service_provider.objects.filter(id=spid)[0]
		sps.append(servicesByProv(servObj.servid.servname,servObj.cost,servObj.desc))
	return sps 

def getImgPath(provid):
	path = provider.objects.filter(provid=provid)[0].provImage.url
	if path is not None:
		return path
	else:
		default = "/media/def.jpg"
		return default


class provprofile:
	def __init__(self,id,name,email,phone,desc,location,firstname,lastname):
		self.id = id
		self.name = name
		self.email = email
		self.phone = phone
		self.desc = desc
		self.location = location
		self.firstname = firstname
		self.lastname = lastname


def getProfileDetails(provid):
	ret = []

	'''for i in provider.objects.all():
		if (i.provid == provid):
			#tempname = customer.objects.filter(custid=i.id)[0].firstname + " " + customer.objects.filter(custid = i.id)[0].lastname
			
			email = provider.objects.filter(provid = provid)[0].email

			phone = provider.objects.filter(provid = provid)[0].phone

			desc = provider.objects.filter(provid = provid)[0].desc
			name = provider.objects.filter(provid = provid)[0].firstname + " " + provider.objects.filter(provid = provid)[0].lastname
			#print("Name is.. ",tempname)
			ret.append(provprofile(i.provid,name,email,phone,desc))
	'''
	email = provider.objects.filter(provid = provid)[0].email

	phone = provider.objects.filter(provid = provid)[0].phone

	location = provider.objects.filter(provid = provid)[0].location

	desc = provider.objects.filter(provid = provid)[0].desc
	name = provider.objects.filter(provid = provid)[0].firstname + " " + provider.objects.filter(provid = provid)[0].lastname
	#print("Name is.. ",tempname)
	fname = provider.objects.filter(provid = provid)[0].firstname
	lname = provider.objects.filter(provid = provid)[0].lastname

	temp = provprofile(provid,name,email,phone,desc,location,fname,lname)
	return temp

class recommendView:
	def __init__(self,spid,provname,servname,imgurl):
		self.id = spid
		self.provname=  provname
		self.servname= servname
		self.url = imgurl

def getTrendingServices():
	sps = service_provider.objects.filter(ratecount__gt=0).order_by('-rating')
	trending = [recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url) for ro in sps][0:5]
	print(trending)
	return trending

def checkPass(provid,password):
	realPass = provider.objects.filter(provid = provid)[0].password
	if realPass == password:
		return True
	return False

def deleteAcc(provid,msg):
	print(msg)
	provobj = provider.objects.filter(provid=provid)[0]
	firstname = provobj.firstname
	lastname = provobj.lastname
	email = provobj.email
	phone = provobj.phone
	obj = deletedprovider(firstname=firstname,lastname=lastname,email=email,phone=phone,msg=msg)
	obj.save()
	provider.objects.filter(provid=provid).delete()

