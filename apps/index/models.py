from django.contrib.auth.models import User
from django.db import models
from decimal import Decimal

# Create your models here.
class Department (models.Model):
    abbreviation = models.CharField( max_length=50)
    name = models.CharField( max_length=50)

    def __str__(self):
        return self.name

class Municipality (models.Model):
    department = models.ForeignKey(Department,  on_delete=models.CASCADE, related_name="municipalities")
    abbreviation = models.CharField( max_length=50)
    name = models.CharField( max_length=50)

    def __str__(self):
        return self.name

class AirCraftType (models.Model):
    name = models.CharField( max_length=50)

    def __str__(self):
        return self.name

class AirCraftModel (models.Model):
    air_craft_type = models.ForeignKey(AirCraftType, on_delete=models.CASCADE, related_name="aircraftmodels")
    name = models.CharField( max_length=50)

    def __str__(self):
        return self.name

class AirCraft (models.Model):   
    air_craft_type = models.ForeignKey(AirCraftType, on_delete=models.CASCADE, related_name="aircraft_types")
    air_craft_models = models.ForeignKey(AirCraftModel, on_delete=models.CASCADE, related_name="aircraft_models")
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name="aircraft_municipalities")
    enrollment = models.CharField( max_length=50,  default= None)
    assigned_hours = models.FloatField()
    fly_hours = models.FloatField()
    total_hours = models.FloatField()
    next_inspection = models.FloatField()
    next_inspection_hours = models.FloatField()
    ACL= 'ACL'
    LRM= 'LRM'
    LRA= 'LRA'
    AMI= 'AMI'
    AMP= 'AMP'
    NLA= 'NLA'
    AVP= 'AVP'
    MMP= 'MMP'
    AMO= 'AMO'
    AMR= 'AMR'
    ACC= 'ACC'
    EVA= 'EVA'
    PAR= 'PAR'
    ABP= 'ABP'
    APA= 'APA'
    STATUS_CHOICES = (
    (ACL, 'Aeronave Completamente lista'),
    (LRM, 'Aeronave Lista con Restricciones por Mantenimiento'),
    (LRA, 'Aeronave Lista con Restricciones por Abastecimiento'),
    (AMI, 'Aeronave en Mantenimiento Imprevisto'),
    (AMP, 'Aeronave en mantenimiento Programado'),
    (NLA, 'Aeronave No Lista por Abastecimientos'),
    (AVP, 'Aeronave en Vuelo de Prueba'),
    (MMP, 'Aeronave en Mantenimiento Mayor Programado'),
    (AMO, 'Aeronave en Mantenimiento Modificativo'),
    (AMR, 'Aeronave en Mantenimiento Recuperativo'),
    (ACC, 'Aeronave Accidentada'),
    (EVA, 'Aeronave en Evaluacion'),
    (PAR, 'Aeronave Pendiente Asignacion de Recursos'),
    (ABP, 'Aeronave en Proeso de Baja'),
    (APA, 'Aeronave en proceso de Alta'),
    )
    aircraft_status = models.CharField(
    max_length=3, choices=STATUS_CHOICES )
    


    def __str__(self):
        return self.aircraft_status


class Rank(models.Model):
    abbreviation = models.CharField(max_length=50)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserType(models.Model):
    user_type = models.CharField(max_length=100)

    def __str__(self):
        return self.user_type


class MajorOperativeUnit(models.Model):
    abbreviation = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    is_ejc = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.abbreviation)


class MinorOperativeUnit(models.Model):
    major_operative_unit = models.ForeignKey(MajorOperativeUnit, on_delete=models.CASCADE, related_name="minor_operative_units")
    abbreviation = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    is_ejc = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.abbreviation)


class TacticUnit(models.Model):
    minor_operative_unit = models.ForeignKey(MinorOperativeUnit, on_delete=models.CASCADE, related_name="tactic_units")
    abbreviation = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    is_aviation = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE, related_name="rank_users")
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE, related_name="user_type_users")
    tactic_unit = models.ForeignKey(TacticUnit, on_delete=models.CASCADE, related_name="tactic_unit_users")

    def __str__(self):
        return self.user.username


