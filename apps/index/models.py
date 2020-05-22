from django.contrib.auth.models import User
from django.db import models
from decimal import Decimal

# Create your models here.


class Department(models.Model):
    abbreviation = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Municipality(models.Model):
    department = models.ForeignKey(
        Department,  on_delete=models.CASCADE, related_name="municipalities")
    abbreviation = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class AirCraftType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class AirCraftModel(models.Model):
    air_craft_type = models.ForeignKey(
        AirCraftType, on_delete=models.CASCADE, related_name="aircraftmodels")
    name = models.CharField(max_length=50)
    has_pam = models.BooleanField(default=False)
    has_pilot = models.BooleanField(default=False)
    has_flight_engineer = models.BooleanField(default=False)
    has_crew_chief = models.BooleanField(default=False)
    has_flight_technician = models.BooleanField(default=False)
    has_gunner = models.BooleanField(default=False)
    has_commander = models.BooleanField(default=False)
    has_mission_operator = models.BooleanField(default=False)
    has_vehicle_operator = models.BooleanField(default=False)

    def function(self, value):
        return value

    def get_choices_charge(self):
        charge_choices = {'PAM': {'name': 'Piloto al Mando', 'value': self.has_pam},
                          'P': {'name': 'Piloto', 'value': self.has_pilot},
                          'IV': {'name': 'Ingeniero de vuelo', 'value': self.has_flight_engineer},
                          'JT': {'name': 'Jefe de Tripulacion', 'value': self.has_crew_chief},
                          'TV': {'name': 'Tecnico de vuelo', 'value': self.has_flight_technician},
                          'ART': {'name': 'Artillero', 'value': self.has_gunner},
                          'CMA': {'name': 'Comandante de misión aérea', 'value': self.has_commander},
                          'OMI': {'name': 'Operador de Mision', 'value': self.has_mission_operator},
                          'OVE': {'name': 'Operador de vehiculo', 'value': self.has_vehicle_operator}}
        current_charge_choices = {}
        for charge in charge_choices:
            if charge_choices[charge]['value']:
                current_charge_choices[charge] = charge_choices[charge]['name']
        return current_charge_choices

    def __str__(self):
        return self.name


class AirCraft(models.Model):
    air_craft_type = models.ForeignKey(
        AirCraftType, on_delete=models.CASCADE, related_name="aircraft_types")
    air_craft_models = models.ForeignKey(
        AirCraftModel, on_delete=models.CASCADE, related_name="aircraft_models")
    municipality = models.ForeignKey(
        Municipality, on_delete=models.CASCADE, related_name="aircraft_municipalities")
    enrollment = models.CharField(max_length=50, default=None)
    assigned_hours = models.FloatField()
    re_asign = models.FloatField(default=0)
    merger_hours = models.FloatField(default=0)
    hours_available = models.FloatField(default=0)
    fly_hours = models.FloatField()
    total_hours = models.FloatField()
    next_inspection = models.FloatField()
    next_inspection_hours = models.FloatField(default=0, blank=True)
    type_inspection = models.CharField(max_length=50, null=True)
    ACL = 'ACL'
    LRM = 'LRM'
    LRA = 'LRA'
    AMI = 'AMI'
    AMP = 'AMP'
    NLA = 'NLA'
    AVP = 'AVP'
    MMP = 'MMP'
    AMO = 'AMO'
    AMR = 'AMR'
    ACC = 'ACC'
    EVA = 'EVA'
    PAR = 'PAR'
    ABP = 'ABP'
    APA = 'APA'
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
        max_length=3, choices=STATUS_CHOICES)
    is_active = models.BooleanField(default=True)

    def save(self):
        # TODO check this functions
        self.next_inspection_hours = self.next_inspection - self.total_hours
        self.hours_available = self.assigned_hours + \
            self.re_asign - self.fly_hours - self.merger_hours
        super(AirCraft, self).save()

    def __str__(self):
        return "{} ({})".format(self.enrollment, self.air_craft_models)


class Rank(models.Model):
    abbreviation = models.CharField(max_length=50)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserType(models.Model):
    user_type = models.CharField(max_length=100)
    code = models.IntegerField(default=1, unique=True, error_messages={
                               'unique': "Ya existe este usuario."})

    def __str__(self):
        return self.user_type


class MajorOperativeUnit(models.Model):
    abbreviation = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    is_ejc = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.abbreviation)


