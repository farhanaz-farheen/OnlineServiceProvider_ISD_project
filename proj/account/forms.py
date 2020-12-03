from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from .format import categoriesAsTuple, servicesAsTuple
from django.utils import timezone

class homeForm(forms.Form):
	btn = forms.CharField()

class loginForm(forms.Form):
	email = forms.EmailField(required=True,max_length=100)
	password = forms.CharField(max_length=100, widget=forms.PasswordInput)

class registerForm(forms.Form):
	firstname = forms.CharField(label='First name',required=True,max_length=100)
	lastname = forms.CharField(label='Last name',required=True,max_length=100)
	email = forms.EmailField(required=True,label='E-mail address')
	password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)
	phone = forms.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(1999999999)],label="Phone Number",required=True)

class EditCustomerForm(forms.Form):
	firstname = forms.CharField(label='First name',required=False,max_length=100)
	lastname = forms.CharField(label='Last name',required=False,max_length=100)
	email = forms.EmailField(required=False,label='E-mail address')
	password = forms.CharField(max_length=100, required=False, widget=forms.PasswordInput)
	phone = forms.IntegerField(label="Phone Number",required=False)

class cartForm(forms.Form):
	def __init__(self,*args,**kwargs):
		self.total = kwargs.pop('total')
		super(cartForm,self).__init__(*args,**kwargs)
		for i in range(1,self.total+1):
			self.fields['expDate_'+str(i)] = forms.DateField(label="Date",input_formats=["%Y-%m-%d"],required=True)
			self.fields['cost_'+str(i)] = forms.IntegerField(label="Cost",required=True)
			self.fields['desc_'+str(i)]= forms.CharField(label='Description',required=False,max_length=300)
			self.fields['deliveryAddress_'+str(i)]= forms.CharField(label='Address',required=True,max_length=300)
			self.fields['expTime_'+str(i)] = forms.TimeField(label="Time",widget=forms.TimeInput(format='%H:%M'),required=True)			

class filterForm(forms.Form):
	#category = forms.MultipleChoiceField(label="Category", required=False, widget=forms.CheckboxSelectMultiple, choices=categoriesAsTuple())
	#widget=forms.Select(choices=choicesCat)
	norating = forms.BooleanField(required=False)
	service = forms.MultipleChoiceField(label="Service", required=False, widget=forms.CheckboxSelectMultiple, choices=servicesAsTuple())
	cost_min= forms.IntegerField(min_value=0, max_value=100000, required=False, label="Cost Above")
	cost_max= forms.IntegerField(min_value=0, max_value=100000, required=False, label="Cost Below")
	rating_min= forms.IntegerField(min_value=1, max_value=5, required=False, label="Rating Above")
	rating_max= forms.IntegerField(min_value=1, max_value=5, required=False, label="Rating Below")
	district = forms.CharField(label='District',required=False)

class searchForm(forms.Form):
	#category = forms.MultipleChoiceField(label="Category", required=False, widget=forms.CheckboxSelectMultiple, choices=categoriesAsTuple())
	#widget=forms.Select(choices=choicesCat)
	service = forms.MultipleChoiceField(label="Service", required=False, widget=forms.CheckboxSelectMultiple, choices=servicesAsTuple())
	provider = forms.CharField(label='Provider',required=False)
	cost_min= forms.IntegerField(min_value=0, max_value=100000, required=False, label="Cost Above")
	cost_max= forms.IntegerField(min_value=0, max_value=100000, required=False, label="Cost Below")
	norating = forms.BooleanField(required=False)
	rating_min= forms.IntegerField(min_value=1, max_value=5, required=False, label="Rating Above")
	rating_max= forms.IntegerField(min_value=1, max_value=5, required=False, label="Rating Below")
	district = forms.CharField(label='District',required=False)
	
class editosForm(forms.Form):
	expDate= forms.DateField(label="Date",input_formats=["%Y-%m-%d"], required=False)
	deliveryAddress = forms.CharField(label='Address',max_length=300, required=False)
	expTime = forms.TimeField(label="Time",widget=forms.TimeInput(format='%H:%M'),required=False)

"""
class cartForm(forms.Form):
	expTime = forms.DateTimeField(label="Time",default=timezone.now(),required=True)
	cost = forms.IntegerField(label="Cost",required=True)
	desc = forms.CharField(label='Description',required=False,max_length=300)
	deliveryAddress = forms.CharField(label='Address',required=True,max_length=300)



class addressForm(forms.Form):
	city = forms.CharField(label='City',required=True,max_length=100)
	zipcode = forms.IntegerField(label="Zip Code",required=True)
	address = forms.CharField(label='Address',required=True,max_length=300)

class provDescForm(forms.Form):
	category = forms.CharField(label="Category",max_length=100, required=True)
	desc = forms.CharField(label='Description',required=True,max_length=300)

"""