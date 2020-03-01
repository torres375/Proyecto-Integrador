from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "index.html"

class Dashboard(TemplateView):
    template_name = "dashboard.html"

class Login(TemplateView):
    template_name = "login.html"

class TableExample(TemplateView):
    template_name = "example/table.html"

class FormExample(TemplateView):
    template_name = "example/form.html"

