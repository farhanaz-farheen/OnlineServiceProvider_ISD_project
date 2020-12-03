from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, timedelta
from account.models import customer, ordered_service

class category(models.Model):
	catname = models.CharField(max_length=100, unique=True)
	desc = models.CharField(max_length=300)
	catImage = models.ImageField(upload_to='categoryImage/',null= True)
	def __str__(self):
		return self.catname

class service(models.Model):
	servname = models.CharField(max_length=100, unique=True)
	catname = models.ForeignKey(category, on_delete=models.CASCADE)
	servImage = models.ImageField(upload_to='serviceImage/',null= True)
	def __str__(self):
		return self.servname	

class provider(models.Model):
	provid = models.AutoField(primary_key=True)
	firstname = models.CharField(max_length=100)
	lastname = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	phone = models.PositiveIntegerField(default=1000000000, validators=[MinValueValidator(1000000000), MaxValueValidator(1999999999)])
	password = models.CharField(max_length=100)
	desc = models.CharField(max_length=300)
	catname = models.ForeignKey(category, on_delete=models.CASCADE)
	adminid = models.ForeignKey('admins.admin_model', on_delete=models.CASCADE, null= True)
	provImage = models.ImageField(upload_to='providerImage/',default="providerImage/default-user.png")
	location = models.CharField(max_length=100)


class service_provider(models.Model):
	cost = models.PositiveIntegerField(default=0)
	rating = models.FloatField(default=0)
	ratecount = models.PositiveIntegerField(default=0)
	desc = models.CharField(max_length=300)
	servid = models.ForeignKey(service, on_delete=models.CASCADE)
	provid = models.ForeignKey(provider, on_delete=models.CASCADE)
	looking = models.BooleanField(default=False)


class sp_images(models.Model):
	spid = models.ForeignKey(service_provider, on_delete=models.CASCADE)
	spImage = models.ImageField(upload_to='spImage/',null= True)


class requested_provider(models.Model):
	firstname = models.CharField(max_length=100)
	lastname = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	phone = models.PositiveIntegerField(default=1000000000, validators=[MinValueValidator(1000000000), MaxValueValidator(1999999999)])
	password = models.CharField(max_length=100)
	desc = models.CharField(max_length=300)
	catname = models.ForeignKey(category, on_delete=models.CASCADE)
	idImage = models.ImageField(upload_to='id_image/',blank= True)

class requested_service(models.Model):
	provider = models.ForeignKey(requested_provider, on_delete=models.CASCADE)
	service = models.ForeignKey(service,on_delete=models.CASCADE, null= True)
	serv_idImage = models.ImageField(upload_to='serv_id_image/',blank= True)



class inbox(models.Model):
	custid = models.ForeignKey(customer,on_delete=models.CASCADE)
	provid = models.ForeignKey(provider,on_delete=models.CASCADE)
	osid = models.ForeignKey(ordered_service,on_delete=models.CASCADE)

class message(models.Model):
	inboxid = models.ForeignKey(inbox,on_delete=models.CASCADE)
	who = models.PositiveIntegerField(default= 1)
	time = models.DateTimeField(default=datetime.now)
	msg = models.CharField(max_length=500)

class deletedprovider(models.Model):
	provid = models.AutoField(primary_key=True)
	firstname = models.CharField(max_length=100)
	lastname = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	phone = models.PositiveIntegerField(default=1000000000, validators=[MinValueValidator(1000000000), MaxValueValidator(1999999999)])
	msg = models.CharField(max_length=300)