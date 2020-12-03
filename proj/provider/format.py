from .models import requested_service
#from .forms import serviceDetForm

def services_images(provider):
	serv_imgs = []
	for i in requested_service.objects.filter(provider=provider):
		serv_imgs.append(service_image(i.id,i.service.servname,i.serv_idImage.url))
	return serv_imgs

class service_image:
	def __init__(self,id_,servname,imgurl):
		self.id = id_
		self.servname = servname
		self.imgurl = imgurl
		#self.form = serviceDetForm()