from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.contrib.staticfiles.finders import find
from django.templatetags.static import static
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.utils.html import mark_safe
from django.http import JsonResponse
from django.db.models import Sum, F
from django.utils import timezone
from apps.index.utilspdf import *
from apps.index.models import *
from apps.index.forms import *
from apps.users.forms import *
from apps.users.utils import *
from apps.index.utils import *
from datetime import datetime
from datetime import timedelta
import json


@method_decorator(login_required(login_url=reverse_lazy('index:login')), name='dispatch')
class IndexView(TemplateView):
    template_name = "index.html"


# class Dashboard(TemplateView):
#     template_name = "dashboard.html"


# Aircraft Views
@method_decorator(user_passes_test(lambda u: read_permissions_2(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class ListAircraft (ListView):
    template_name = 'aircraft/list.html'
    model = AirCraft
    context_object_name = 'aircraft_list'


def get_municipalities(request):
    id_department = request.GET.get('id_department')
    municipalities = Municipality.objects.none()
    options = '<option value="" selected="selected">---------</option>'
    if id_department:
        municipalities = Municipality.objects.filter(
            department__pk=id_department)
    for municipality in municipalities:
        options += '<option value="%s">%s</option>' % (
            municipality.pk,
            municipality.name
        )
    response = {}
    response['municipalities'] = options
    return JsonResponse(response)


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class CreateAircraft (CreateView):
    template_name = 'aircraft/form.html'
    model = AirCraft
    form_class = AirCraftForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['municipality'].queryset = Municipality.objects.none()
        context['form'].fields['air_craft_models'].queryset = AirCraftModel.objects.none()
        context['departments'] = Department.objects.all()
        return context

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_aircraft', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: read_permissions_2(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class DetailAircraft(DetailView):
    template_name = "aircraft/detail.html"
    model = AirCraft
    context_object_name = "property_list"


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class UpdateAircraft(UpdateView):
    template_name = "aircraft/form.html"
    model = AirCraft
    form_class = AirCraftForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        context['form'].fields['municipality'].queryset = Municipality.objects.filter(
            department=instance.municipality.department)
        context['departments'] = Department.objects.all()
        context['department_id'] = instance.municipality.department.pk
        return context

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_aircraft', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class DeleteAircraft (DeleteView):
    model = AirCraft
    success_url = reverse_lazy('index:list_aircraft')
# Aircraft Views


# Crew Views
@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class CreateCrew(CreateView):
    template_name = 'crew/create.html'
    model = Crew
    form_class = CrewForm

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_crew', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # instance = self.get_object()
        STATUS_CHOICES = (
        )
        context['form'].fields['flight_charge'].choices = STATUS_CHOICES
        context['form'].fields['air_craft_models'].queryset = AirCraftModel.objects.none()
        return context


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class DetailCrew(DetailView):
    template_name = "crew/detail.html"
    model = Crew
    context_object_name = "crew_list"


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class UpdateCrew(UpdateView):
    template_name = "crew/create.html"
    model = Crew
    form_class = CrewForm

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_crew', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class DeleteCrew(DeleteView):
    model = Crew
    success_url = reverse_lazy('index:list_crew')


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class ListCrew(ListView):
    template_name = "crew/list.html"
    model = Crew
    context_object_name = "crew_list"
# Crew Views


# UOMA Views
@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class CreateUOMA(CreateView):
    template_name = 'uoma/create.html'
    model = MajorOperativeUnit
    form = MajorOperativeUnitForm
    fields = '__all__'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_uoma', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aircraft_models = AirCraftModel.objects.all().order_by('name')
        for aircraft_model in aircraft_models:
            assigned_hours = 0
            aircraft_model.assigned_hours = int(assigned_hours)
        context['aircraft_models'] = aircraft_models
        return context

    def form_valid(self, form):
        self.object = form.save()
        aircraft_models = list(AirCraftModel.objects.all().order_by('name'))
        assigned_aircrafts = []
        for aircraft_model in aircraft_models:
            input_id = "model_" + str(aircraft_model.pk)
            assigned_hours = int(self.request.POST.get(input_id, 0))
            data = {'aircraft_model': aircraft_model,
                    'assigned_hours': assigned_hours}
            assigned_aircrafts.append(data)
        for assigned_data in assigned_aircrafts:
            aircraft_model = assigned_data['aircraft_model']
            assigned_hours = assigned_data['assigned_hours']
            assigned = get_one_or_none(AssignedHourMajorOperationAircraftModel,
                                       major_operative_unit=self.object, aircraft_model=aircraft_model)
            if assigned is None:
                assigned = AssignedHourMajorOperationAircraftModel(
                    major_operative_unit=self.object, aircraft_model=aircraft_model, assigned_hours=0)
            assigned.assigned_hours = assigned_hours
            assigned.save()
        return super(CreateUOMA, self).form_valid(form)


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class DetailUOMA(DetailView):
    template_name = "uoma/detail.html"
    model = MajorOperativeUnit

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        aircraft_models = AirCraftModel.objects.all().order_by('name')
        for aircraft_model in aircraft_models:
            assigned_hours = 0
            assigned = get_one_or_none(AssignedHourMajorOperationAircraftModel,
                                       major_operative_unit=instance, aircraft_model=aircraft_model)
            if assigned is not None:
                assigned_hours = assigned.assigned_hours
            aircraft_model.assigned_hours = int(assigned_hours)
        context['aircraft_models'] = aircraft_models
        return context


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class UpdateUOMA(UpdateView):
    template_name = "uoma/create.html"
    model = MajorOperativeUnit
    form = MajorOperativeUnitForm
    fields = '__all__'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_uoma', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        aircraft_models = AirCraftModel.objects.all().order_by('name')
        for aircraft_model in aircraft_models:
            assigned_hours = 0
            assigned = get_one_or_none(AssignedHourMajorOperationAircraftModel,
                                       major_operative_unit=instance, aircraft_model=aircraft_model)
            if assigned is not None:
                assigned_hours = assigned.assigned_hours
            aircraft_model.assigned_hours = int(assigned_hours)
        context['aircraft_models'] = aircraft_models
        return context

    def form_valid(self, form):
        self.object = form.save()
        aircraft_models = list(AirCraftModel.objects.all().order_by('name'))
        assigned_aircrafts = []
        for aircraft_model in aircraft_models:
            input_id = "model_" + str(aircraft_model.pk)
            assigned_hours = int(self.request.POST.get(input_id, 0))
            data = {'aircraft_model': aircraft_model,
                    'assigned_hours': assigned_hours}
            assigned_aircrafts.append(data)
        for assigned_data in assigned_aircrafts:
            aircraft_model = assigned_data['aircraft_model']
            assigned_hours = assigned_data['assigned_hours']
            assigned = get_one_or_none(AssignedHourMajorOperationAircraftModel,
                                       major_operative_unit=self.object, aircraft_model=aircraft_model)
            if assigned is None:
                assigned = AssignedHourMajorOperationAircraftModel(
                    major_operative_unit=self.object, aircraft_model=aircraft_model, assigned_hours=0)
            assigned.assigned_hours = assigned_hours
            assigned.save()
        return super(UpdateUOMA, self).form_valid(form)


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class DeleteUOMA(DeleteView):
    model = MajorOperativeUnit
    success_url = reverse_lazy('index:list_uoma')


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class ListUOMA(ListView):
    template_name = "uoma/list.html"
    model = MajorOperativeUnit
    context_object_name = "uoma_list"
# UOMA Views


# UOME Views
@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class CreateUOME(CreateView):
    template_name = 'uome/create.html'
    model = MinorOperativeUnit
    form = MinorOperativeUnitForm
    fields = '__all__'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_uome', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class DetailUOME(DetailView):
    template_name = "uome/detail.html"
    model = MinorOperativeUnit


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class UpdateUOME(UpdateView):
    template_name = "uome/create.html"
    model = MinorOperativeUnit
    form = MinorOperativeUnitForm
    fields = '__all__'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_uome', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class DeleteUOME(DeleteView):
    model = MinorOperativeUnit
    success_url = reverse_lazy('index:list_uome')


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class ListUOME(ListView):
    template_name = "uome/list.html"
    model = MinorOperativeUnit
    context_object_name = "uome_list"
# UOME Views


# Tactic Unit Views
@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class CreateTacticUnit(CreateView):
    template_name = 'tactic_unit/create.html'
    model = TacticUnit
    form_class = TacticUnitForm

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_tactic_unit', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['minor_operative_unit'].queryset = MinorOperativeUnit.objects.none()
        return context


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class DetailTacticUnit(DetailView):
    template_name = "tactic_unit/detail.html"
    model = TacticUnit


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class UpdateTacticUnit(UpdateView):
    template_name = "tactic_unit/create.html"
    model = TacticUnit
    form_class = TacticUnitForm

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_tactic_unit', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        context['form'].fields['major_operative_unit'].initial = instance.minor_operative_unit.major_operative_unit
        return context


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class DeleteTacticUnit(DeleteView):
    model = TacticUnit
    success_url = reverse_lazy('index:list_tactic_unit')


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class ListTacticUnit(ListView):
    template_name = "tactic_unit/list.html"
    model = TacticUnit
    context_object_name = "ut_list"
# Tactic Unit Views


# Major Operation Views
@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class CreateMajorOperation(CreateView):
    template_name = 'major_operation/create.html'
    model = MajorOperation
    form = MajorOperationForm
    fields = '__all__'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_major_operation', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class DetailMajorOperation(DetailView):
    template_name = "major_operation/detail.html"
    model = MajorOperation


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class UpdateMajorOperation(UpdateView):
    template_name = "major_operation/create.html"
    model = MajorOperation
    form = MajorOperationForm
    fields = '__all__'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_major_operation', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class DeleteMajorOperation(DeleteView):
    model = MajorOperation
    success_url = reverse_lazy('index:list_major_operation')


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class ListMajorOperation(ListView):
    template_name = "major_operation/list.html"
    model = MajorOperation
    context_object_name = "major_operation_list"
# Major Operation Views


# Operation Views
@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class CreateOperation(CreateView):
    template_name = 'operation/create.html'
    model = Operation
    form = OperationForm
    fields = '__all__'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_operation', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class DetailOperation(DetailView):
    template_name = "operation/detail.html"
    model = Operation


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class UpdateOperation(UpdateView):
    template_name = "operation/create.html"
    model = Operation
    form = OperationForm
    fields = '__all__'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_operation', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class DeleteOperation(DeleteView):
    model = Operation
    success_url = reverse_lazy('index:list_operation')


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class ListOperation(ListView):
    template_name = "operation/list.html"
    model = Operation
    context_object_name = "operation_list"
# Operation Views


# FlightCondition Views
@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class CreateFlightCondition(CreateView):
    template_name = 'flight_condition/create.html'
    model = FlightCondition
    form = FlightConditionForm
    fields = '__all__'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_flight_condition', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class DetailFlightCondition(DetailView):
    template_name = "flight_condition/detail.html"
    model = FlightCondition


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class UpdateFlightCondition(UpdateView):
    template_name = "flight_condition/create.html"
    model = FlightCondition
    form = FlightConditionForm
    fields = '__all__'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_flight_condition', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class DeleteFlightCondition(DeleteView):
    model = FlightCondition
    success_url = reverse_lazy('index:list_flight_condition')


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class ListFlightCondition(ListView):
    template_name = "flight_condition/list.html"
    model = FlightCondition
    context_object_name = "flight_condition_list"
# FlightCondition Views


# Agreement Views
@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class CreateAgreement(CreateView):
    template_name = 'agreement/create.html'
    model = Agreement
    form = AgreementForm
    fields = '__all__'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_agreement', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aircraft_models = AirCraftModel.objects.all().order_by('name')
        for aircraft_model in aircraft_models:
            assigned_hours = 0
            aircraft_model.assigned_hours = int(assigned_hours)
        context['aircraft_models'] = aircraft_models
        return context

    def form_valid(self, form):
        self.object = form.save()
        aircraft_models = list(AirCraftModel.objects.all().order_by('name'))
        assigned_aircrafts = []
        for aircraft_model in aircraft_models:
            input_id = "model_" + str(aircraft_model.pk)
            assigned_hours = int(self.request.POST.get(input_id, 0))
            data = {'aircraft_model': aircraft_model,
                    'assigned_hours': assigned_hours}
            assigned_aircrafts.append(data)
        for assigned_data in assigned_aircrafts:
            aircraft_model = assigned_data['aircraft_model']
            assigned_hours = assigned_data['assigned_hours']
            assigned = get_one_or_none(
                AssignedHourAgreementAircraftModel, agreement=self.object, aircraft_model=aircraft_model)
            if assigned is None:
                assigned = AssignedHourAgreementAircraftModel(
                    agreement=self.object, aircraft_model=aircraft_model, assigned_hours=0)
            assigned.assigned_hours = assigned_hours
            assigned.save()
        return super(CreateAgreement, self).form_valid(form)


@method_decorator(user_passes_test(lambda u: read_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class DetailAgreement(DetailView):
    template_name = "agreement/detail.html"
    model = Agreement

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        aircraft_models = AirCraftModel.objects.all().order_by('name')
        for aircraft_model in aircraft_models:
            assigned_hours = 0
            assigned = get_one_or_none(
                AssignedHourAgreementAircraftModel, agreement=instance, aircraft_model=aircraft_model)
            if assigned is not None:
                assigned_hours = assigned.assigned_hours
            aircraft_model.assigned_hours = int(assigned_hours)
        context['aircraft_models'] = aircraft_models
        return context


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class UpdateAgreement(UpdateView):
    template_name = "agreement/create.html"
    model = Agreement
    form = AgreementForm
    fields = '__all__'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_agreement', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        aircraft_models = AirCraftModel.objects.all().order_by('name')
        for aircraft_model in aircraft_models:
            assigned_hours = 0
            assigned = get_one_or_none(
                AssignedHourAgreementAircraftModel, agreement=instance, aircraft_model=aircraft_model)
            if assigned is not None:
                assigned_hours = assigned.assigned_hours
            aircraft_model.assigned_hours = int(assigned_hours)
        context['aircraft_models'] = aircraft_models
        return context

    def form_valid(self, form):
        self.object = form.save()
        aircraft_models = list(AirCraftModel.objects.all().order_by('name'))
        assigned_aircrafts = []
        for aircraft_model in aircraft_models:
            input_id = "model_" + str(aircraft_model.pk)
            assigned_hours = int(self.request.POST.get(input_id, 0))
            data = {'aircraft_model': aircraft_model,
                    'assigned_hours': assigned_hours}
            assigned_aircrafts.append(data)
        for assigned_data in assigned_aircrafts:
            aircraft_model = assigned_data['aircraft_model']
            assigned_hours = assigned_data['assigned_hours']
            assigned = get_one_or_none(
                AssignedHourAgreementAircraftModel, agreement=self.object, aircraft_model=aircraft_model)
            if assigned is None:
                assigned = AssignedHourAgreementAircraftModel(
                    agreement=self.object, aircraft_model=aircraft_model, assigned_hours=0)
            assigned.assigned_hours = assigned_hours
            assigned.save()
        return super(UpdateAgreement, self).form_valid(form)


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class DeleteAgreement(DeleteView):
    model = Agreement
    success_url = reverse_lazy('index:list_agreement')


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class ListAgreement(ListView):
    template_name = "agreement/list.html"
    model = Agreement
    context_object_name = "agreement_list"
# Agreement Views


# AirCraftType Views
@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class CreateAirCraftType(CreateView):
    template_name = 'aircraft_type/create.html'
    model = AirCraftType
    form = AirCraftTypeForm
    fields = '__all__'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_aircraft_type', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class DetailAirCraftType(DetailView):
    template_name = "aircraft_type/detail.html"
    model = AirCraftType


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class UpdateAirCraftType(UpdateView):
    template_name = "aircraft_type/create.html"
    model = AirCraftType
    form = AirCraftTypeForm
    fields = '__all__'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_aircraft_type', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class DeleteAirCraftType(DeleteView):
    model = AirCraftType
    success_url = reverse_lazy('index:list_aircraft_type')


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class ListAirCraftType(ListView):
    template_name = "aircraft_type/list.html"
    model = AirCraftType
    context_object_name = "aircraft_type_list"
# AirCraftType Views


# AirCraftModel Views
@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class CreateAirCraftModel(CreateView):
    template_name = 'aircraft_model/create.html'
    model = AirCraftModel
    form = AirCraftModelForm
    fields = '__all__'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_aircraft_model', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class DetailAirCraftModel(DetailView):
    template_name = "aircraft_model/detail.html"
    model = AirCraftModel


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class UpdateAirCraftModel(UpdateView):
    template_name = "aircraft_model/create.html"
    model = AirCraftModel
    form = AirCraftModelForm
    fields = '__all__'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_aircraft_model', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class DeleteAirCraftModel(DeleteView):
    model = AirCraftModel
    success_url = reverse_lazy('index:list_aircraft_model')


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class ListAirCraftModel(ListView):
    template_name = "aircraft_model/list.html"
    model = AirCraftModel
    context_object_name = "aircraft_model_list"
# AirCraftType Views
# TODO Users roles

# AviationEvent Views
@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class CreateAviationEvent(CreateView):
    template_name = 'aviation_event/create.html'
    model = AviationEvent
    form = AviationEventForm
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['municipality'].queryset = Municipality.objects.none()
        context['departments'] = Department.objects.all()
        return context

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_aviation_event', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class DetailAviationEvent(DetailView):
    template_name = "aviation_event/detail.html"
    model = AviationEvent


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class UpdateAviationEvent(UpdateView):
    template_name = "aviation_event/create.html"
    model = AviationEvent
    form = AviationEventForm
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        context['form'].fields['municipality'].queryset = Municipality.objects.filter(
            department=instance.municipality.department)
        context['departments'] = Department.objects.all()
        context['department_id'] = instance.municipality.department.pk
        return context

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_aviation_event', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class DeleteAviationEvent(DeleteView):
    model = AviationEvent
    success_url = reverse_lazy('index:list_aviation_event')


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class ListAviationEvent(ListView):
    template_name = "aviation_event/list.html"
    model = AviationEvent
    context_object_name = "aviation_event_list"
# AviationEvent Views


# MissionType Views
@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class CreateMissionType(CreateView):
    template_name = 'mission_type/create.html'
    model = MissionType
    form = MissionTypeForm
    fields = '__all__'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_mission_type', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class DetailMissionType(DetailView):
    template_name = "mission_type/detail.html"
    model = MissionType


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class UpdateMissionType(UpdateView):
    template_name = "mission_type/create.html"
    model = MissionType
    form = MissionTypeForm
    fields = '__all__'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_mission_type', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class DeleteMissionType(DeleteView):
    model = MissionType
    success_url = reverse_lazy('index:list_mission_type')


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class ListMissionType(ListView):
    template_name = "mission_type/list.html"
    model = MissionType
    context_object_name = "mission_type_list"
# MissionType Views


# AviationMission Views
@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class CreateAviationMission(CreateView):
    template_name = 'aviation_mission/create.html'
    model = AviationMission
    form = AviationMissionForm
    fields = '__all__'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_aviation_mission', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class DetailAviationMission(DetailView):
    template_name = "aviation_mission/detail.html"
    model = AviationMission


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class UpdateAviationMission(UpdateView):
    template_name = "aviation_mission/create.html"
    model = AviationMission
    form = AviationMissionForm
    fields = '__all__'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_aviation_mission', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class DeleteAviationMission(DeleteView):
    model = AviationMission
    success_url = reverse_lazy('index:list_aviation_mission')


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class ListAviationMission(ListView):
    template_name = "aviation_mission/list.html"
    model = AviationMission
    context_object_name = "aviation_mission_list"
# AviationMission Views


# Configuration Views
@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class CreateConfiguration(CreateView):
    template_name = 'configuration/create.html'
    model = Configuration
    form = ConfigurationForm
    fields = '__all__'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_configuration', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class DetailConfiguration(DetailView):
    template_name = "configuration/detail.html"
    model = Configuration


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class UpdateConfiguration(UpdateView):
    template_name = "configuration/create.html"
    model = Configuration
    form = ConfigurationForm
    fields = '__all__'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('index:detail_configuration', kwargs={'pk': pk})


@method_decorator(user_passes_test(lambda u: write_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class DeleteConfiguration(DeleteView):
    model = Configuration
    success_url = reverse_lazy('index:list_configuration')


@method_decorator(user_passes_test(lambda u: read_permissions(u, True), login_url=reverse_lazy('index:login')), name='dispatch')
class ListConfiguration(ListView):
    template_name = "configuration/list.html"
    model = Configuration
    context_object_name = "configuration_list"
# Configuration Views


# Javi
def get_charges(request):
    id_aircraft_model = request.GET.get('id_aircraft_model')
    options = '<option value="" selected="selected">---------</option>'
    aircraft_model = None
    if id_aircraft_model:
        aircraft_model = get_one_or_none(AirCraftModel, pk=id_aircraft_model)
    if aircraft_model is not None:
        choices_charge = aircraft_model.get_choices_charge()
        for value, option in choices_charge.items():
            options += '<option value="%s">%s</option>' % (
                value,
                option
            )
    response = {}
    response['charges'] = options
    return JsonResponse(response)


def get_aircraft_models(request):
    id_aircraft_type = request.GET.get('id_aircraft_type')
    aircraft_models = AirCraftModel.objects.none()
    options = '<option value="" selected="selected">---------</option>'
    if id_aircraft_type:
        aircraft_models = AirCraftModel.objects.filter(
            air_craft_type__pk=id_aircraft_type)
    for aircraft_model in aircraft_models:
        options += '<option value="%s">%s</option>' % (
            aircraft_model.pk,
            aircraft_model.name
        )
    response = {}
    response['aircraft_models'] = options
    return JsonResponse(response)


def get_aircrafts(request):
    id_aircraft_model = request.GET.get('id_aircraft_model')
    aircrafts = AirCraft.objects.none()
    options = '<option value="" selected="selected">---------</option>'
    if id_aircraft_model:
        aircrafts = AirCraft.objects.filter(
            air_craft_models__pk=id_aircraft_model)
    for aircraft in aircrafts:
        options += '<option value="%s">%s</option>' % (
            aircraft.pk,
            aircraft.enrollment
        )
    response = {}
    response['aircrafts'] = options
    return JsonResponse(response)


def get_aviation_missions(request):
    id_mission_type = request.GET.get('id_mission_type')
    aviation_missions = AviationMission.objects.none()
    options = '<option value="" selected="selected">---------</option>'
    if id_mission_type:
        aviation_missions = AviationMission.objects.filter(
            mission_type__pk=id_mission_type)
    for aviation_mission in aviation_missions:
        options += '<option value="%s">%s %s</option>' % (
            aviation_mission.pk,
            aviation_mission.abbreviation,
            aviation_mission.name
        )
    response = {}
    response['aviation_missions'] = options
    return JsonResponse(response)


def get_operations(request):
    id_major_operation = request.GET.get('id_major_operation')
    operations = Operation.objects.none()
    options = '<option value="" selected="selected">---------</option>'
    if id_major_operation:
        operations = Operation.objects.filter(
            major_operations__pk=id_major_operation)
    for operation in operations:
        options += '<option value="%s">%s</option>' % (
            operation.pk,
            operation.name
        )
    response = {}
    response['operations'] = options
    return JsonResponse(response)


def get_minor_operative_units(request):
    id_major_operative_unit = request.GET.get('id_major_operative_unit')
    minor_operative_units = MinorOperativeUnit.objects.none()
    options = '<option value="" selected="selected">---------</option>'
    if id_major_operative_unit:
        minor_operative_units = MinorOperativeUnit.objects.filter(
            major_operative_unit__pk=id_major_operative_unit)
    for minor_operative_unit in minor_operative_units:
        options += '<option value="%s">%s</option>' % (
            minor_operative_unit.pk,
            minor_operative_unit.name
        )
    response = {}
    response['minor_operative_units'] = options
    return JsonResponse(response)


def get_tactic_unit(request):
    id_minor_operative_unit = request.GET.get('id_minor_operative_unit')
    tactic_units = TacticUnit.objects.none()
    options = '<option value="" selected="selected">---------</option>'

    if id_minor_operative_unit:
        tactic_units = TacticUnit.objects.filter(
            minor_operative_unit__pk=id_minor_operative_unit)
    for tactic_unit in tactic_units:
        options += '<option value="%s">%s</option>' % (
            tactic_unit.pk,
            tactic_unit.name
        )
    response = {}
    response['tactic_units'] = options
    return JsonResponse(response)


def get_tactic_unit_aviation(request):
    id_minor_operative_unit = request.GET.get('id_minor_operative_unit')
    tactic_units = TacticUnit.objects.none()
    options = '<option value="" selected="selected">---------</option>'

    if id_minor_operative_unit:
        tactic_units = TacticUnit.objects.filter(
            is_aviation=True, minor_operative_unit__pk=id_minor_operative_unit)
    for tactic_unit in tactic_units:
        options += '<option value="%s">%s</option>' % (
            tactic_unit.pk,
            tactic_unit.name
        )
    response = {}
    response['tactic_units'] = options
    return JsonResponse(response)


# FlightReport Views
@method_decorator(user_passes_test(lambda u: True, login_url=reverse_lazy('index:login')), name='dispatch')
class ListFlightReport(ListView):
    template_name = "flight_report/list.html"
    model = FlightReport
    context_object_name = "flight_report_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.localtime(timezone.now())
        context['current_date'] = now.strftime('%Y-%m-%d')
        context['past_date'] = (now-timedelta(days=30)).strftime('%Y-%m-%d')
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = FlightReport.objects.all()
        profile = user.profile
        if profile.user_type.code == 3 or profile.user_type.code == 5:
            queryset = queryset.filter(aviation_unit=profile.tactic_unit)
        return queryset


@method_decorator(user_passes_test(lambda u: True, login_url=reverse_lazy('index:login')), name='dispatch')
class DetailFlightReport(DetailView):
    template_name = "flight_report/detail.html"
    model = FlightReport

    def get_queryset(self):
        user = self.request.user
        queryset = FlightReport.objects.all()
        profile = user.profile
        if profile.user_type.code == 3 or profile.user_type.code == 5:
            queryset = queryset.filter(aviation_unit=profile.tactic_unit)
        return queryset


@method_decorator(user_passes_test(lambda u: report_permissions(u), login_url=reverse_lazy('index:login')), name='dispatch')
class CreateFlightReport(CreateView):
    template_name = 'flight_report/create.html'
    model = FlightReport
    form = FlightReportForm
    fields = '__all__'
    success_url = reverse_lazy('index:list_flight_report')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['municipality'].queryset = Municipality.objects.none()
        context['form'].fields['minor_operative_unit'].queryset = MinorOperativeUnit.objects.none()
        context['form'].fields['tactic_unit'].queryset = TacticUnit.objects.none()
        context['departments'] = Department.objects.all()
        context['aircraft_types'] = AirCraftType.objects.all()
        context['mission_types'] = MissionType.objects.all()
        context['major_operations'] = MajorOperation.objects.all()
        now = timezone.localtime(timezone.now())
        context['current_date'] = now.strftime('%Y-%m-%d')
        profile = self.request.user.profile
        if profile.user_type.code == 1 or profile.user_type.code == 4:
            context['aviation_units'] = TacticUnit.objects.filter(
                is_aviation=True)
        elif self.request.user.profile.tactic_unit is not None:
            context['aviation_unit'] = self.request.user.profile.tactic_unit
        elif self.request.user.profile.minor_operative_unit is not None:
            context['aviation_units'] = TacticUnit.objects.filter(
                is_aviation=True, minor_operative_unit=self.request.user.profile.minor_operative_unit)
        else:
            context['aviation_units'] = TacticUnit.objects.filter(
                is_aviation=True, minor_operative_unit__major_operative_unit=self.request.user.profile.major_operative_unit)
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = FlightReportForm(request.POST)
        aircraft = get_object_or_404(AirCraft, pk=request.POST.get('aircraft'))
        aircraft_model = aircraft.air_craft_models
        crew_list = []
        valid_crew = True
        pam_crew = request.POST.get('pam_crew', None)
        if pam_crew is not None:
            pam_crew = get_object_or_404(Crew, pk=pam_crew)
            crew_list.append(pam_crew)
            if not aircraft_model.has_pam:
                valid_crew = False
        elif aircraft_model.has_pam:
            valid_crew = False
        p_crew = request.POST.get('p_crew', None)
        if p_crew is not None:
            p_crew = get_object_or_404(Crew, pk=p_crew)
            crew_list.append(p_crew)
            if not aircraft_model.has_pilot:
                valid_crew = False
        elif aircraft_model.has_pilot:
            valid_crew = False
        iv_crew = request.POST.get('iv_crew', None)
        if iv_crew is not None:
            iv_crew = get_object_or_404(Crew, pk=iv_crew)
            crew_list.append(iv_crew)
            if not aircraft_model.has_flight_engineer:
                valid_crew = False
        elif aircraft_model.has_flight_engineer:
            valid_crew = False
        jt_crew = request.POST.get('jt_crew', None)
        if jt_crew is not None:
            jt_crew = get_object_or_404(Crew, pk=jt_crew)
            crew_list.append(jt_crew)
            if not aircraft_model.has_crew_chief:
                valid_crew = False
        elif aircraft_model.has_crew_chief:
            valid_crew = False
        tv_crew = request.POST.get('tv_crew', None)
        if tv_crew is not None:
            tv_crew = get_object_or_404(Crew, pk=tv_crew)
            crew_list.append(tv_crew)
            if not aircraft_model.has_flight_technician:
                valid_crew = False
        elif aircraft_model.has_flight_technician:
            valid_crew = False
        art_crew = request.POST.get('art_crew', None)
        if art_crew is not None:
            art_crew = get_object_or_404(Crew, pk=art_crew)
            crew_list.append(art_crew)
            if not aircraft_model.has_gunner:
                valid_crew = False
        elif aircraft_model.has_gunner:
            valid_crew = False
        cma_crew = request.POST.get('cma_crew', None)
        if cma_crew is not None:
            cma_crew = get_object_or_404(Crew, pk=cma_crew)
            crew_list.append(cma_crew)
            if not aircraft_model.has_commander:
                valid_crew = False
        elif aircraft_model.has_commander:
            valid_crew = False
        omi_crew = request.POST.get('omi_crew', None)
        if omi_crew is not None:
            omi_crew = get_object_or_404(Crew, pk=omi_crew)
            crew_list.append(omi_crew)
            if not aircraft_model.has_mission_operator:
                valid_crew = False
        elif aircraft_model.has_mission_operator:
            valid_crew = False
        ove_crew = request.POST.get('ove_crew', None)
        if ove_crew is not None:
            ove_crew = get_object_or_404(Crew, pk=ove_crew)
            crew_list.append(ove_crew)
            if not aircraft_model.has_vehicle_operator:
                valid_crew = False
        elif aircraft_model.has_vehicle_operator:
            valid_crew = False
        now = timezone.localtime(timezone.now())
        form.instance.date = now.date()
        if form.is_valid() and valid_crew:
            flight_report = form.save()
            flight_report.save()
            for crew in crew_list:
                AirCrew.objects.create(flight_reports=flight_report, crew=crew)
            return HttpResponseRedirect(self.success_url)
        print(form.errors)
        context = super().get_context_data()
        errors = []
        if not valid_crew:
            errors.append('Hay un error con la tripulación seleccionada.')
        context['errors'] = errors
        context['form'] = form
        return render(request, self.template_name, context)

   # def get_success_url(self):
     #   pk = self.object.pk
        # return reverse('index:detail_configuration', kwargs={'pk': pk})


class CrewFormView(TemplateView):
    template_name = 'flight_report/form_crew.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aircraft_id = self.request.GET.get('aircraft_id')
        aircraft = get_object_or_404(AirCraft, pk=aircraft_id)
        air_craft_type = aircraft.air_craft_type
        aircraft_model = aircraft.air_craft_models
        context['aircraft_model'] = aircraft_model
        basic_query_crew = Crew.objects.filter(air_craft_type=air_craft_type)
        if aircraft_model.has_pam:
            context['pam_crew'] = basic_query_crew.filter(
                flight_charge=Crew.PAM)
        if aircraft_model.has_pilot:
            context['p_crew'] = basic_query_crew.filter(flight_charge=Crew.PI)
        if aircraft_model.has_flight_engineer:
            context['iv_crew'] = basic_query_crew.filter(flight_charge=Crew.IV)
        if aircraft_model.has_crew_chief:
            context['jt_crew'] = basic_query_crew.filter(flight_charge=Crew.JT)
        if aircraft_model.has_flight_technician:
            context['tv_crew'] = basic_query_crew.filter(flight_charge=Crew.TV)
        if aircraft_model.has_gunner:
            context['art_crew'] = basic_query_crew.filter(
                flight_charge=Crew.ART)
        if aircraft_model.has_commander:
            context['cma_crew'] = basic_query_crew.filter(
                flight_charge=Crew.CMA)
        if aircraft_model.has_mission_operator:
            context['omi_crew'] = basic_query_crew.filter(
                flight_charge=Crew.OMI)
        if aircraft_model.has_vehicle_operator:
            context['ove_crew'] = basic_query_crew.filter(
                flight_charge=Crew.OVE)
        return context
# FlightReport Views


# PDF Views
@method_decorator(login_required(login_url=reverse_lazy('index:login')), name='dispatch')
class ListPdf(ListView):
    template_name = "pdf/pdf.html"
    model = FlightReport
    context_object_name = "flight_report_list"


def get_static(path):
    if settings.DEBUG:
        return find(path)
    else:
        return static(path)


@login_required(login_url=reverse_lazy('index:login'))
def gen_pdf(request):
    ids = request.GET.get('id')
    cid = request.GET.get('cid')

    start = request.GET.get('start_date',  None)
    end = request.GET.get('end_date',  None)

    basic_query = FlightReport.objects.all()
    if start is not None and end is not None:
        basic_query = FlightReport.objects.filter(date__range=[start, end])

    user = request.user
    profile = user.profile
    if profile.user_type.code == 3 or profile.user_type.code == 5:
        basic_query = basic_query.filter(aviation_unit=profile.tactic_unit)

    aircraft_models = AirCraftModel.objects.all().order_by('name')
    aircraft_models_dict = {}
    for aircraft_model in aircraft_models:
        flight_reports = basic_query.filter(aircraft__air_craft_models=aircraft_model).select_related().distinct(
            'aviation_unit', 'major_operative_unit', 'agreement', 'aircraft').order_by('aircraft', 'major_operative_unit')
        if flight_reports.count() > 0:
            aircraft_models_dict[aircraft_model.name] = flight_reports
    url = get_static('images/escudo_ejercito.png')
    url2 = get_static('images/Brigada_de_aviacion_33.jpg')
    url3 = get_static('images/circle_red.ico')
    url4 = get_static('images/circle_yellow.ico')
    url5 = get_static('images/circle_green.ico')
    now = datetime.now()
    format = now.strftime('%d/' + '%m/' + '%Y')
    params = {
        'aircraft_models_dict': aircraft_models_dict,
        'request': request,
        'image': url,
        'image2': url2,
        'image3': url3,
        'image4': url4,
        'image5': url5,
        'format': format,
        # 'project':project
    }
    return render_to_pdf('pdf/pdf.html', params)
# graphic elements


@login_required(login_url=reverse_lazy('index:login'))
def graph_bar_battalion(request):
    battalions = TacticUnit.objects.filter(is_aviation=True).order_by('name')
    fly_hours_list = []
    assigned_hours_list = []
    user = request.user
    profile = user.profile
    for battalion in battalions:
        battalion_query = FlightReport.objects.filter(aviation_unit=battalion)
        if profile.user_type.code == 3 or profile.user_type.code == 5:
            battalion_query = battalion_query.filter(
                aviation_unit=profile.tactic_unit)
        battalion_total_assigned = battalion_query.aggregate(
            Sum('aircraft__assigned_hours'))
        battalion_total_assigned = battalion_total_assigned.get(
            'aircraft__assigned_hours__sum')
        if battalion_total_assigned is None:
            battalion_total_assigned = 0
        battalion_total_fly = battalion_query.aggregate(
            Sum('aircraft__fly_hours'))
        battalion_total_fly = battalion_total_fly.get(
            'aircraft__fly_hours__sum')
        if battalion_total_fly is None:
            battalion_total_fly = 0
        assigned_hours_list.append(battalion_total_assigned)
        fly_hours_list.append(battalion_total_fly)
    data = [{'name': 'Horas Voladas', 'data': fly_hours_list}, {
        'name': 'Horas Asignadas', 'data': assigned_hours_list}]
    battalions = list(battalions.values_list(
        'abbreviation', flat=True).distinct())
    return render(request, 'graphic/graph_bar_battalion.html', {'battalions': mark_safe(json.dumps(battalions)), 'data': mark_safe(json.dumps(data))})


@login_required(login_url=reverse_lazy('index:login'))
def graphic_bar_month(request):
    # filter_mounth =
    now = datetime.now()
    year = now.year
    month1 = FlightReport.objects.filter(date__year__gte=year,
                                         date__month__gte=1)
    month2 = FlightReport.objects.filter(date__year__gte=year,
                                         date__month__gte=2)
    month3 = FlightReport.objects.filter(date__year__gte=year,
                                         date__month__gte=3)
    month4 = FlightReport.objects.filter(date__year__gte=year,
                                         date__month__gte=4)
    month5 = FlightReport.objects.filter(date__year__gte=year,
                                         date__month__gte=5)
    month6 = FlightReport.objects.filter(date__year__gte=year,
                                         date__month__gte=6)
    month7 = FlightReport.objects.filter(date__year__gte=year,
                                         date__month__gte=7)
    month8 = FlightReport.objects.filter(date__year__gte=year,
                                         date__month__gte=8)
    month9 = FlightReport.objects.filter(date__year__gte=year,
                                         date__month__gte=9)
    month10 = FlightReport.objects.filter(date__year__gte=year,
                                          date__month__gte=10)
    month11 = FlightReport.objects.filter(date__year__gte=year,
                                          date__month__gte=11)
    month12 = FlightReport.objects.filter(date__year__gte=year,
                                          date__month__gte=12)

    month1_total_assigned = month1.aggregate(Sum('aircraft__assigned_hours'))
    month2_total_assigned = month2.aggregate(Sum('aircraft__assigned_hours'))
    month3_total_assigned = month3.aggregate(Sum('aircraft__assigned_hours'))
    month4_total_assigned = month4.aggregate(Sum('aircraft__assigned_hours'))
    month5_total_assigned = month5.aggregate(Sum('aircraft__assigned_hours'))
    month6_total_assigned = month6.aggregate(Sum('aircraft__assigned_hours'))
    month7_total_assigned = month7.aggregate(Sum('aircraft__assigned_hours'))
    month8_total_assigned = month8.aggregate(Sum('aircraft__assigned_hours'))
    month9_total_assigned = month9.aggregate(Sum('aircraft__assigned_hours'))
    month10_total_assigned = month10.aggregate(Sum('aircraft__assigned_hours'))
    month11_total_assigned = month11.aggregate(Sum('aircraft__assigned_hours'))
    month12_total_assigned = month12.aggregate(Sum('aircraft__assigned_hours'))
    month1_total_fly = month1.aggregate(Sum('aircraft__fly_hours'))
    month2_total_fly = month2.aggregate(Sum('aircraft__fly_hours'))
    month3_total_fly = month3.aggregate(Sum('aircraft__fly_hours'))
    month4_total_fly = month4.aggregate(Sum('aircraft__fly_hours'))
    month5_total_fly = month5.aggregate(Sum('aircraft__fly_hours'))
    month6_total_fly = month6.aggregate(Sum('aircraft__fly_hours'))
    month7_total_fly = month7.aggregate(Sum('aircraft__fly_hours'))
    month8_total_fly = month8.aggregate(Sum('aircraft__fly_hours'))
    month9_total_fly = month9.aggregate(Sum('aircraft__fly_hours'))
    month10_total_fly = month10.aggregate(Sum('aircraft__fly_hours'))
    month11_total_fly = month11.aggregate(Sum('aircraft__fly_hours'))
    month12_total_fly = month12.aggregate(Sum('aircraft__fly_hours'))
    categories = "sooy una categoria"
    month1_total_fly = month1_total_fly.get('aircraft__fly_hours__sum')
    month2_total_fly = month2_total_fly.get('aircraft__fly_hours__sum')
    month3_total_fly = month3_total_fly.get('aircraft__fly_hours__sum')
    month4_total_fly = month4_total_fly.get('aircraft__fly_hours__sum')
    month5_total_fly = month5_total_fly.get('aircraft__fly_hours__sum')
    month6_total_fly = month6_total_fly.get('aircraft__fly_hours__sum')
    month7_total_fly = month7_total_fly.get('aircraft__fly_hours__sum')
    month8_total_fly = month8_total_fly.get('aircraft__fly_hours__sum')
    month9_total_fly = month9_total_fly.get('aircraft__fly_hours__sum')
    month10_total_fly = month10_total_fly.get('aircraft__fly_hours__sum')
    month11_total_fly = month11_total_fly.get('aircraft__fly_hours__sum')
    month12_total_fly = month12_total_fly.get('aircraft__fly_hours__sum')
    month1_total_assigned = month1_total_assigned.get(
        'aircraft__assigned_hours__sum')
    month2_total_assigned = month2_total_assigned.get(
        'aircraft__assigned_hours__sum')
    month3_total_assigned = month3_total_assigned.get(
        'aircraft__assigned_hours__sum')
    month4_total_assigned = month4_total_assigned.get(
        'aircraft__assigned_hours__sum')
    month5_total_assigned = month5_total_assigned.get(
        'aircraft__assigned_hours__sum')
    month6_total_assigned = month6_total_assigned.get(
        'aircraft__assigned_hours__sum')
    month7_total_assigned = month7_total_assigned.get(
        'aircraft__assigned_hours__sum')
    month8_total_assigned = month8_total_assigned.get(
        'aircraft__assigned_hours__sum')
    month9_total_assigned = month9_total_assigned.get(
        'aircraft__assigned_hours__sum')
    month10_total_assigned = month10_total_assigned.get(
        'aircraft__assigned_hours__sum')
    month11_total_assigned = month11_total_assigned.get(
        'aircraft__assigned_hours__sum')
    month12_total_assigned = month12_total_assigned.get(
        'aircraft__assigned_hours__sum')

    if month1_total_fly is None:
        month1_total_fly = 0
    if month2_total_fly is None:
        month2_total_fly = 0
    if month3_total_fly is None:
        month3_total_fly = 0
    if month4_total_fly is None:
        month4_total_fly = 0
    if month5_total_fly is None:
        month5_total_fly = 0
    if month6_total_fly is None:
        month6_total_fly = 0
    if month7_total_fly is None:
        month7_total_fly = 0
    if month8_total_fly is None:
        month8_total_fly = 0
    if month9_total_fly is None:
        month9_total_fly = 0
    if month10_total_fly is None:
        month10_total_fly = 0
    if month11_total_fly is None:
        month11_total_fly = 0
    if month12_total_fly is None:
        month12_total_fly = 0

    if month1_total_assigned is None:
        month1_total_assigned = 0
    if month1_total_assigned is None:
        month1_total_assigned = 0
    if month2_total_assigned is None:
        month2_total_assigned = 0
    if month3_total_assigned is None:
        month3_total_assigned = 0
    if month4_total_assigned is None:
        month4_total_assigned = 0
    if month5_total_assigned is None:
        month5_total_assigned = 0
    if month6_total_assigned is None:
        month6_total_assigned = 0
    if month7_total_assigned is None:
        month7_total_assigned = 0
    if month8_total_assigned is None:
        month8_total_assigned = 0
    if month9_total_assigned is None:
        month9_total_assigned = 0
    if month10_total_assigned is None:
        month10_total_assigned = 0
    if month11_total_assigned is None:
        month11_total_assigned = 0
    if month12_total_assigned is None:
        month12_total_assigned = 0

    #fly_hours_total = fly_hours_total.get('fly_hours__sum')
    return render(request, 'graphic/graphic_bar_mounth.html', {
        'categories': json.dumps(categories),
        'month1_total_fly': json.dumps(month1_total_fly),
        'month2_total_fly': json.dumps(month2_total_fly),
        'month3_total_fly': json.dumps(month3_total_fly),
        'month4_total_fly': json.dumps(month4_total_fly),
        'month5_total_fly': json.dumps(month5_total_fly),
        'month6_total_fly': json.dumps(month6_total_fly),
        'month7_total_fly': json.dumps(month7_total_fly),
        'month8_total_fly': json.dumps(month8_total_fly),
        'month9_total_fly': json.dumps(month9_total_fly),
        'month10_total_fly': json.dumps(month10_total_fly),
        'month11_total_fly': json.dumps(month11_total_fly),
        'month12_total_fly': json.dumps(month12_total_fly),
        'month1_total_assigned': json.dumps(month1_total_assigned),
        'month2_total_assigned': json.dumps(month2_total_assigned),
        'month3_total_assigned': json.dumps(month3_total_assigned),
        'month4_total_assigned': json.dumps(month4_total_assigned),
        'month5_total_assigned': json.dumps(month5_total_assigned),
        'month6_total_assigned': json.dumps(month6_total_assigned),
        'month7_total_assigned': json.dumps(month7_total_assigned),
        'month8_total_assigned': json.dumps(month8_total_assigned),
        'month9_total_assigned': json.dumps(month9_total_assigned),
        'month10_total_assigned': json.dumps(month10_total_assigned),
        'month11_total_assigned': json.dumps(month11_total_assigned),
        'month12_total_assigned': json.dumps(month12_total_assigned),
    })


@login_required(login_url=reverse_lazy('index:login'))
def graphic_bar_years(request):
    dates = FlightReport.objects.dates('date', 'year')
    year_list = []
    data = {}
    user = request.user
    profile = user.profile
    for date in dates:
        year = date.year
        year_list.append(year)
        assigned_hours_list = []
        fly_hours_list = []
        for month in range(1, 13):
            month_query = FlightReport.objects.filter(date__year=year,
                                                      date__month=month)
            if profile.user_type.code == 3 or profile.user_type.code == 5:
                month_query = month_query.filter(
                    aviation_unit=profile.tactic_unit)
            month_total_assigned = month_query.aggregate(
                Sum('aircraft__assigned_hours'))
            month_total_assigned = month_total_assigned.get(
                'aircraft__assigned_hours__sum')
            if month_total_assigned is None:
                month_total_assigned = 0
            month_total_fly = month_query.aggregate(Sum('aircraft__fly_hours'))
            month_total_fly = month_total_fly.get('aircraft__fly_hours__sum')
            if month_total_fly is None:
                month_total_fly = 0
            assigned_hours_list.append(month_total_assigned)
            fly_hours_list.append(month_total_fly)
        data[year] = [{'name': 'Horas Voladas', 'data': fly_hours_list}, {
            'name': 'Horas Asignadas', 'data': assigned_hours_list}]
    first_year = year_list[0]
    return render(request, 'graphic/graphic_bar.html', {'years': year_list, 'data': mark_safe(json.dumps(data)), 'first_year': first_year})


@login_required(login_url=reverse_lazy('index:login'))
def graph_bar_aircraft_model_hours(request):
    aircraft_models = AirCraftModel.objects.all().order_by('name')
    data = {}
    assigned_hours_list = []
    fly_hours_list = []
    user = request.user
    profile = user.profile
    for aircraft_model in aircraft_models:
        model_query = FlightReport.objects.filter(
            aircraft__air_craft_models=aircraft_model)
        if profile.user_type.code == 3 or profile.user_type.code == 5:
            model_query = model_query.filter(aviation_unit=profile.tactic_unit)
        model_total_assigned = model_query.aggregate(
            Sum('aircraft__assigned_hours'))
        model_total_assigned = model_total_assigned.get(
            'aircraft__assigned_hours__sum')
        if model_total_assigned is None:
            model_total_assigned = 0
        model_total_fly = model_query.aggregate(Sum('aircraft__fly_hours'))
        model_total_fly = model_total_fly.get('aircraft__fly_hours__sum')
        if model_total_fly is None:
            model_total_fly = 0
        assigned_hours_list.append(model_total_assigned)
        fly_hours_list.append(model_total_fly)
    data = [{'name': 'Horas Voladas', 'data': fly_hours_list}, {
        'name': 'Horas Asignadas', 'data': assigned_hours_list}]
    # Operationals
    operationals = AviationMission.objects.filter(
        mission_type__name__icontains='Misiones Tácticas de Aviación')
    op_hours_list = []
    for aircraft_model in aircraft_models:
        model_query = FlightReport.objects.filter(aviation_mission__pk__in=operationals.values(
            'pk'), aircraft__air_craft_models=aircraft_model)
        if profile.user_type.code == 3 or profile.user_type.code == 5:
            model_query = model_query.filter(aviation_unit=profile.tactic_unit)
        model_total_fly = model_query.aggregate(Sum('aircraft__fly_hours'))
        model_total_fly = model_total_fly.get('aircraft__fly_hours__sum')
        op_hours_list.append(model_total_fly)
    # No Operationals
    no_operationals = AviationMission.objects.exclude(
        mission_type__name__icontains='Misiones Tácticas de Aviación')
    no_op_hours_list = []
    for aircraft_model in aircraft_models:
        model_query = FlightReport.objects.filter(aviation_mission__pk__in=no_operationals.values(
            'pk'), aircraft__air_craft_models=aircraft_model)
        if profile.user_type.code == 3 or profile.user_type.code == 5:
            model_query = model_query.filter(aviation_unit=profile.tactic_unit)
        model_total_fly = model_query.aggregate(Sum('aircraft__fly_hours'))
        model_total_fly = model_total_fly.get('aircraft__fly_hours__sum')
        no_op_hours_list.append(model_total_fly)
    data2 = [{'name': 'Horas Voladas', 'data': fly_hours_list}, {'name': 'Horas Asignadas', 'data': assigned_hours_list}, {
        'name': 'Horas Operacionales', 'data': op_hours_list}, {'name': 'Horas No Operacionales', 'data': no_op_hours_list}]
    # print(aircraft_models, data)
    aircraft_models = list(aircraft_models.values_list(
        'name', flat=True).distinct())
    return render(request, 'graphic/graph_bar_aircraft_model.html', {'aircraft_models': mark_safe(json.dumps(aircraft_models)), 'data': mark_safe(json.dumps(data)), 'data2': mark_safe(json.dumps(data2))})


# def graph_bar_aircraft_model_operation(request):
#     operationals = AviationMission.objects.filter(mission_type__name__icontains='Misiones Tácticas de Aviación')
#     no_operationals = AviationMission.objects.exclude(id__in=operationals.values('pk'))
#     data = {}
#     assigned_hours_list = []
#     fly_hours_list = []
#     for aircraft_model in aircraft_models:
#         model_query = FlightReport.objects.filter(
#             aircraft__air_craft_models=aircraft_model)
#         model_total_assigned = model_query.aggregate(
#             Sum('aircraft__assigned_hours'))
#         model_total_assigned = model_total_assigned.get(
#             'aircraft__assigned_hours__sum')
#         if model_total_assigned is None:
#             model_total_assigned = 0
#         model_total_fly = model_query.aggregate(Sum('aircraft__fly_hours'))
#         model_total_fly = model_total_fly.get('aircraft__fly_hours__sum')
#         if model_total_fly is None:
#             model_total_fly = 0
#         assigned_hours_list.append(model_total_assigned)
#         fly_hours_list.append(model_total_fly)
#     data = [{'name': 'Horas Voladas', 'data': fly_hours_list}, {
#         'name': 'Horas Asignadas', 'data': assigned_hours_list}]
#     # print(aircraft_models, data)
#     aircraft_models = list(aircraft_models.values_list('name', flat=True).distinct())
#     return render(request, 'graphic/graph_bar_aircraft_model.html', {'aircraft_models': mark_safe(json.dumps(aircraft_models)), 'data': mark_safe(json.dumps(data))})
# PDF Views


@login_required(login_url=reverse_lazy('index:login'))
def graph_pie_operational(request):
    user = request.user
    profile = user.profile
    operationals = AviationMission.objects.filter(
        mission_type__name__icontains='Misiones Tácticas de Aviación')
    query = FlightReport.objects.filter(
        aviation_mission__pk__in=operationals.values('pk'))
    if profile.user_type.code == 3 or profile.user_type.code == 5:
        query = query.filter(aviation_unit=profile.tactic_unit)
    total_count = query.count()
    percentage_results = []
    for aviation_mission in operationals:
        report_count = FlightReport.objects.filter(
            aviation_mission=aviation_mission).count()
        percentage = 0
        if total_count != 0:
            percentage = (report_count * 100) / total_count
        data = {'name': aviation_mission.name + ' - ' +
                aviation_mission.abbreviation, 'y': percentage}
        percentage_results.append(data)
    return render(request, 'graphic/graphic_pie_operational.html', {'data': mark_safe(json.dumps(percentage_results))})


@login_required(login_url=reverse_lazy('index:login'))
def graphic_pie_no_operational(request):
    user = request.user
    profile = user.profile
    no_operationals = AviationMission.objects.exclude(
        mission_type__name__icontains='Misiones Tácticas de Aviación')
    query = FlightReport.objects.filter(
        aviation_mission__pk__in=no_operationals.values('pk'))
    total_count = query.count()
    if profile.user_type.code == 3 or profile.user_type.code == 5:
        query = query.filter(aviation_unit=profile.tactic_unit)
    percentage_results = []
    for aviation_mission in no_operationals:
        report_count = FlightReport.objects.filter(
            aviation_mission=aviation_mission).count()
        percentage = 0
        if total_count != 0:
            percentage = (report_count * 100) / total_count
        data = {'name': aviation_mission.name + ' - ' +
                aviation_mission.abbreviation, 'y': percentage}
        percentage_results.append(data)
    return render(request, 'graphic/graphic_pie_no_operational.html', {'data': mark_safe(json.dumps(percentage_results))})
