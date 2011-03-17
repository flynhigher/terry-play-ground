from django.conf import settings
from django import forms

from judges.models import Judge
from rateme_profiles.models import Profile

class ProfileForm(forms.ModelForm):
#    def __init__(self, *args, **kwargs):
#        super (ProfileForm, self ).__init__(*args, **kwargs) # populates the post
#        self.fields['myjudge'].queryset = Judge.active_objects.get_query_set()

    class Meta:
        model = Profile
        exclude = ('user',)
