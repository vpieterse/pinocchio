/*$(window).load(function(){
    window.actionEvents = {
        'click .up': function (e, value, row, index) {
            var source = JSON.stringify($('#table').bootstrapTable('getData')[index]);
            var target = JSON.stringify($('#table').bootstrapTable('getData')[index - 1]);
            $('#table').bootstrapTable('updateRow', {'index':index - 1, 'row': JSON.parse(source)});
            $('#table').bootstrapTable('updateRow', {'index':index, 'row': JSON.parse(target)});
        },
        'click .down': function (e, value, row, index) {
            var source = JSON.stringify($('#table').bootstrapTable('getData')[index]);
            var target = JSON.stringify($('#table').bootstrapTable('getData')[index + 1]);
            $('#table').bootstrapTable('updateRow', {'index':index + 1, 'row': JSON.parse(source)});
            $('#table').bootstrapTable('updateRow', {'index':index, 'row': JSON.parse(target)});
        }
    }
    function fmtMoveUp(value) {return '<a class="action up" href="javascript:void(0)" title="Move up"><span class="glyphicon glyphicon-arrow-up"></span></a>';};
    function fmtMoveDown(value) {return '<a class="action down" href="javascript:void(0)" title="Move down"><span class="glyphicon glyphicon-arrow-down"></span></a>';};

    var fakedata= [
        {"choice":"Chicken"},
        {"choice":"Beef"},
        {"choice":"Fish"},
        {"choice":"Other"},
    ]

    $("#table").bootstrapTable({
        data:fakedata,
        classes: 'table-striped table-condensed table-hover btable',
        columns: [
            { field:'choice', title:'Choices', align:'center'},
            { field:'Up', title:'', align:'center', width:20, formatter:fmtMoveUp, events:actionEvents},
            { field:'Down', title:'', align:'center', width:20, formatter:fmtMoveDown, events:actionEvents}
        ]
    });

    $('#btn').click(function() {
        var tableData = $('#table').bootstrapTable('getData');
        console.log(tableData);    
    });
});*/

function initialiseStacking() {
    $('.table').on("click", '.move', function () {
        var row = $(this).closest('tr');
        if ($(this).hasClass('up'))
            row.prev().before(row);
        else
            row.next().after(row);
    });

    //Remove row from table
    $('table').on('click', '.remove', function ()
    {
        var rowCount = $('#labelTable').find('> tbody > tr').length;
        if (rowCount <= 2) {
            console.log(rowCount);
            $('#table-error').html("<div class=\"alert alert-danger\">There needs to be at least 2 labels in the Rank type.</div>");
            
        } else {
            $(this).closest('tr').remove(); 
        }
    });

    $('table').on('change', '#type', function()
    {
        inputBox =  $(this).parents('tr').find('input');
        //console.log($(this).parents('tr').find('select').val());
        switch ($(this).parents('tr').find('select').val())
        {
            case 'Real':
            case 'Integer':
                inputBox.attr('type', 'number');
                break;
            case 'Paragraph':
            case 'Default':
            case 'Word':
                inputBox.attr('type', 'text');
                break;
        }
    });

}
