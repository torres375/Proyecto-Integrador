$(document).ready(function() {
    $('#datatables').DataTable({
        "pagingType": "full_numbers",
        "lengthMenu": [
            [10, 25, 50, -1],
            [10, 25, 50, "All"]
        ],
        responsive: true,
        language: {
            emptyTable: "No hay datos aún",
            search: "_INPUT_",
            searchPlaceholder: "Buscar",
            info: "Mostrando página _PAGE_ de _PAGES_",
            infoEmpty: "No hay datos que mostrar",
            infoFiltered: "- filtrados de _MAX_ registros",
            lengthMenu: "Mostrando _MENU_ registros",
            processing: "Buscando...",
            zeroRecords: "No hay resultados",
            paginate:{
            first:"Inicio",
            last:"Final",
            next:"Siguiente",
            previous:"Anterior",
            },
        }
    });

    var table = $('#datatable').DataTable();

    // Edit record
    table.on('click', '.edit', function() {
    $tr = $(this).closest('tr');
    var data = table.row($tr).data();
    alert('You press on Row: ' + data[0] + ' ' + data[1] + ' ' + data[2] + '\'s row.');
    });

    // Delete a record
    table.on('click', '.remove', function(e) {
    $tr = $(this).closest('tr');
    table.row($tr).remove().draw();
    e.preventDefault();
    });

    //Like record
    table.on('click', '.like', function() {
    alert('You clicked on Like button');
    });
});
function modalDelete(obj) {
    var url = obj.getAttribute("data-link");
    $('#form_delete').attr('action', url);
    return false;
  }