from django.http.response import HttpResponse
from django.views.generic import TemplateView
from apps.index.models import * 
from openpyxl.styles import Color, PatternFill, Font, Border, Alignment, Side    
from openpyxl.styles import colors
from openpyxl.cell import Cell
from openpyxl.utils import get_column_letter
from openpyxl import Workbook

def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


class ReportAircratfExcel(TemplateView):
  
    def get(self, request, *args, **kwargs):
        aircratf_model = AirCraftModel.objects.all()        
        crew = Crew.objects.all()
        wb = Workbook()
       
        
        for aircratf_model in  aircratf_model:
            name = aircratf_model.name
            flightreport = FlightReport.objects.all().filter(aircraft__air_craft_models__name=name)                 
            
            ws = wb.active         
            ws = wb.create_sheet(name)
            ws.title = name         
            print(ws)

            ws.row_dimensions[1].height = 50


            redFill = PatternFill(start_color='ff0000',
                                    end_color='ff0000',
                                    fill_type='solid')

            bluefill = PatternFill(start_color='8db3e2',
                                    end_color='8db3e2',
                                    fill_type='solid')                     

            centered_alignment = Alignment(horizontal='center')  
            border_bottom = Border(left=Side(border_style='medium',
                                                color='00000000'),
                                    right=Side(border_style='medium',
                                                color='00000000'),
                                    top=Side(border_style='medium',
                                                color='00000000'),
                                    bottom=Side(border_style='medium',
                                                color='00000000'),
                                    vertical=Side(border_style='medium',
                                                color='00000000'),
                                    horizontal=Side(border_style='medium',
                                                color='00000000'),
                                    )
            wrapped_alignment = Alignment(
                horizontal='general',
                vertical='center',
                wrap_text=True,
                shrink_to_fit=True
            )

            

            columns = [
                '    FECHA    ',
                '   HORA   ',
                '   UNIDAD DE AVIACION   ',
                'DIVISION/CONVENIO/FUERZA DE TAREA A QUIEN VAN CARGADAS LAS HORAS',
                '      UNIDAD OPERATIVA MENOR APOYADA      ',
                '   MATRICULA   ',
                '          TIPO MISIÓN          ',
                '   CONFIGURACION  ',
                '   CLASIFICACION DEL RIESGO   ',
                '   HRS MAQUINA   ',
                '   HRS TRIPULACION   ',
                '   OPERACIÓN MAYOR   ',
                '   NOMBRE DE LA OPERACION   ',
                '   DEPARTAMENTO   ',
                '   MUNICIPIO   ',
                '   RUTA   ',
                '   PAX   ',
                'ENFERMOS PROPIAS TROPAS',
                'HERIDOS PROPIAS TROPAS',
                'MUERTOS PROPIAS TROPAS',
                '   ENFERMOS ENEMIGO   ',
                '   HERIDOS ENEMIGO   ',
                '   MUERTOS ENEMIGO   ',
                '   EVACUACION CIVILES   ',
                '   KILOS   ',
                '   COMBUSTIBLE   ',
                '   PAM   ',
                '    ',
                '   P   ',
                '   ',
                '   IV  ',
                '   ',
                '   JT   ',
                '    ',
                '   TV   ',
                '    ',
                '   ART   ',
                '   ',
                '   CMA   ',
                '   ',
                '   OMI  ',
                '   ',
                '   OVE  ',
                '   ',
                '   ORDEN DE VUELO   ',
                '   EVENTO DE AVIACIÓN  ',
                '   OBSERVACIONES  ',
            ]

            column_widths = {} 
            cont =1
            for col_num, column_title in enumerate(columns,1):
                cell = ws.cell(row=cont,column=col_num)
                cell.value = column_title
                cell.border = border_bottom
                cell.alignment = centered_alignment
                cell.alignment = wrapped_alignment
                cell.fill = bluefill
                column_letter = get_column_letter(col_num)
                if column_letter not in column_widths:
                    column_widths[column_letter] = 0
                if len(str(column_title)) >= column_widths[column_letter]:
                    column_widths[column_letter] = len(str(column_title)) + 1            
                

            ws['A1'].fill = redFill
            ws['C1'].fill = redFill
            ws['D1'].fill = redFill
            ws['G1'].fill = redFill
            ws['H1'].fill = redFill
            
            ws.merge_cells('AE1:AF1')
            ws.merge_cells('AG1:AH1')
            ws.merge_cells('AI1:AJ1')
            ws.merge_cells('AK1:AL1')
            ws.merge_cells('AM1:AN1')
            ws.merge_cells('AO1:AP1')
            ws.merge_cells('AQ1:AR1')

            cont = 2
            for flightReport in flightreport:      
                cell =  ws.cell(row=cont,column=1)
                cell.alignment = centered_alignment  
                ws.cell(row=cont,column=1).value = flightReport.date

                cell =  ws.cell(row=cont,column=2)
                cell.alignment = centered_alignment
                ws.cell(row=cont,column=2).value = flightReport.time

                cell =  ws.cell(row=cont,column=3)
                cell.alignment = centered_alignment
                ws.cell(row=cont,column=3).value = flightReport.aviation_unit.abbreviation

                cell =  ws.cell(row=cont,column=4)
                cell.alignment = centered_alignment
                ws.cell(row=cont,column=4).value = flightReport.charged_unit.abbreviation

                cell =  ws.cell(row=cont,column=5)
                cell.alignment = centered_alignment  
                ws.cell(row=cont,column=5).value = flightReport.tactic_unit.minor_operative_unit.abbreviation

                cell =  ws.cell(row=cont,column=6)
                cell.alignment = centered_alignment  
                ws.cell(row=cont,column=6).value = flightReport.aircraft.enrollment

                cell =  ws.cell(row=cont,column=7)
                cell.alignment = centered_alignment  
                ws.cell(row=cont,column=7).value = flightReport.aviation_mission.mission_type.name

                cell =  ws.cell(row=cont,column=8)
                cell.alignment = centered_alignment
                ws.cell(row=cont,column=8).value = flightReport.configuration.abbreviation

                cell =  ws.cell(row=cont,column=9)
                cell.alignment = centered_alignment  
                ws.cell(row=cont,column=9).value = flightReport.get_risk_classification_display()

                cell =  ws.cell(row=cont,column=10)
                cell.alignment = centered_alignment  
                ws.cell(row=cont,column=10).value = flightReport.machine_hours

                cell =  ws.cell(row=cont,column=11)
                cell.alignment = centered_alignment  
                ws.cell(row=cont,column=11).value = flightReport.crew_hours

                cell =  ws.cell(row=cont,column=12)
                cell.alignment = centered_alignment  
                ws.cell(row=cont,column=12).value = flightReport.operation.major_operations.name

                cell =  ws.cell(row=cont,column=13)
                cell.alignment = centered_alignment  
                ws.cell(row=cont,column=13).value = flightReport.operation.name

                cell =  ws.cell(row=cont,column=14)
                cell.alignment = centered_alignment 
                ws.cell(row=cont,column=14).value = flightReport.municipality.department.name

                cell =  ws.cell(row=cont,column=15)
                cell.alignment = centered_alignment 
                ws.cell(row=cont,column=15).value = flightReport.municipality.name

                cell =  ws.cell(row=cont,column=16)
                cell.alignment = centered_alignment 
                ws.cell(row=cont,column=16).value = flightReport.route

                cell =  ws.cell(row=cont,column=17)
                cell.alignment = centered_alignment 
                ws.cell(row=cont,column=17).value = flightReport.pax

                cell =  ws.cell(row=cont,column=18)
                cell.alignment = centered_alignment  
                ws.cell(row=cont,column=18).value = flightReport.sick_pt

                cell =  ws.cell(row=cont,column=19)
                cell.alignment = centered_alignment 
                ws.cell(row=cont,column=19).value = flightReport.wounded_pt

                cell =  ws.cell(row=cont,column=20)
                cell.alignment = centered_alignment  
                ws.cell(row=cont,column=20).value = flightReport.dead_pt

                cell =  ws.cell(row=cont,column=21)
                cell.alignment = centered_alignment  
                ws.cell(row=cont,column=21).value = flightReport.sick_en

                cell =  ws.cell(row=cont,column=22)
                cell.alignment = centered_alignment  
                ws.cell(row=cont,column=22).value = flightReport.wounded_en

                cell =  ws.cell(row=cont,column=23)
                cell.alignment = centered_alignment  
                ws.cell(row=cont,column=23).value = flightReport.dead_en

                cell =  ws.cell(row=cont,column=24)
                cell.alignment = centered_alignment  
                ws.cell(row=cont,column=24).value = flightReport.civil_evacuations

                cell =  ws.cell(row=cont,column=25)
                cell.alignment = centered_alignment  
                ws.cell(row=cont,column=25).value = flightReport.kilos

                cell =  ws.cell(row=cont,column=26)
                cell.alignment = centered_alignment  
                ws.cell(row=cont,column=26).value = flightReport.fuel

                crew = flightReport.crew_flight_report.all()
                print(crew)

                pam = crew.filter(crew__flight_charge=Crew.PAM)
                print(pam)
                if pam.count() > 0:
                    pam = pam.first()
                    cell =  ws.cell(row=cont,column=27)
                    cell.alignment = centered_alignment  
                    ws.cell(row=cont,column=27).value = pam.crew.rank.abbreviation
                    cell =  ws.cell(row=cont,column=28)
                    cell.alignment = centered_alignment  
                    ws.cell(row=cont,column=28).value = pam.crew.name
                
                p = crew.filter(crew__flight_charge=Crew.PI)
                if p.count() > 0:
                    p = p.first()
                    cell =  ws.cell(row=cont,column=29)
                    cell.alignment = centered_alignment  
                    ws.cell(row=cont,column=29).value = p.crew.rank.abbreviation
                    cell =  ws.cell(row=cont,column=30)
                    cell.alignment = centered_alignment  
                    ws.cell(row=cont,column=30).value = p.crew.name
                
                iv = crew.filter(crew__flight_charge=Crew.IV)
                if iv.count() > 0:
                    iv = iv.first()
                    cell =  ws.cell(row=cont,column=31)
                    cell.alignment = centered_alignment  
                    ws.cell(row=cont,column=31).value = iv.crew.rank.abbreviation
                    cell =  ws.cell(row=cont,column=32)
                    cell.alignment = centered_alignment  
                    ws.cell(row=cont,column=32).value = iv.crew.name
                
                jt = crew.filter(crew__flight_charge=Crew.JT)
                if jt.count() > 0:
                    jt = jt.first()
                    cell =  ws.cell(row=cont,column=33)
                    cell.alignment = centered_alignment  
                    ws.cell(row=cont,column=33).value = jt.crew.rank.abbreviation
                    cell =  ws.cell(row=cont,column=34)
                    cell.alignment = centered_alignment  
                    ws.cell(row=cont,column=34).value = jt.crew.name
                
                tv = crew.filter(crew__flight_charge=Crew.TV)
                if tv.count() > 0:
                    tv = tv.first()
                    cell =  ws.cell(row=cont,column=35)
                    cell.alignment = centered_alignment  
                    ws.cell(row=cont,column=35).value = tv.crew.rank.abbreviation
                    cell =  ws.cell(row=cont,column=36)
                    cell.alignment = centered_alignment  
                    ws.cell(row=cont,column=36).value = tv.crew.name
                
                art = crew.filter(crew__flight_charge=Crew.ART)
                if art.count() > 0:
                    art = art.first()
                    cell =  ws.cell(row=cont,column=37)
                    cell.alignment = centered_alignment  
                    ws.cell(row=cont,column=37).value = art.crew.rank.abbreviation
                    cell =  ws.cell(row=cont,column=38)
                    cell.alignment = centered_alignment  
                    ws.cell(row=cont,column=38).value = art.crew.name
                
                cma = crew.filter(crew__flight_charge=Crew.CMA)
                if cma.count() > 0:
                    cma = cma.first()
                    cell =  ws.cell(row=cont,column=39)
                    cell.alignment = centered_alignment  
                    ws.cell(row=cont,column=39).value = cma.crew.rank.abbreviation
                    cell =  ws.cell(row=cont,column=40)
                    cell.alignment = centered_alignment  
                    ws.cell(row=cont,column=40).value = cma.crew.name
                
                omi = crew.filter(crew__flight_charge=Crew.OMI)
                if omi.count() > 0:
                    omi = omi.first()
                    cell =  ws.cell(row=cont,column=41)
                    cell.alignment = centered_alignment  
                    ws.cell(row=cont,column=41).value = omi.crew.rank.abbreviation
                    cell =  ws.cell(row=cont,column=42)
                    cell.alignment = centered_alignment  
                    ws.cell(row=cont,column=42).value = omi.crew.name
                
                ove = crew.filter(crew__flight_charge=Crew.OVE)
                if ove.count() > 0:
                    ove = ove.first()
                    cell =  ws.cell(row=cont,column=43)
                    cell.alignment = centered_alignment  
                    ws.cell(row=cont,column=43).value = ove.crew.rank.abbreviation
                    cell =  ws.cell(row=cont,column=44)
                    cell.alignment = centered_alignment  
                    ws.cell(row=cont,column=44).value = ove.crew.name

                cell =  ws.cell(row=cont,column=45)
                cell.alignment = centered_alignment  
                ws.cell(row=cont,column=45).value = flightReport.flight_order_id

                cell =  ws.cell(row=cont,column=46)
                cell.alignment = centered_alignment  
                ws.cell(row=cont,column=46).value = flightReport.aviation_event.name

                cell =  ws.cell(row=cont,column=47)
                cell.alignment = centered_alignment  
                ws.cell(row=cont,column=47).value = flightReport.observations

                for col_num, column_title in enumerate(columns,1):
                    cell = ws.cell(row=cont,column=col_num)
                    column_letter = get_column_letter(col_num)
                    if column_letter not in column_widths:
                        column_widths[column_letter] = 0
                    if len(str(cell.value)) >= column_widths[column_letter]:
                        column_widths[column_letter] = len(str(cell.value)) + 1            
                
                cont = cont + 1

            for col_num, column_title in enumerate(columns, 1):
                column_letter = get_column_letter(col_num)
                column_dimensions = ws.column_dimensions[column_letter]
                column_dimensions.width = column_widths[column_letter]

        ws.merge_cells(
            start_row=cont+1, start_column=1, end_row=cont+2, end_column=len(columns))
        cell = ws.cell(row=cont+1, column=1)
        #cell.value = footer_usuarios
        cell.alignment = wrapped_alignment


        filename ="ReporteDeAeronaveExcel.xlsx"
        response = HttpResponse(content_type="application/ms-excel")
        content = "attachment; filename={0}".format(filename)
        response["Content-Disposition"]= content

        
        wb.save(response)       
        return response 