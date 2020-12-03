from django.db import models
#from django.db import connection
from django.core.validators import MaxValueValidator, MinValueValidator
#from django.utils import timezone
from datetime import datetime, timedelta

class customer(models.Model):
	custid = models.AutoField(primary_key=True)
	firstname = models.CharField(max_length=100)
	lastname = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	phone = models.PositiveIntegerField(default=1000000000, validators=[MinValueValidator(1000000000), MaxValueValidator(1999999999)])
	password = models.CharField(max_length=100)
	rating = models.FloatField(default=0)
	ratecount = models.PositiveIntegerField(default=0)

class deletedcustomer(models.Model):
	custid = models.AutoField(primary_key=True)
	firstname = models.CharField(max_length=100)
	lastname = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	phone = models.PositiveIntegerField(default=1000000000, validators=[MinValueValidator(1000000000), MaxValueValidator(1999999999)])
	msg = models.CharField(max_length=300)

class order(models.Model):
	time_order = models.DateTimeField(default=datetime.now)
	cost = models.PositiveIntegerField(default=0)
	custid = models.ForeignKey(customer, on_delete=models.CASCADE)

class ordered_service(models.Model):
	cost = models.PositiveIntegerField(default=0)
	status = models.PositiveIntegerField(default=0)
	rating_prov = models.PositiveIntegerField(default=0)
	rating_cust = models.PositiveIntegerField(default=0)
	feedback_prov = models.CharField(max_length=100,null=True)
	feedback_cust = models.CharField(max_length=100,null=True)
	desc = models.CharField(max_length=300,null=True)
	deliveryAddress = models.CharField(max_length=300,default="")
	orderid = models.ForeignKey(order, on_delete=models.CASCADE)
	spid = models.ForeignKey('provider.service_provider', on_delete=models.CASCADE)
	expDate = models.DateTimeField(default=datetime.now)
	lat = models.FloatField(null=True)
	lon = models.FloatField(null=True)

class search_history(models.Model):
	custid = models.ForeignKey(customer, on_delete=models.CASCADE,null=True)
	mincost = models.CharField(max_length=1000,null=True)
	maxcost = models.CharField(max_length=1000,null=True)
	keywd = models.CharField(max_length=1000,null=True)
	services = models.CharField(max_length=1000,null=True)