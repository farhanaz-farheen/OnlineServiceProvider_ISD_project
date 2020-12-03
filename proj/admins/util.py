from .models import *
from provider.models import category,service,requested_provider,requested_service,provider, deletedprovider
from account.models import deletedcustomer
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def emailSend(msgstring, dest):
	msg = MIMEMultipart()
	password = "proxierOSP"
	msg['From'] = "onlineserviceprovider131625@gmail.com"
	message = msgstring
	msg['To'] = dest
	msg['Subject'] = "Response to Provider's Request"
	# add in the message body
	msg.attach(MIMEText(message, 'plain'))
 
	#create server
	server = smtplib.SMTP('smtp.gmail.com: 587')
 
	server.starttls()
 
	# Login Credentials for sending the mail
	server.login(msg['From'], password)
 
 
	# send the message via the server.
	server.sendmail(msg['From'], msg['To'], msg.as_string())
 
	server.quit()

def providerRequestProcess(adminid,reqProvider,idImage,approved,rejected):
	
	msgstring = "To whom it may concern, Thank you for choosing to join Online Service Provider. On the basis of those, we have come to the following conclusions: "

	if idImage==False:
		msgstring = msgstring + "We are sorry to inform you that \
we could not accept your request due to issues with your \
verification document (NID/Passport/Birth Certificate). \
Thank you for your patience."

	else:
		if len(approved)==0:
			msgstring = msgstring + "We are sorry to inform you that we could not accept your request due to issues with your documents. Thank you for your patience."
		else:
			msgstring = msgstring + "We have accepted the requests for the following services:\n"
			for x in approved:
				msgstring = msgstring + x + "\n"

			newProvider(reqProvider,adminid,approved)
			
			if len(rejected)>0:
				msgstring = msgstring + "Unfortunately, we could not accept the request for the following services due to some issues with your documents:\n"
				for y in rejected:
					msgstring = msgstring + y + "\n"
				msgstring = msgstring + "\nThank you for your patience."

	try:
		emailSend(msgstring, reqProvider.email)
	except:
		requested_service.objects.filter(provider=reqProvider).delete()
		reqProvider.delete()
		return -1
	else:
		requested_service.objects.filter(provider=reqProvider).delete()
		reqProvider.delete()
		return 0


class reqProvider:
	def __init__(self,id,name,email,category,desc,imgurl,phone):
		self.id = id
		self.name = name
		self.email = email
		self.category = category
		self.desc = desc
		self.imgurl = imgurl
		self.phone = phone

def getRequestedProvider(provid):
	i = requested_provider.objects.filter(id=provid)[0]
	return reqProvider(i.id,i.firstname+ ' '+i.lastname, i.email,i.catname,i.desc,i.idImage.url,i.phone)

def totalProviderReqs():
	return requested_provider.objects.all().count()

def getProviderReqs():
	ret = []
	for i in requested_provider.objects.all():
		ret.append(reqProvider(i.id,i.firstname+ ' '+i.lastname, i.email,i.catname,i.desc,i.idImage.url,i.phone))
	return ret

def isNewUser(email):
	user = admin_model.objects.filter(email=email)
	if len(user)==0:
		return True
	return False

def isUser(email,password):
	print(email,password,len(password))
	user = admin_model.objects.filter(email=email,password=password)
	for u in user:
		return u
	return None

def insertCategory(cd):
	newcat = category(catname=cd['catname'],desc=cd['desc'])
	newcat.save()

def insertService(cd):
	newserv = service(servname= cd['servname'],
		catname=category.objects.filter(catname=cd['catname'])[0])
	newserv.save()

def getCategories():
	#print(type(category.objects.all()))
	return [i.catname for i in category.objects.all()]

def editUser(adminid,cd):
	user = admin_model.objects.filter(adminid=adminid)[0]
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

	user.save()
	return user

def services_images(provider):
	serv_imgs = {}
	ret = []
	for i in requested_service.objects.filter(provider=provider):
		if serv_imgs.get(i.service.servname):
			serv_imgs[i.service.servname].append(i.serv_idImage.url)
		else:
			serv_imgs[i.service.servname]=[i.serv_idImage.url]
	for i in serv_imgs.items():
		ret.append(service_image(i[0],i[1]))
	return ret

class service_image:
	def __init__(self,servname,imgurls):
		#self.id = id_
		self.servname = servname
		self.imgurls = [i for i in imgurls]
		#self.form = serviceDetForm()

def newProvider(prov,adminid,services):
	adm = admin_model.objects.filter(adminid=adminid)[0]
	newprov = provider(firstname = prov.firstname, lastname = prov.lastname,
		email = prov.email , phone= prov.phone, password = prov.password,
		catname = prov.catname , desc = prov.desc , adminid = adm)
	newprov.save()
	for i in services:
		newserv = allowed_services(provider= newprov,service = i)
		newserv.save()

def isValidVerification(reqProvider,approved,rejected):
	for i in requested_service.objects.filter(provider=reqProvider):
		name = i.service.servname
		if (name not in approved) and (name not in rejected):
			return False
	return True

class deleteView():
	def __init__(self,name,email,phone,msg):
		self.name = name
		self.email = email
		self.phone = phone
		self.msg = msg

def getDeletedProviders():
	deleted = deletedprovider.objects.all()
	ret = []
	for p in deleted:
		name = p.firstname + ' ' + p.lastname
		ret.append(deleteView(name,p.email,p.phone,p.msg))

	return ret

def getDeletedCustomers():
	deleted = deletedcustomer.objects.all()
	ret = []
	for p in deleted:
		name = p.firstname + ' ' + p.lastname
		ret.append(deleteView(name,p.email,p.phone,p.msg))

	return ret

class adminprofile:
	def __init__(self,id,name,email,phone,firstname,lastname):
		self.id = id
		self.name = name
		self.email = email
		self.phone = phone
		self.firstname = firstname
		self.lastname = lastname


def getProfileDetails(adminid):
	ret = []

	email = admin_model.objects.filter(adminid = adminid)[0].email

	phone = admin_model.objects.filter(adminid = adminid)[0].phone

	
	name = admin_model.objects.filter(adminid = adminid)[0].firstname + " " + admin_model.objects.filter(adminid = adminid)[0].lastname
	#print("Name is.. ",tempname)
	fname = admin_model.objects.filter(adminid = adminid)[0].firstname
	lname = admin_model.objects.filter(adminid = adminid)[0].lastname

	temp = adminprofile(adminid,name,email,phone,fname,lname)
	return temp