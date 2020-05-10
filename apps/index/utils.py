from openpyxl.styles import Color, PatternFill, Font, Border, Alignment, Side
from django.http.response import HttpResponse
from django.views.generic import TemplateView
from openpyxl.utils import get_column_letter
from openpyxl.styles import colors
from django.db.models import Sum
from apps.index.models import * 
from openpyxl.cell import Cell
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

                #cell =  ws.cell(row=cont,column=5)
                #cell.alignment = centered_alignment  
                #ws.cell(row=cont,column=5).value = flightReport.tactic_unit.minor_operative_unit.abbreviation

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
                aviation_event = '---'
                if flightReport.aviation_event is not None:
                    aviation_event = flightReport.aviation_event.name
                ws.cell(row=cont,column=46).value = aviation_event

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


        filename ="ReporteDeAeronavesExcel.xlsx"
        response = HttpResponse(content_type="application/ms-excel")
        content = "attachment; filename={0}".format(filename)
        response["Content-Disposition"]= content

        
        wb.save(response)       
        return response 


def get_assisted_unit(data):
    result = {}
    if data['agreement'] is not None:
        result['assisted_unit'] = data['agreement']
        result['assisted_unit__name'] = data['agreement__agreement_name']
        result['assisted_unit__abbreviation'] = data['agreement__abbreviation']
    elif data['tactic_unit'] is not None:
        result['assisted_unit'] = data['tactic_unit']
        result['assisted_unit__name'] = data['tactic_unit__name']
        result['assisted_unit__abbreviation'] = data['tactic_unit__abbreviation']
    elif data['minor_operative_unit'] is not None:
        result['assisted_unit'] = data['minor_operative_unit']
        result['assisted_unit__name'] = data['minor_operative_unit__name']
        result['assisted_unit__abbreviation'] = data['minor_operative_unit__abbreviation']
    elif data['major_operative_unit'] is not None:
        result['assisted_unit'] = data['major_operative_unit']
        result['assisted_unit__name'] = data['major_operative_unit__name']
        result['assisted_unit__abbreviation'] = data['major_operative_unit__abbreviation']
    return result


def get_default_hours(aircraft_models):
    default_hours_model = {}
    for aircraft_model in aircraft_models:
        hours_result = {}
        hours_result['aircraft__assigned_hours__sum'] = 0
        hours_result['aircraft__fly_hours__sum'] = 0
        hours_result['aircraft__hours_available__sum'] = 0
        default_hours_model[aircraft_model.pk] = hours_result
    return default_hours_model


