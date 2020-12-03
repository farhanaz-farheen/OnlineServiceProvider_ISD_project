from django.db import models
#from django.db import connection
from django.core.validators import MaxValueValidator, MinValueValidator

class admin_model(models.Model):
	adminid = models.AutoField(primary_key=True)
	firstname = models.CharField(max_length=100)
	lastname = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	phone = models.PositiveIntegerField(default=1000000000, validators=[MinValueValidator(1000000000), MaxValueValidator(1999999999)])
	password = models.CharField(max_length=100)

class allowed_services(models.Model):
	provider = models.ForeignKey('provider.provider', on_delete= models.CASCADE)
	service = models.CharField(max_length=100)