class Crew(models.Model):
    rank =models.ForeignKey(Rank,on_delete=models.CASCADE, related_name="rank_crew")
    air_craft_type = models.ForeignKey(AirCraftType, on_delete=models.CASCADE, related_name="aircrafts_type_crew")
    air_craft_models = models.ForeignKey(AirCraftModel, on_delete=models.CASCADE, related_name="aircrafts_model_crew")    
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
    PAM = 'PAM'
    PI = 'P'
    IV= 'IV'
    JT= 'JT'
    TV= 'TV'
    ART= 'ART'
    CMA= 'CMA'
    OMI= 'OMI'
    OVE= 'OVE'
    STATUS_CHOICES = (
    (PAM, 'Piloto al Mando'),
    (PI, 'Piloto'),
    (IV, 'Ingeniero de vuelo'),
    (JT, 'Jefe de Tripulacion'),
    (TV, 'Tecnico de vuelo'),
    (ART, 'Artillero'),
    (CMA, 'Comandante de misión aérea'),
    (OMI, 'Operador de Mision'),
    (OVE, 'Operador de vehiculo'),
    )
    flight_charge = models.CharField(max_length=3, choices=STATUS_CHOICES,)

    def __str__(self):
        return self.name




class MajorOperation(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Operation(models.Model):
    major_operations = models.ForeignKey(MajorOperation,  on_delete=models.CASCADE, related_name="major_operations")
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class FlightCondition(models.Model): 
    name = models.CharField(max_length=50) 
    initials = models.CharField(max_length=50)  
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AviationEvent(models.Model):
    DB = 'DB'
    BASH = 'BASH'
    FOD = 'FOD'
    CFIT = 'CFIT'
    CO = 'CO'
    IP = 'IP'
    NAME_CHOICES = (
        (DB, 'Daño de batalla'),
        (BASH, 'BASH - Bird/wildlife aircraft strike hazzard'),
        (FOD, 'FOD - Foreign object damage'),
        (CFIT, 'CFIT - Controlled Flight InTo Terrain'),
        (CO, 'Colision'),
        (IP, 'Incursión de pista')
    )
    name = models.CharField(max_length=4, choices=NAME_CHOICES,)
    municipality = models.ForeignKey(Municipality,  on_delete=models.CASCADE, related_name="aviation_events_municipalities")
    is_active = models.BooleanField(default=True)
    latitude = models.DecimalField(max_digits=18, decimal_places=16, default=Decimal('0'))
    longitude = models.DecimalField(max_digits=19, decimal_places=16, default=Decimal('0'))

    def __str__(self):
        return self.name


class MissionType(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AviationMission(models.Model):    
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=50)
    mission_type = models.ForeignKey(MissionType,  on_delete=models.CASCADE, related_name="aviation_mission_type")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Agreement(models.Model):
    abbreviation = models.CharField(max_length=50)
    agreement_name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.agreement_name


class Configuration(models.Model):
    mission = models.ForeignKey(AviationMission,  on_delete=models.CASCADE, related_name="configurations")
    abbreviation = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class FlightReport(models.Model):
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name="flight_reports_municipalities")

    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE, null=True, blank=True, related_name="flight_reports_agreements")
    major_operative_unit = models.ForeignKey(MajorOperativeUnit, on_delete=models.CASCADE, null=True, blank=True, related_name="flight_reports_major_operative_units")    
    aviation_mission = models.ForeignKey(AviationMission, on_delete=models.CASCADE, null=True, blank=True, related_name="flight_reports_aviation_missions")
    configuration = models.ForeignKey(Configuration, on_delete=models.CASCADE, null=True, blank=True, related_name="flight_reports_configurations")
    
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE, related_name="flight_reports_crew")
    tactic_unit = models.ForeignKey(TacticUnit, on_delete=models.CASCADE, related_name="flight_reports_tactic_units")
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name="flight_reports_operations")
    aircraft = models.ForeignKey(AirCraft, on_delete=models.CASCADE, related_name="flight_reports_aircrafts")
    aviation_event = models.ForeignKey(AviationEvent, on_delete=models.CASCADE, related_name="flight_reports_events")
    
    observations = models.CharField(max_length=50)
    fuel = models.FloatField()
    kilos = models.FloatField()
    sick_pt =  models.IntegerField()
    wounded_pt =  models.IntegerField()
    dead_pt =  models.IntegerField()
    sick_en =  models.IntegerField()
    wounded_en =  models.IntegerField()
    dead_en =  models.IntegerField()
    civil_evacuations = models.IntegerField()
    pax = models.IntegerField()
    flight_conditions = models.ForeignKey(FlightCondition, on_delete=models.CASCADE, related_name="flight_conditions")
    crew_hours = models.FloatField()
    machine_hours = models.FloatField()
    time = models.TimeField() 
    date = models.DateField()
    
class AirCrew(models.Model):
    flight_reports = models.ForeignKey(FlightReport,  on_delete=models.CASCADE, related_name="configurations")
    crew = models.ForeignKey(Crew,  on_delete=models.CASCADE, related_name="air_crews")

    def __str__(self):
        return self.name