class ExcelHoursAircraft(TemplateView):

    def get(self, request, *args, **kwargs):
        aircraft_models = AirCraftModel.objects.all().order_by('name')
        aircraft_models_dict = {}
        aviation_units = TacticUnit.objects.filter(
            is_aviation=True).order_by('pk')
        count_aviation = {}
        real_query = {}
        total_hours = get_default_hours(aircraft_models)
        for aviation_unit in aviation_units:
            count_aviation[aviation_unit.pk] = 0
        for aircraft_model in aircraft_models:
            flight_reports = FlightReport.objects.filter(
                aircraft__air_craft_models=aircraft_model).select_related().order_by('tactic_unit')
            queryset = flight_reports.values('aviation_unit', 'aviation_unit__name', 'aviation_unit__abbreviation', 'agreement', 'agreement__abbreviation', 'agreement__agreement_name', 'major_operative_unit', 'major_operative_unit__name', 'major_operative_unit__abbreviation',
                                             'minor_operative_unit', 'minor_operative_unit__name', 'minor_operative_unit__abbreviation', 'tactic_unit', 'tactic_unit__name', 'tactic_unit__abbreviation').order_by('aviation_unit').annotate(aircraft__assigned_hours__sum=Sum('aircraft__assigned_hours'), aircraft__fly_hours__sum=Sum('aircraft__fly_hours'), aircraft__hours_available__sum=Sum('aircraft__hours_available'))
            list_result = []
            # print(queryset.count())
            results_aviation = {}
            count_aviation = {}
            for aviation_unit in aviation_units:
                results_aviation[aviation_unit.pk] = []
                count_aviation[aviation_unit.pk] = 0
            for data in queryset:
                result = get_assisted_unit(data)
                result['aviation_unit'] = data['aviation_unit']
                result['aviation_unit__abbreviation'] = data['aviation_unit__abbreviation']
                result['aviation_unit__name'] = data['aviation_unit__name']
                hours_result = {}
                hours_result['aircraft__assigned_hours__sum'] = data['aircraft__assigned_hours__sum']
                hours_result['aircraft__fly_hours__sum'] = data['aircraft__fly_hours__sum']
                hours_result['aircraft__hours_available__sum'] = data['aircraft__hours_available__sum']
                key_query = str(result['aviation_unit']) + \
                    '_' + result['assisted_unit__abbreviation']
                if key_query in real_query:
                    real_query[key_query]['aicraft_models'][aircraft_model.pk]['aircraft__assigned_hours__sum'] += hours_result[
                        'aircraft__assigned_hours__sum']
                    real_query[key_query]['aicraft_models'][aircraft_model.pk]['aircraft__fly_hours__sum'] += hours_result[
                        'aircraft__fly_hours__sum']
                    real_query[key_query]['aicraft_models'][aircraft_model.pk]['aircraft__hours_available__sum'] += hours_result[
                        'aircraft__hours_available__sum']
                else:
                    result['aicraft_models'] = get_default_hours(
                        aircraft_models)
                    result['aicraft_models'][aircraft_model.pk] = hours_result
                    real_query[key_query] = result
                total_hours[aircraft_model.pk]['aircraft__assigned_hours__sum'] += hours_result['aircraft__assigned_hours__sum']
                total_hours[aircraft_model.pk]['aircraft__fly_hours__sum'] += hours_result['aircraft__fly_hours__sum']
                total_hours[aircraft_model.pk]['aircraft__hours_available__sum'] += hours_result['aircraft__hours_available__sum']
        # full_aviation_units = []
        # for aviation_unit in aviation_units:
        #     for count in range(count_aviation[aviation_unit.pk]+1):
        #         full_aviation_units.append(aviation_unit)
        real_query = dict(sorted(real_query.items()))
        wb = Workbook()
        #name = aircratf.name
        ws = wb.active
        ws.title = "Horas Unidades"
        ws.row_dimensions[1].height = 50
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
        redFill = PatternFill(start_color='ff0000',
                              end_color='ff0000',
                              fill_type='solid')

        bluefill = PatternFill(start_color='8db3e2',
                               end_color='8db3e2',
                               fill_type='solid')
        columns = [
            '    UNIDAD DE AVIACIÓN ',
            '    UNIDAD APOYADA',
        ]

        second_columns = [
            '    UNIDAD DE AVIACIÓN ',
            '    UNIDAD APOYADA',
        ]

        columns_count = 3

        for aircraft_model in aircraft_models:
            columns.append(aircraft_model.name)
            columns.append('')
            columns.append('')
            # Second columns
            second_columns.append('ASIG')
            second_columns.append('VOL')
            second_columns.append('DISP')

        column_widths = {}
        cont = 1
        for col_num, column_title in enumerate(columns, 1):
            cell = ws.cell(row=cont, column=col_num)
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
            # Second columns
            cell = ws.cell(row=cont+1, column=col_num)
            cell.value = second_columns[col_num-1]
            cell.border = border_bottom
            cell.alignment = centered_alignment
            cell.alignment = wrapped_alignment
            cell.fill = bluefill
            column_letter = get_column_letter(col_num)
            if column_letter not in column_widths:
                column_widths[column_letter] = 0
            if len(str(second_columns[col_num-1])) >= column_widths[column_letter]:
                column_widths[column_letter] = len(
                    str(second_columns[col_num-1])) + 1
        cont += 1
        # ws.merge_cells(start_row=1, start_column=1, end_row=2, end_column=1)
        # ws.merge_cells(start_row=1, start_column=2, end_row=2, end_column=2)

        columns_count = 2
        for aircraft_model in aircraft_models:
            columns_count += 1
            ws.merge_cells(start_row=1, start_column=columns_count,
                           end_row=1, end_column=columns_count+2)
            columns_count += 2

        # Table Rows
        for key, row_table in real_query.items():
            cont += 1
            row = [
                row_table['aviation_unit__abbreviation'],
                row_table['assisted_unit__abbreviation'],
            ]

            for air_key, aircraft_model in row_table['aicraft_models'].items():
                row.append(aircraft_model['aircraft__assigned_hours__sum'])
                row.append(aircraft_model['aircraft__fly_hours__sum'])
                row.append(aircraft_model['aircraft__hours_available__sum'])

            for col_num, column_title in enumerate(row, 1):
                cell = ws.cell(row=cont, column=col_num)
                cell.value = column_title
                cell.alignment = wrapped_alignment
                if col_num <= 2:
                    cell.fill = bluefill
                cell.border = border_bottom
                column_letter = get_column_letter(col_num)
                if column_letter not in column_widths:
                    column_widths[column_letter] = 0
                if len(str(column_title)) >= column_widths[column_letter]:
                    column_widths[column_letter] = len(str(column_title)) + 1

        cont += 1
        # Total Row
        row = [
            '  TOTAL  ',
            '  TOTAL  ',
        ]

        for total_key, total in total_hours.items():
            row.append(total['aircraft__assigned_hours__sum'])
            row.append(total['aircraft__fly_hours__sum'])
            row.append(total['aircraft__hours_available__sum'])

        for col_num, column_title in enumerate(row, 1):
            cell = ws.cell(row=cont, column=col_num)
            cell.value = column_title
            cell.alignment = wrapped_alignment
            cell.fill = bluefill
            cell.border = border_bottom
            column_letter = get_column_letter(col_num)
            if column_letter not in column_widths:
                column_widths[column_letter] = 0
            if len(str(column_title)) >= column_widths[column_letter]:
                column_widths[column_letter] = len(str(column_title)) + 1

        ws.merge_cells(start_row=cont, start_column=1,
                       end_row=cont, end_column=2)

        # merge columns 1 and 2
        for col_num in range(2):
            col_num += 1
            cell = ws.cell(row=1, column=col_num)
            cell_value = cell.value
            cell_row = 1
            for row_count in range(len(real_query)+1):
                row_count += 2
                cell = ws.cell(row=row_count, column=col_num)
                current_cell_value = cell.value
                if current_cell_value != cell_value:
                    cell_value = current_cell_value
                    ws.merge_cells(start_row=cell_row, start_column=col_num,
                                   end_row=row_count-1, end_column=col_num)
                    cell_row = row_count
            ws.merge_cells(start_row=cell_row, start_column=col_num,
                           end_row=row_count, end_column=col_num)

        filename = "ReporteDeAeronaveExcel.xlsx"
        response = HttpResponse(content_type="application/ms-excel")
        content = "attachment; filename={0}".format(filename)
        response["Content-Disposition"] = content

        wb.save(response)
        return response
