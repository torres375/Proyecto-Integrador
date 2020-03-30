from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from apps.index.models import *
from django import forms


class AirCraftForm(forms.ModelForm):
    municipality = forms.ModelChoiceField(queryset=Municipality.objects.none())
    class Meta:
        model = AirCraft
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super(AirCraftForm, self).__init__(*args, **kwargs)
        self.fields['municipality'].queryset = Municipality.objects.none()
        # print(self.fields['municipality'].queryset)
        # self.fields['department']=forms.ModelChoiceField(queryset= Department.objects.all())


class CrewForm(forms.ModelForm): 
    class Meta:
        model = Crew 
        fields = ('__all__')


class MajorOperativeUnitForm(forms.ModelForm):
    class Meta:
        model = MajorOperativeUnit 
        fields = ('__all__')


class MinorOperativeUnitForm(forms.ModelForm):
    class Meta:
        model = MinorOperativeUnit 
        fields = ('__all__')


class TacticUnitForm(forms.ModelForm):
    
    class Meta:
        model = TacticUnit 
        fields = ('__all__')
   


class MajorOperationForm(forms.ModelForm):
    class Meta:
        model = MajorOperation 
        fields = ('__all__')


class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation 
        fields = ('__all__')


class FlightConditionForm(forms.ModelForm):
    class Meta:
        model = FlightCondition 
        fields = ('__all__')


class AgreementForm(forms.ModelForm):
    class Meta:
        model = Agreement 
        fields = ('__all__')


class AirCraftTypeForm(forms.ModelForm):
    class Meta:
        model = AirCraftType 
        fields = ('__all__')


class AirCraftModelForm(forms.ModelForm):
    class Meta:
        model = AirCraftModel 
        fields = ('__all__')


class AviationEventForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.none())
    latitude = forms.DecimalField(max_digits=18, decimal_places=16, validators=[MaxValueValidator(90), MinValueValidator(-90)])
    longitude = forms.DecimalField(max_digits=19, decimal_places=16, validators=[MaxValueValidator(180), MinValueValidator(-180)])

    class Meta:
        model = AviationEvent 
        fields = ('__all__')


class MissionTypeForm(forms.ModelForm):
    class Meta:
        model = MissionType 
        fields = ('__all__')


class AviationMissionForm(forms.ModelForm):
    class Meta:
        model = AviationMission 
        fields = ('__all__')


class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = Configuration 
        fields = ('__all__')


#Javi
  


class FlightReportForm(forms.ModelForm):
    municipality = forms.ModelChoiceField(queryset=Municipality.objects.none())
    major_operative_unit = forms.CharField(max_length=255, required=False)
    agreement = forms.CharField( max_length= 255, required=False)
    date = forms.DateField( input_formats=['%d/%m/%Y'])
    time = forms.TimeField( input_formats=['%I:%M %p'])
    class Meta:
        model = FlightReport 
        fields = ('__all__')
        
    def __init__(self, *args, **kwargs):
        super(FlightReportForm,self).__init__(*args, **kwargs)
        self.fields['municipality'].queryset = Municipality.objects.none()

    
    def clean(self):
        cleaned_data = super(FlightReportForm, self).clean(*args, **kwargs)
        minor_operative_unit = self.cleaned_data['minor_operative_unit']
        agreement = self.cleaned_data['agreement']    
        error_messages = ""
        
        if major_operative_unit and agreement is None:
            error_messages = 'Span must be less than or equal to Maximum Span'
            self._errors["span"] = "Please enter a valid span"
        raise forms.ValidationError(' & '.join(error_messages))

        return self.error_messages




    ##def clean(self, *args, **kwargs):    
      ##  cleaned_data = super(FlightReportForm, self).clean(*args, **kwargs)
       ## major_operative_unit = cleaned_data.get('major_operative_unit', None)
        ##agreement = cleaned_data.get('agreement', None)

        ##if major_operative_unit and agreement is None:
          # major_operative_unit = forms.CharField( max_length=255, required=True)
           #agreement = forms.CharField( max_length= 255, required=True)
            
            
        #self.fields['agreement'].required = False    
        #self.fields['major_operative_unit'].required = False