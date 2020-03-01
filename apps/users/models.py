from django.db import models

class Department (models.Model):
    abbreviation = models.CharField((), max_length=50)
    name = models.CharField((), max_length=50)

    def _str_(self):
        return self.name

class Municipality (models.Model):
    department = models.ForeignKey(Department,  on_delete=models.CASCADE, related_name="municipalities")
    abbreviation = models.CharField( max_length=50)
    name = models.CharField( max_length=50)

    def _str_(self):
        return self.name

class AirCraftType (models.Model):
    name = models.CharField( max_length=50)

    def _str_(self):
        return self.name

class AirCraftModel (models.Model):
    air_craft_type = models.ForeignKey(AirCraftType, on_delete=models.CASCADE, related_name="aircraftmodels")
    name = models.CharField( max_length=50)

    def _str_(self):
        return self.name

class Aircraft (models.Model):   
    air_craft_type = models.ForeignKey(AirCraftType, on_delete=models.CASCADE, related_name="aircrafts")
    air_craft_models = models.ForeignKey(AirCraftModel, on_delete=models.CASCADE, related_name="aircrafts")
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name="aircrafts")
    enrollment = models.CharField( max_length=50,  default= None)
    assigned_hours = models.FloatField()
    fly_hours = models.FloatField()
    total_hours = models.FloatField()
    next_inspection = models.FloatField()
    next_inspection_hours = models.FloatField()
    state = models.CharField( max_length=50)

    def _str_(self):
        return self.state