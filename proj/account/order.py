from .models import *
from provider.models import *
from datetime import datetime
from django.db.models import Q
from django.conf import settings
from .util import getCartObj,order_view,ordered_service_view
from datetime import datetime, timedelta

"""
status

0 - pending
1 - accepted
2 - cust rated only
3 - prov rated only
4 - rated by both
5 - rejected(not in db)

"""
def extractLocation(loc):
	ll = loc.split("_")
	lat_lng = []
	for l in ll[1:]:
		lat_lng.append(l.split(":"))
	return lat_lng

def insertOrder(custid,cartobj,formval,loc):
	orderObj = order()
	orderObj.custid = customer.objects.filter(custid=custid)[0]
	orderObj.save()
	totalcost =0
	lat_lng = extractLocation(loc)
	for i in range(len(cartobj)):
		ordser = ordered_service()
		ordser.cost = formval['cost_'+str(i+1)]
		totalcost = totalcost+ordser.cost
		if formval.get('desc_'+str(i+1)):
			ordser.desc = formval.get('desc_'+str(i+1))
		ordser.deliveryAddress = formval['deliveryAddress_'+str(i+1)]
		ordser.orderid = orderObj
		ordser.spid = service_provider.objects.filter(id=cartobj[i].id)[0]
		ordser.expDate = datetime.combine(formval['expDate_'+str(i+1)],formval['expTime_'+str(i+1)])
		ordser.lat = float(lat_lng[i][0])
		ordser.lon = float(lat_lng[i][1])
		ordser.save()
	orderObj.cost = totalcost
	orderObj.save()



def PendingOrders(custid):
	ret = []
	retmap = {}
	orders = order.objects.filter(custid=customer.objects.filter(custid=custid)[0])

	for orderObj in orders:
		#total = 0
		ord_obj = order_view()
		ordsers = ordered_service.objects.filter(orderid=orderObj,status=0)
		ord_obj.dtime = orderObj.time_order
		ord_obj.dtime = ord_obj.dtime + timedelta(hours=6)

		for ordser in ordsers:
			if ordser.status == 0:
				#total = total+1
				ordser_obj = ordered_service_view()
				ordser_obj.id = ordser.id
				ordser_obj.spid = ordser.spid
				ordser_obj.provname = ordser.spid.provid.firstname + " " + ordser.spid.provid.lastname
				ordser_obj.servname = ordser.spid.servid.servname
				ordser_obj.cost = ordser.cost
				ordser_obj.lat = ordser.lat
				ordser_obj.lon = ordser.lon
				retmap[ordser_obj.id] = [ordser_obj.lat,ordser_obj.lon]
				if ordser.desc is not None:
					ordser_obj.desc = ordser.desc
				ordser_obj.deliveryAddress = ordser.deliveryAddress
				ordser_obj.dtime = ordser.expDate
				ord_obj.ordser.append(ordser_obj)
				ord_obj.cost = ord_obj.cost + ordser_obj.cost
		if len(ord_obj.ordser)>0:
			ret.append(ord_obj)
	return ret,retmap

def AcceptedOrders(custid):
	ret = []
	retmap = {}
	orders = order.objects.filter(custid=customer.objects.filter(custid=custid)[0])

	for orderObj in orders:
		#total = 0
		ord_obj = order_view()
		ordsers = ordered_service.objects.filter(orderid=orderObj,status__in=[1,3])
		ord_obj.dtime = orderObj.time_order
		ord_obj.dtime = ord_obj.dtime + timedelta(hours=6)
		for ordser in ordsers:
			if ordser.status == 1 or ordser.status==3:
				#total = total+1
				ordser_obj = ordered_service_view()
				ordser_obj.id = ordser.id
				ordser_obj.spid = ordser.spid
				ordser_obj.provname = ordser.spid.provid.firstname + " " + ordser.spid.provid.lastname
				ordser_obj.servname = ordser.spid.servid.servname
				ordser_obj.cost = ordser.cost
				ordser_obj.lat = ordser.lat
				ordser_obj.lon = ordser.lon
				retmap[ordser_obj.id] = [ordser_obj.lat,ordser_obj.lon]
				if ordser.desc is not None:
					ordser_obj.desc = ordser.desc
				ordser_obj.deliveryAddress = ordser.deliveryAddress
				ordser_obj.dtime = ordser.expDate
				ord_obj.ordser.append(ordser_obj)
				ord_obj.cost = ord_obj.cost + ordser_obj.cost
		if len(ord_obj.ordser)>0:
			ret.append(ord_obj)
	return ret,retmap


def confirm_os(osid,rating,feedback):
	print("confirming..")
	print(osid)
	osObj = ordered_service.objects.filter(id=osid)[0]
	#osObj.rating_cust = rating
	osObj.rating_prov = rating
	if len(feedback)>0:
		osObj.feedback_prov = feedback
	
	currstatus = osObj.status
	if currstatus==1:
		osObj.status=2
	elif currstatus==3:
		osObj.status=4
	else:
		print("\n\n\n\n\nEEEERRRROOOOORRRRR\n\n\n\n\n")

	prevrating = osObj.spid.rating
	prevrc = osObj.spid.ratecount
	osObj.spid.ratecount = prevrc+1
	osObj.spid.rating = (prevrating*prevrc + rating)/(prevrc+1)
	osObj.spid.save()
	osObj.save()

def getPastOrderReqs(custid):
	cust = customer.objects.filter(custid=custid)[0]
	orders = order.objects.filter(custid=custid)
	ordservs = ordered_service.objects.filter(orderid__in=orders,status__in=[2,4])
	ret = []
	for os_ in ordservs:
		os = ordered_service_view()
		os.time_order = os_.orderid.time_order
		os.time_order = os.time_order + timedelta(hours=6)
		prov = os_.spid.provid
		os.provname = prov.firstname + ' ' + prov.lastname
		os.servname = os_.spid.servid.servname
		os.cost = os_.cost
		os.rate = os_.rating_prov
		fdbk = os_.feedback_prov
		if fdbk is None:
			os.feedback = ""
		else:
			os.feedback = fdbk
		ret.append(os)
	return ret

def getOrderStats(custid,request):
	if request.session.get('cartadd'):
		cart = str(len(request.session['cartadd']))
		cartobjs = getCartObj(request.session['cartadd'])
	else:
		cart = "None"
		cartobjs = None
	return cart, cartobjs, len(PendingOrders(custid)[0]), len(AcceptedOrders(custid)[0]), len(getPastOrderReqs(custid))	

