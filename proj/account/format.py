from provider.models import category, service

def categoriesAsTuple():
	categories = [(c.catname,c.catname) for c in category.objects.all()]
	catnames = tuple(categories)
	return catnames

def servicesAsTuple():
	services = [(c.servname,c.servname) for c in service.objects.all()]
	servnames = tuple(services)
	return servnames

"""
from .models import searchValues
class cat_serv:
	def construct(self,category):
		self.category = category
		result = searchValues()
		self.services = [i[1] for i in result.getServnames(category=[category])]

def categoriesAsTuple():
	result = searchValues()
	catnames=()
	category = []
	for i in result.getCatnames():
		category.append((i[0],i[0]))
	catnames = tuple(category)
	#print(catnames)
	return catnames

def servicesAsTuple():
	result = searchValues()
	servnames=()
	services = []
	for i in result.getServnames():
		services.append((i[1],i[1]))
	servnames = tuple(services)
	#print(servnames)
	return servnames

class service_provider:
	def __init__(self):
		self.info = []
#	def searchResult(self,criteria):

	def servidToProv(self,service):
		result = searchValues()
		servids = [i[0] for i in result.getServids(service)]
		provids = [i[0] for i in result.getProvids(servids)]
		for i in result.getProvinfo(provids):
			self.info.append((i[0],i[1],i[2]))
		print(self.info)

	def provcatToProv(self,provider,category):
		#print("\n\n\nHere\n\n\n")
		result = searchValues()		
		for i in result.provcatGetProvInfo(provider,category):
			self.info.append((i[0],i[1],i[2]))
		#print(self.info)

	def costToProv(self,cost_min,cost_max):
		result = searchValues()
		for i in result.costToProvid(cost_min,cost_max):
			val = result.getProvinfo([i[0]])
			for v in val:
				self.info.append((v[0],v[1],v[2]))
		#print(self.info)

	def construct(self,costmin,costmax):
		searchObj = []
		result = searchValues()
		found = []
		for prov in self.info:
			for val in result.getServProv(prov[0]):
				if val[0] not in found:
					if (costmin==-1 or val[1]>costmin) and (costmax==-1 or val[1]<costmax):
						sobj = search_view()
						sobj.provname = str(prov[1]+" "+prov[2])
						sobj.cost = val[1]
						if val[3]==0:
							sobj.rating = "No rating yet"
						else:
							sobj.rating = val[2]
						sobj.desc = str(val[4])				
						searchObj.append(sobj)
						found.append(val[0])
		return searchObj


def formatPromo():
	result = searchValues()
	rows = result.getPromo()
	promoObj = []
	for r in rows:
		pr = promo_view()
		pr.provname = r[0] + " " + r[1]
		pr.code = r[3]
		pr.startdate = r[4]
		pr.enddate = r[5]
		pr.discount = r[6]
		promoObj.append(pr)
	return promoObj

class promo_view:
	def __init__(self):
		self.provname = ""

class search_view:
	
	def __init__(self):
		self.provname = ""
		self.cost = 0
		self.rating = 0 
		self.desc = ""
	
	def construct(self,provinfo):
		result = searchValues()
		for prov in provinfo:
			for val in result.getServProv(prov[0]):
				self.provname.append(str(prov[1]+" "+prov[2]))
				self.cost.append(val[1])
				if val[3]==0:
					self.rating.append("No rating yet")
				else:
					self.rating.append(val[2])
				self.desc.append(val[4])
"""


"""
def getCommonOrderViewForProfile(custid):
	_,_,_,recOrders = showRecommends(custid)
	orderObjs = []
	if (recOrders is None) or (len(recOrders)==0):
		return orderObjs
	elif len(recOrders)==1:
		ro = recOrders[0]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		orderObjs.append(recommendView(0,"Ordering Services","Simple and Easy","0"))
		orderObjs.append(recommendView(0,"Recommendation","Based on your preferences","0"))
	elif len(recOrders)==2:
		ro = recOrders[0]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		ro = recOrders[1]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		orderObjs.append(recommendView(0,"Recommendation","Based on your preferences","0"))
	else:
		ro = recOrders[0]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		ro = recOrders[1]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		ro = recOrders[2]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
	return orderObjs

def getRangeOrderViewForProfile(custid):
	_,_,recOrders,_ = showRecommends(custid)
	orderObjs = []
	if (recOrders is None) or (len(recOrders)==0):
		return orderObjs
	elif len(recOrders)==1:
		ro = recOrders[0]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		orderObjs.append(recommendView(0,"Ordering Services","Simple and Easy","0"))
		orderObjs.append(recommendView(0,"Recommendation","Based on your preferences","0"))
	elif len(recOrders)==2:
		ro = recOrders[0]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		ro = recOrders[1]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		orderObjs.append(recommendView(0,"Recommendation","Based on your preferences","0"))
	else:
		ro = recOrders[0]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		ro = recOrders[1]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		ro = recOrders[2]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
	return orderObjs

def getProviderOrderViewForProfile(custid):
	_,recOrders,_,_ = showRecommends(custid)
	orderObjs = []
	if (recOrders is None) or (len(recOrders)==0):
		return orderObjs
	elif len(recOrders)==1:
		ro = recOrders[0]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		orderObjs.append(recommendView(0,"Ordering Services","Simple and Easy","0"))
		orderObjs.append(recommendView(0,"Recommendation","Based on your preferences","0"))
	elif len(recOrders)==2:
		ro = recOrders[0]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		ro = recOrders[1]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		orderObjs.append(recommendView(0,"Recommendation","Based on your preferences","0"))
	else:
		ro = recOrders[0]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		ro = recOrders[1]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		ro = recOrders[2]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
	return orderObjs

def getServiceOrderViewForProfile(custid):
	recOrders,_,_,_ = showRecommends(custid)
	orderObjs = []
	if (recOrders is None) or (len(recOrders)==0):
		return orderObjs
	elif len(recOrders)==1:
		ro = recOrders[0]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		orderObjs.append(recommendView(0,"Ordering Services","Simple and Easy","0"))
		orderObjs.append(recommendView(0,"Recommendation","Based on your preferences","0"))
	elif len(recOrders)==2:
		ro = recOrders[0]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		ro = recOrders[1]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		orderObjs.append(recommendView(0,"Recommendation","Based on your preferences","0"))
	else:
		ro = recOrders[0]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		ro = recOrders[1]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		ro = recOrders[2]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
	return orderObjs

def getRecommendOrderViewForProfile(custid):
	recOrders = recommendFromOrder(custid)
	orderObjs = []
	if len(recOrders)==0:
		return orderObjs
	elif len(recOrders)==1:
		ro = recOrders[0]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		orderObjs.append(recommendView(0,"Ordering Services","Simple and Easy","0"))
		orderObjs.append(recommendView(0,"Recommendation","Based on Orders","0"))
	elif len(recOrders)==2:
		ro = recOrders[0]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		ro = recOrders[1]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		orderObjs.append(recommendView(0,"Recommendation","Based on Orders","0"))
	else:
		ro = recOrders[0]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		ro = recOrders[1]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
		ro = recOrders[2]
		orderObjs.append(recommendView(ro.id,ro.provid.firstname+' '+ro.provid.lastname,ro.servid.servname,ro.servid.servImage.url))
	return orderObjs

"""