function initialiseStacking() {
    $('.table a.move').click(function () {
        var row = $(this).closest('tr');
        if ($(this).hasClass('up'))
            row.prev().before(row);
        else
            row.next().after(row);
    });
};