class AssignedHourMajorOperationAircraftModel(models.Model):
    major_operative_unit = models.ForeignKey(
        MajorOperativeUnit,  on_delete=models.CASCADE, related_name="assigned_major_operative_unit")
    aircraft_model = models.ForeignKey(
        AirCraftModel,  on_delete=models.CASCADE, related_name="assigned_aircraft_model")
    assigned_hours = models.FloatField()

    def __str__(self):
        return '{} - {} ({})'.format(self.major_operative_unit, self.aircraft_model, self.assigned_hours)


class MinorOperativeUnit(models.Model):
    major_operative_unit = models.ForeignKey(
        MajorOperativeUnit, on_delete=models.CASCADE, related_name="major_operative_units")
    abbreviation = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    is_ejc = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.abbreviation)


class TacticUnit(models.Model):
    minor_operative_unit = models.ForeignKey(
        MinorOperativeUnit, on_delete=models.CASCADE, related_name="tactic_units")
    abbreviation = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    is_aviation = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.abbreviation)


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    rank = models.ForeignKey(
        Rank, on_delete=models.CASCADE, related_name="rank_users")
    user_type = models.ForeignKey(
        UserType, on_delete=models.CASCADE, related_name="user_type_users")
    major_operative_unit = models.ForeignKey(
        MajorOperativeUnit, on_delete=models.CASCADE, null=True, blank=True, related_name="major_operative_unit_users")
    minor_operative_unit = models.ForeignKey(
        MinorOperativeUnit, on_delete=models.CASCADE, null=True, blank=True, related_name="minor_operative_unit_users")
    tactic_unit = models.ForeignKey(
        TacticUnit, on_delete=models.CASCADE, null=True, blank=True, related_name="tactic_unit_users")

    def __str__(self):
        return self.user.username
    
    def get_unit(self):
        if self.tactic_unit is not None:
            return self.tactic_unit
        if self.minor_operative_unit is not None:
            return self.minor_operative_unit
        if self.major_operative_unit is not None:
            return self.major_operative_unit
    
    unit = property(get_unit)


class Crew(models.Model):
    rank = models.ForeignKey(
        Rank, on_delete=models.CASCADE, related_name="rank_crew")
    air_craft_type = models.ForeignKey(
        AirCraftType, on_delete=models.CASCADE, related_name="aircrafts_type_crew")
    air_craft_models = models.ForeignKey(
        AirCraftModel, on_delete=models.CASCADE, related_name="aircrafts_model_crew")
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
    PAM = 'PAM'
    PI = 'P'
    IV = 'IV'
    JT = 'JT'
    TV = 'TV'
    ART = 'ART'
    CMA = 'CMA'
    OMI = 'OMI'
    OVE = 'OVE'
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
        return "{} ({})".format(self.name, self.rank)


class MajorOperation(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Operation(models.Model):
    major_operations = models.ForeignKey(
        MajorOperation,  on_delete=models.CASCADE, related_name="major_operations")
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
    municipality = models.ForeignKey(
        Municipality,  on_delete=models.CASCADE, related_name="aviation_events_municipalities")
    is_active = models.BooleanField(default=True)
    latitude = models.DecimalField(
        max_digits=18, decimal_places=16, default=Decimal('0'))
    longitude = models.DecimalField(
        max_digits=19, decimal_places=16, default=Decimal('0'))

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
    mission_type = models.ForeignKey(
        MissionType,  on_delete=models.CASCADE, related_name="aviation_mission_type")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} {} ({})".format(self.mission_type, self.name, self.abbreviation)


class Agreement(models.Model):
    abbreviation = models.CharField(max_length=50)
    agreement_name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.agreement_name


class AssignedHourAgreementAircraftModel(models.Model):
    agreement = models.ForeignKey(
        Agreement,  on_delete=models.CASCADE, related_name="assigned_agreement")
    aircraft_model = models.ForeignKey(
        AirCraftModel,  on_delete=models.CASCADE, related_name="assigned_agreement_aircraft_model")
    assigned_hours = models.FloatField()

    def __str__(self):
        return '{} - {} ({})'.format(self.agreement, self.aircraft_model, self.assigned_hours)


