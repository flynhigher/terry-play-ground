from django import forms

from about.models import Contact

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        exclude = ('submitter')
