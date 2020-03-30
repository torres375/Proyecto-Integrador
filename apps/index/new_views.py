def generar_excel_actividades(actividades, date):
    # Set response Headers and content
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename={datefile}-actividades.xlsx'.format(
        datefile=date.strftime('%Y-%m-%d'),
    )
    response['Access-Control-Expose-Headers'] = 'Content-Disposition'

    # CREATE FILE
    # USERS WORKSHEET
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Peticiones'
    centered_alignment = Alignment(horizontal='center')
    border_bottom = Border(left=Side(border_style='medium',
                                     color='FF000000'),
                           right=Side(border_style='medium',
                                      color='FF000000'),
                           top=Side(border_style='medium',
                                    color='FF000000'),
                           bottom=Side(border_style='medium',
                                       color='FF000000'),
                           outline=Side(border_style='medium',
                                        color='FF000000'),
                           vertical=Side(border_style='medium',
                                         color='FF000000'),
                           horizontal=Side(border_style='medium',
                                           color='FF000000')
                           )
    wrapped_alignment = Alignment(
        horizontal='general',
        vertical='top',
        wrap_text=True,
        shrink_to_fit=True
    )

    columns = [
        'Nombre solicitante',
        'Número de empleado',
        'Número de teléfono',
        'Fecha de la actividad',
        'Nombre Actividad',
    ]

    row_num = 1
    column_widths = {}
    count_actividades = actividades.count()
    footer_usuarios = 'Para el día ' + date.strftime('%Y-%m-%d') + ' existen ' + \
        str(count_actividades) + \
        ' peticiones.'

    dimo_cell = "Lista."
    # DIMO title
    worksheet.merge_cells(
        start_row=row_num, start_column=1, end_row=row_num+1, end_column=len(columns))
    cell = worksheet.cell(row=row_num, column=1)
    cell.value = dimo_cell
    cell.alignment = wrapped_alignment
    cell.border = border_bottom
    row_num += 2

    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title
        cell.border = border_bottom
        cell.alignment = centered_alignment
        column_letter = get_column_letter(col_num)
        if column_letter not in column_widths:
            column_widths[column_letter] = 0
        if len(str(column_title)) >= column_widths[column_letter]:
            column_widths[column_letter] = len(str(column_title)) + 2

    for peticion in actividades:
        row_num += 1

        convenio = peticion.convenio
        user = peticion.usuario
        n_telefono = '---'
        if user.n_telefono:
            n_telefono = n_telefono
        fecha_bono = '---'
        if peticion.fecha_bono is not None:
            fecha_bono = peticion.fecha_bono.strftime('%Y-%m-%d')
        row = [
            user.user.get_full_name(),
            user.n_empleado,
            n_telefono,
            fecha_bono,
            convenio.nombre_empresa + ' ' + convenio.ciudad
        ]

        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value
            cell.alignment = wrapped_alignment
            column_letter = get_column_letter(col_num)
            if column_letter not in column_widths:
                column_widths[column_letter] = 0
            if len(str(cell_value)) >= column_widths[column_letter]:
                column_widths[column_letter] = len(str(cell_value)) + 2

    for col_num, column_title in enumerate(columns, 1):
        column_letter = get_column_letter(col_num)
        column_dimensions = worksheet.column_dimensions[column_letter]
        column_dimensions.width = column_widths[column_letter]

    worksheet.merge_cells(
        start_row=row_num+1, start_column=1, end_row=row_num+2, end_column=len(columns))
    cell = worksheet.cell(row=row_num+1, column=1)
    cell.value = footer_usuarios
    cell.alignment = wrapped_alignment

    workbook.save(response)

    return response