from django.views.generic import TemplateView,ListView,DetailView,CreateView,DeleteView,UpdateView 
from django.urls import reverse_lazy
from django.http import JsonResponse
from apps.index.models import * 
from apps.index.forms import * 

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


class DetailExample(TemplateView):
    template_name = "aircraft/detail.html"  


class DetailExample1(TemplateView):
    template_name = "crew/detail.html"


class CrewView(TemplateView):
    template_name = "crew/crew.html"    


class CrewFormView(TemplateView):
    template_name = "example/crew_form.html"      


class ListAircraft (ListView):
    template_name = 'aircraft/list.html'
    model = AirCraft
    context_object_name = 'aircraft_list'

def get_municipalities(request):
    id_department = request.GET.get('id_department')
    municipalities = Municipality.objects.none()
    options = '<option value="" selected="selected">---------</option>'
    if id_department:
        municipalities = Municipality.objects.filter(department__pk=id_department)   
    for municipality in municipalities:
        options += '<option value="%s">%s</option>' % (
            municipality.pk,
            municipality.name
        )
    response = {}
    response['municipalities'] = options
    return JsonResponse(response)


class CreateAircraft (CreateView):
    template_name = 'aircraft/form.html'
    model = AirCraft
    form = AirCraftForm
    fields = "__all__"
    success_url = reverse_lazy('index:list_aircraft')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['municipality'].queryset = Municipality.objects.none()
        context['departments'] = Department.objects.all()
        return context


class DetailAircraft(DetailView):
    template_name ="aircraft/detail.html"
    model = AirCraft
    context_object_name = "property_list"


class UpdateAircraft(UpdateView):
    template_name = "aircraft/form.html"
    model = AirCraft
    form = AirCraftForm
    fields = "__all__"
    success_url = reverse_lazy('index:list_aircraft')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        context['form'].fields['municipality'].queryset = Municipality.objects.filter(department=instance.municipality.department)
        context['departments'] = Department.objects.all()
        context['department_id'] = instance.municipality.department.pk
        return context
    

class DeleteAircraft (DeleteView):
    model = AirCraft
    success_url = reverse_lazy('index:list_aircraft')


class CreateCrew(CreateView):
    template_name = 'crew/create.html'
    model = Crew     
    form = CrewForm
    fields = '__all__'
    success_url = reverse_lazy('index:crew_list')

class DetailCrew(DetailView): 
    template_name= "crew/detail.html"
    model = Crew
    context_object_name = "crew_list" 


class UpdateCrew(UpdateView):
    template_name="crew/create.html"
    model = Crew
    form = CrewForm
    fields = '__all__'
    success_url = reverse_lazy('index:crew_list')


class DeleteCrew(DeleteView):
    model = Crew
    success_url = reverse_lazy('index:crew_list')


class CrewList(ListView):
    template_name = "crew/list.html"
    model = Crew
    context_object_name = "crew_list"

    
    
    
