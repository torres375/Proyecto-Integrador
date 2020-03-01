from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView
from django.contrib.auth import login,logout
from django.http import HttpResponse,HttpResponseRedirect
from .forms import LoginForm, DepartmentForm
from apps.users.models import Department
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
            if request.user.is_staff:
                return redirect('index:dashboard')
            logout(request)
        return super(LoginView, self).get(request, **kwargs)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.login(request)
            if user.is_staff:
                login(request, user)
                return redirect('index:dashboard')
            else:
                form.add_error(
                    None, "No eres un usuario administrador.")
                logout(request)
        return render(request, self.template_name, {'form': form })


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

class List (ListView):
    template_name = 'example/table.html'
    model = Department
    context_object_name = 'deparment_list'
    



    