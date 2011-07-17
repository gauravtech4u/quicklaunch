"""
Forms and validation code for user registration.

"""


from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from registration.models import RegistrationProfile
from core.models import ContactUs

# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_dict = { 'class': 'required' }

TYPE_CHOICES=(
                ('institute','Student'),
                ('job','Recruiter'),
                ('other','Others'),    
)
class ContactForm(forms.ModelForm):


    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_(u'email address'))

    mobile = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_(u'mobile'))
    name = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=30)),
                             label=_(u'Name'))
    message = forms.Textarea()

    
    
    class Meta:
                model=ContactUs
    



    

