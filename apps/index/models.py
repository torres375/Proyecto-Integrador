from django.db import models

# Create your models here.
class UnidadesOperativasMayores(models.Model):
    abbreviation = models.CharField((), max_length=50)
    name_uoma = models.CharField((), max_length=50)
    ejc= models.BooleanField(())
    ability = models.BooleanField(())

class UnidadesOperativasMenores(models.Model):
    unity = models.ForeignKey(UnidadesOperativasMayores, on_delete=models.CASCADE)
    abbreviation = models.CharField((), max_length=50)
    name_uoma = models.CharField((), max_length=50)
    ejc= models.BooleanField(())
    ability = models.BooleanField(())

class Tactica(models.Model):
    unity = models.ForeignKey(UnidadesOperativasMenores, on_delete=models.CASCADE)
    abbreviation = models.CharField((), max_length=50)
    name_ut = models.CharField((), max_length=50)
    ut_aviacion = models.BooleanField(())
    ability = models.BooleanField(())

class Grades(models.Model):
    abbreviation = models.CharField((), max_length=50)
    grade_name = models.CharField((), max_length=50) 

class UserType(models.Model):
    type1 =  models.CharField((), max_length=50)

class Users(models.Model):
    grades = models.ForeignKey(Grades, on_delete=models.CASCADE)
    unity = models.ForeignKey(Tactica, on_delete=models.CASCADE)
    user_type1 = models.ForeignKey(UserType, on_delete=models.CASCADE)
    name = models.CharField((), max_length=50)
    email = models.CharField((), max_length=50)
    password = models.CharField((), max_length=50)
    state = models.CharField((), max_length=50)