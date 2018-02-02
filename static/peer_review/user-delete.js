$("#remove").on("click", function () {
    wResponses = [];
    woResponses = [];

    var token = $(this).data("csrf");

    $("[style!='display: none;'] > td > input:checked.multiRemove.wResponses").each(function() {
        wResponses.push({
            "id": $(this).data("id"),
            "pk": $(this).data("pk")
        });
    });

    $("[style!='display: none;'] > td > input:checked.multiRemove.woResponses").each(function() {
        woResponses.push({
            "id": $(this).data("id"),
            "pk": $(this).data("pk")
        });
    });

    toDeleteMessage =
            "Are you sure you want to delete the following users?\n\n";
    var responsePrompt = [
            "The following users have responses assosiated with them:\n\n",
            "\nAre you sure you want to delete these users and all" +
            " responses assosiated with them?\n\n"
        ];

    var toDeleteList = [];
    var wResponsesList = [];
    var woResponsesList = [];

    $.each(wResponses, function(index, value) {
        toDeleteMessage += value.id + "\n";
        responsePrompt[0] += value.id + "\n";
        wResponsesList.push(value.pk);
    });

    res = responsePrompt[0] + responsePrompt[1];

    $.each(woResponses, function(index, value) {
        toDeleteMessage += value.id + "\n";
        woResponsesList.push(value.pk);
    });

    if (woResponses.length > 0) {
        if(confirm(toDeleteMessage)) {
            var data = {
                'toDelete': woResponsesList,
                'csrfmiddlewaretoken': token
            };

            $.ajax({
                type: 'POST',
                url: '/userAdmin/delete/',
                data: data,
                success: function() {
                    $.each(woResponses, function(index, value) {
                        $("#users > tbody > tr#user" + value.id).fadeOut(500);
                    });
                }
            });
        }
    }

    if (wResponses.length > 0) {
        if(confirm(res)) {
            var data = {
                'toDelete': wResponsesList,
                'csrfmiddlewaretoken': token
            };

            $.ajax({
                type: 'POST',
                url: '/userAdmin/deleteHandler/',
                data: data,
                success: function() {
                    $.each(wResponses, function(index, value) {
                        $("#users > tbody > tr#user" + value.id).fadeOut(500);
                    });
                }
            });
        }
    }
});
