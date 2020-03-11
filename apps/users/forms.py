
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from apps.index.models import *

 
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


class RegisterForm(UserCreationForm):
    rank = forms.ModelChoiceField(queryset=Rank.objects.all())     
    user_type = forms.ModelChoiceField(queryset=UserType.objects.all())
    tactic_unit = forms.ModelChoiceField(queryset=TacticUnit.objects.all())
    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','email', 'password1', 'password2','rank','user_type','tactic_unit',  )

    def save(self, commit=True):
        instance = super(UserCreationForm, self).save(commit=False)
        rank = self.cleaned_data['rank']
        user_type = self.cleaned_data['user_type']
        tactic_unit = self.cleaned_data['tactic_unit']
        password1 = self.cleaned_data['password1']

        if commit:
            instance.set_password(password1) 
            instance.save() 
            UserProfile.objects.create(user=instance, rank=rank, user_type=user_type, tactic_unit=tactic_unit, ) 
        return instance
       





