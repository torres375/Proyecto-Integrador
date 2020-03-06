from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    address = forms.CharField(required=True) # required=True para que no los deje validar si no se envia este campo

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password1', 'password2', ) #Pueden escoger otros campos de usuarios

    def save(self, commit=True):
        instance = super(UserCreationForm, self).save(commit=False) #instance es el usuario
        address = self.cleaned_data['address']

        if commit:
            instance.set_password(password1) #set de la contraseña
            instance.save() #siempre hay que guardar después de poner la contraseña
            UserProfile.objects.create(user=instance, address=address) # creación del perfil o extensión del usuario
        return instance

#views.py
# class CreateUser(CreateView):
#     model = User
#     form_class = CustomUserCreationForm
#     template_name = "user/create.html"