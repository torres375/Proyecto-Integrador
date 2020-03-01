
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from apps.users.models import Department

 
#class LoginForm(AuthenticationForm):
 #   def __init__(self, *args, **kwargs):
  #      self.fields['username'].widget.attrs['class']= 'form-control'       
   #     self.fields['username'].widget.attrs['placeholder']= 'Nombre de Usuario'
    #    self.fields['password'].widget.attrs['class']= 'form-control'
     #   self.fields['password'].widget.attrs['placeholder']= 'Contraseña'
        
        

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError(
                "Este usuario y contraseña no coinciden, intenta de nuevo.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('__all__')