class Configuration(models.Model):
    mission = models.ForeignKey(
        AviationMission,  on_delete=models.CASCADE, related_name="configurations")
    abbreviation = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class FlightReport(models.Model):
    flight_order_id = models.CharField(primary_key=True, max_length=100)
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE,
                                  null=True, blank=True, related_name="flight_reports_agreements")
    major_operative_unit = models.ForeignKey(
        MajorOperativeUnit, on_delete=models.CASCADE, null=True, blank=True, related_name="flight_reports_major_operative_units")
    minor_operative_unit = models.ForeignKey(
        MinorOperativeUnit, on_delete=models.CASCADE, null=True, blank=True, related_name="flight_reports_minor_operative_units")
    aviation_mission = models.ForeignKey(AviationMission, on_delete=models.CASCADE,
                                         null=True, blank=True, related_name="flight_reports_aviation_missions")
    configuration = models.ForeignKey(Configuration, on_delete=models.CASCADE,
                                      null=True, blank=True, related_name="flight_reports_configurations")
    aviation_event = models.ForeignKey(
        AviationEvent, on_delete=models.CASCADE, null=True, blank=True, related_name="flight_reports_events")
    municipality = models.ForeignKey(
        Municipality, on_delete=models.CASCADE, related_name="flight_reports_municipalities")
    aviation_unit = models.ForeignKey(
        TacticUnit, on_delete=models.CASCADE, related_name="flight_reports_aviation_units")
    tactic_unit = models.ForeignKey(TacticUnit, on_delete=models.CASCADE,
                                    null=True, blank=True, related_name="flight_reports_tactic_units")
    operation = models.ForeignKey(
        Operation, on_delete=models.CASCADE, related_name="flight_reports_operations")
    aircraft = models.ForeignKey(
        AirCraft, on_delete=models.CASCADE, related_name="flight_reports_aircrafts")
    flight_conditions = models.ForeignKey(
        FlightCondition, on_delete=models.CASCADE, related_name="flight_conditions")
    HIGH = 'HIGH'
    MED = 'MED'
    LOW = 'LOW'
    RISK_CHOICES = (
        (HIGH, 'RIESGO ALTO'),
        (MED, 'RIESGO MEDIO'),
        (LOW, 'RIESGO BAJO'),
    )
    risk_classification = models.CharField(
        max_length=4, choices=RISK_CHOICES, null=True, blank=True,)
    route = models.CharField(max_length=1000)
    observations = models.CharField(max_length=1000, null=True, blank=True,)
    fuel = models.FloatField(null=True, blank=True,)
    kilos = models.FloatField(null=True, blank=True,)
    sick_pt = models.IntegerField(null=True, blank=True,)
    wounded_pt = models.IntegerField(null=True, blank=True,)
    dead_pt = models.IntegerField(null=True, blank=True,)
    sick_en = models.IntegerField(null=True, blank=True,)
    wounded_en = models.IntegerField(null=True, blank=True,)
    dead_en = models.IntegerField(null=True, blank=True,)
    civil_evacuations = models.IntegerField(null=True, blank=True,)
    pax = models.IntegerField(null=True, blank=True,)
    crew_hours = models.FloatField(null=True, blank=True,)
    machine_hours = models.FloatField(null=True, blank=True,)
    time = models.TimeField()
    date = models.DateField()

    def __str__(self):
        return self.flight_order_id

    def get_charged_unit(self):
        if self.agreement is not None:
            return self.agreement
        if self.tactic_unit is not None:
            return self.tactic_unit
        if self.minor_operative_unit is not None:
            return self.minor_operative_unit
        if self.major_operative_unit is not None:
            return self.major_operative_unit

    charged_unit = property(get_charged_unit)

    def get_supported_unit(self):
        if self.agreement is not None:
            return self.agreement
        if self.major_operative_unit is not None:
            return self.major_operative_unit

    supported_unit = property(get_supported_unit)

    def save(self):
        if self.aviation_mission.abbreviation == 'RA':
            aircraft = self.aircraft
            aircraft.re_asign += self.machine_hours
            aircraft.total_hours += self.machine_hours
            aircraft.save()
        else:
            aircraft = self.aircraft
            aircraft.fly_hours += self.machine_hours
            aircraft.total_hours += self.machine_hours
            aircraft.save()
        super(FlightReport, self).save()


class AirCrew(models.Model):
    flight_reports = models.ForeignKey(
        FlightReport,  on_delete=models.CASCADE, related_name="crew_flight_report")
    crew = models.ForeignKey(
        Crew,  on_delete=models.CASCADE, related_name="air_crews")

    def __str__(self):
        return str(self.flight_reports)
