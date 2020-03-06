from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from apps.index.models import *
class AirCraftForm(forms.ModelForm):
    municipality = forms.ModelChoiceField(queryset=Municipality.objects.none())
    class Meta:
        model = AirCraft
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super(AirCraftForm, self).__init__(*args, **kwargs)
        self.fields['municipality'].queryset = Municipality.objects.none()
        print(self.fields['municipality'].queryset)
        # self.fields['department']=forms.ModelChoiceField(queryset= Department.objects.all())

class CrewForm(forms.ModelForm): 
    class Meta:
        model = Crew 
        fields = ('__all__')
    