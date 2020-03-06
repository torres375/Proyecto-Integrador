
from apps.index.models import *
from apps.index.utils import *
import pandas as pd

def deps_script():
    xls = pd.ExcelFile("deps.xlsx")
    sheetX = xls.parse(0)
    departamento = None
    department = None
    for index, row in sheetX.iterrows():
        row = row.fillna(value='')
        if row['Departamento']:
            department = None
            departamento = row['Departamento']
            department = get_or_none(Department, name=departamento)
            if department is None:
                department = Department.objects.create(name=departamento, abbreviation=departamento)
        name_mun = row['Nombre']
        mun = get_or_none(Municipality, department=department, name=name_mun)
        if mun is None:
            Municipality.objects.create(name=name_mun, department=department, abbreviation=name_mun)