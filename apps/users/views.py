from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView 
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from apps.index.models import Department, AirCraft 
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from django.views.generic import CreateView
from apps.users.forms import RegisterForm
from .forms import *



# Create your views here.

#class Login(FormView):
 #   template_name = 'login.html'
  #  form_class = LoginForm 
   # success_url = reverse_lazy('index:dashboard')

    #@method_decorator(csrf_protect)
    #@method_decorator(never_cache)

    #def dispatch(self,request,*args, **kwargs):
     #   if request.user.is_authenticated:
      #      return HttpResponseRedirect(self.get_success_url())
       # else:
        #    return super(Login,self).dispatch(request,*args,**kwargs)

    #def form_valid(self,form):
     #   login(self.request,form.get_user())
      #  return super(Login,self).form_valid(form)

class LoginView(TemplateView):
    template_name = 'layouts/landing/base.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index:list_aircraft')
        return super(LoginView, self).get(request, **kwargs)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.login(request)
            login(request, user)
            return redirect('index:list_aircraft')
        return render(request, self.template_name, {'form': form })


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index:login')


#Usuarios
class UserRegister(CreateView):
    model = User
    template_name = "user/user.html"
    form_class = RegisterForm
    success_url = reverse_lazy('index:dashboard')

    def get_success_url(self):
        pk = self.object.pk
        return reverse('users:detail', kwargs={'pk': pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['minor_operative_unit'].queryset = MinorOperativeUnit.objects.none()
        context['form'].fields['tactic_unit'].queryset = TacticUnit.objects.none()
        return context

@method_decorator(user_passes_test(lambda u: u.profile.user_type.code == 1, login_url=reverse_lazy('index:login')), name='dispatch')
class UserDetail(DetailView):
    model = User
    template_name = "user/detail.html"


@method_decorator(user_passes_test(lambda u: u.profile.user_type.code == 1, login_url=reverse_lazy('index:login')), name='dispatch')
class UserUpdate(UpdateView):
    model = User
    template_name = "user/user.html"
    form_class = RegisterForm
    
    def get_success_url(self):
        pk = self.object.pk
        return reverse('users:detail', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: u.profile.user_type.code == 1, login_url=reverse_lazy('index:login')), name='dispatch')
class UserDelete(DeleteView):
    model = User
    success_url = reverse_lazy('users:list')


@method_decorator(user_passes_test(lambda u: u.profile.user_type.code == 1, login_url=reverse_lazy('index:login')), name='dispatch')
class UserList(ListView):
    model = User
    template_name = "user/list.html"
    form_class = RegisterForm
    context_object_name = "user_list"    
