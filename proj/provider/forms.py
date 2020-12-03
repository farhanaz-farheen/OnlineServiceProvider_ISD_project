from django import forms
from .models import requested_provider, requested_service, sp_images

class loginForm(forms.Form):
	email = forms.EmailField(required=True,max_length=100)
	password = forms.CharField(max_length=100, widget=forms.PasswordInput)


class setupForm(forms.Form):
	def __init__(self,*args,**kwargs):
		self.total = kwargs.pop('total')
		super(setupForm,self).__init__(*args,**kwargs)
		for i in range(1,self.total+1):
			self.fields['cost_'+str(i)] = forms.IntegerField(required=True)
			self.fields['service_'+str(i)]= forms.CharField()
			self.fields['desc_'+str(i)]= forms.CharField(required=True)

class serviceImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
    	#self.sp = kwargs.pop('sp')
    	super(serviceImageForm, self).__init__(*args, **kwargs)	
    	#self.initial['spid'] = self.sp
    	self.fields['spid'].required = False
    	#self.fields['spid'].widget = forms.HiddenInput()
    	self.fields['spImage'].required = True
    class Meta:
    	model = sp_images
    	fields = ('spid','spImage',)
"""
class registerForm(forms.Form):
	firstname = forms.CharField(label='First name',required=True,max_length=100)
	lastname = forms.CharField(label='Last name',required=True,max_length=100)
	email = forms.EmailField(required=True,label='E-mail address')
	password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)
	phone = forms.IntegerField(label="Phone Number",required=True)
	catname = forms.CharField(label="Category", required=True)
	desc = forms.CharField(label='Description',required=True,max_length=300)
"""

#servnames = forms.MultipleChoiceField(label="Service", required=False, widget=forms.CheckboxSelectMultiple, choices=servicesAsTuple())

class registerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
    	super(registerForm, self).__init__(*args, **kwargs)
    	self.fields['idImage'].required = True
    	self.fields['idImage'].label= "Identification"
    	self.fields['firstname'].label = "First Name"
    	self.fields['lastname'].label = "Last Name"
    	self.fields['email'].label = "Email"
    	self.fields['password'].label = "Password"
    	#self.fields['password'].widget=forms.PasswordInput
    	self.fields['phone'].label = "Phone Number"
    	self.fields['catname'].label = "Category"
    	self.fields['desc'].label = "Description"

    class Meta:
    	model = requested_provider
    	fields = ('firstname', 'lastname', 'email', 'password', 'phone', 'catname', 'desc', 'idImage',)

class requestServiceForm(forms.ModelForm):
	serviceName = forms.ChoiceField(label = 'Service', required=True)
	def __init__(self, *args, **kwargs):
		services = kwargs.pop('services')
		super(requestServiceForm, self).__init__(*args, **kwargs)
		self.fields['serv_idImage'].required = True
		self.fields['serviceName'].choices = services

	class Meta:
		model = requested_service
		exclude = ['provider','service']

class homeForm(forms.Form):
	btn = forms.CharField()

class serviceDetForm(forms.Form):
	btn = forms.CharField()

class EditProviderForm(forms.Form):
	firstname = forms.CharField(label='First name',required=False,max_length=100)
	lastname = forms.CharField(label='Last name',required=False,max_length=100)
	desc = forms.CharField(label='Description',required=False,max_length=300)
	email = forms.EmailField(required=False,label='E-mail address')
	password = forms.CharField(max_length=100, required=False, widget=forms.PasswordInput)
	phone = forms.IntegerField(label="Phone Number",required=False)
	location = forms.CharField(label='Location',required=False,max_length=300)
	


class AddPromoForm(forms.Form):
	code = forms.CharField(label='Promo Code',required=True,max_length=8)
	startdate= forms.DateField(label="Starting Date (MM/DD/YYYY)",widget=forms.DateInput(format='%m/%d/%Y'),input_formats=('%m/%d/%Y', ))
	enddate= forms.DateField(label="Ending Date (MM/DD/YYYY)",widget=forms.DateInput(format='%m/%d/%Y'),input_formats=('%m/%d/%Y', ))
	discount = forms.IntegerField(label="Discount",required=True)

class costEditForm(forms.Form):
	servname = forms.CharField(label='Service',required=True,max_length=100)
	cost = forms.IntegerField(label="Cost",required=False)
	desc = forms.CharField(label='Description',required=False,max_length=300)
	looking = forms.CharField(label="Availability Status",required=False,max_length=100)

class detForm(forms.Form):
	btn = forms.CharField()
	
class negotiateForm(forms.Form):
	cost = forms.IntegerField(label="Cost",required=False)
	message = forms.CharField(label='Message',required=True,max_length=500)

class negotiate2Form(forms.Form):
	message = forms.CharField(label='Message',required=True,max_length=500)

class feedbackForm(forms.Form):
	
	comments = forms.CharField(label='Additional Comments',required=True,max_length=500)