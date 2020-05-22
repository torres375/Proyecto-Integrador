
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from apps.index.models import *


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
    major_operative_unit = forms.ModelChoiceField(
        queryset=MajorOperativeUnit.objects.all())
    minor_operative_unit = forms.ModelChoiceField(
        queryset=MinorOperativeUnit.objects.all(), required=False)
    tactic_unit = forms.ModelChoiceField(
        queryset=TacticUnit.objects.all(), required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password1', 'password2', 'rank', 'user_type', 'tactic_unit',)

    def save(self, commit=True):
        instance = super(UserCreationForm, self).save(commit=False)
        rank = self.cleaned_data['rank']
        user_type = self.cleaned_data['user_type']
        tactic_unit = self.cleaned_data['tactic_unit']
        major_operative_unit = self.cleaned_data['major_operative_unit']
        minor_operative_unit = self.cleaned_data['minor_operative_unit']
        password1 = self.cleaned_data['password1']

        if commit:
            instance.set_password(password1)
            instance.save()
            UserProfile.objects.create(user=instance, rank=rank, user_type=user_type, major_operative_unit=major_operative_unit,
                                       minor_operative_unit=minor_operative_unit,  tactic_unit=tactic_unit, )
        return instance


class EditUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('password1', 'password2')

    def save(self, commit=True):
        instance = super(UserCreationForm, self).save(commit=False)
        password1 = self.cleaned_data['password1']

        if commit:
            instance.set_password(password1)
            instance.save()
        return instance

