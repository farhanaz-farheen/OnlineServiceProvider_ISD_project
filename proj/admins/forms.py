from django import forms
from provider.models import category, service

class loginForm(forms.Form):
	email = forms.EmailField(required=True,max_length=100)
	password = forms.CharField(max_length=100, widget=forms.PasswordInput)

class categoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
    	super(categoryForm, self).__init__(*args, **kwargs)
    	self.fields['catImage'].required = True
    	self.fields['catImage'].label= "Image"
    	self.fields['catname'].label = "Category"
    	self.fields['desc'].label = "Description"

    class Meta:
    	model = category
    	fields = ('catname', 'desc', 'catImage',)

class serviceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
    	super(serviceForm, self).__init__(*args, **kwargs)
    	self.fields['servImage'].required = True
    	self.fields['servImage'].label= "Image"
    	self.fields['servname'].label = "Service"
    	self.fields['catname'].label = "Category"

    class Meta:
    	model = service
    	fields = ('servname','catname', 'servImage',)

"""
class categoryForm(forms.Form):
	catname = forms.CharField(max_length=100, required=True , label="Category")
	desc = forms.CharField(max_length=300, required=True , label="Description")

class serviceForm(forms.Form):
	catname = forms.CharField(required=True , label="Category")
	servname = forms.CharField(max_length=100, required=True , label="Service")
"""


class EditAdminForm(forms.Form):
	firstname = forms.CharField(label='First name',required=False,max_length=100)
	lastname = forms.CharField(label='Last name',required=False,max_length=100)
	email = forms.EmailField(required=False,label='E-mail address')
	password = forms.CharField(max_length=100, required=False, widget=forms.PasswordInput)
	phone = forms.IntegerField(label="Phone Number",required=False)

class AddAdminForm(forms.Form):
	firstname = forms.CharField(label='First name',required=True,max_length=100)
	lastname = forms.CharField(label='Last name',required=True,max_length=100)
	email = forms.EmailField(required=True,label='E-mail address')
	password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)
	phone = forms.IntegerField(label="Phone Number",required=True)

class ProviderRequestForm(forms.Form):
	def __init__(self,*args,**kwargs):
		self.total = kwargs.pop('total')
		super(ProviderRequestForm,self).__init__(*args,**kwargs)
		for i in range(1,self.total+1):
			self.fields['serv_%s' %i] = forms.CharField(required=True)
	idoption = forms.CharField(required= True)
	#option = forms.ChoiceField(widget=forms.RadioSelect, choices=[('1', 'Approve'), ('2', 'Reject')],required=True)

class optionForm(forms.Form):
	btn = forms.CharField()