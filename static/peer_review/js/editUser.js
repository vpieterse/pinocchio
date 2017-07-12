/**
* Created by jeffreyrussell on 5/26/17.
*/
$(document).on("ready", function() {
    $(".edit").on("click", function () {
        var pk = $(this).data("pk");
        $("#more").attr("data-pk", pk);
        var token = $(this).data("csrf");
        var row = $("#user" + pk);

        var userId = row.find("[data-id='userId']");
        var title = row.find("[data-id='title']");
        var initials = row.find("[data-id='initials']");
        var name = row.find("[data-id='name']");
        var surname = row.find("[data-id='surname']");
        var cell = row.find("[data-id='cell']");
        var email = row.find("[data-id='email']");
        var status = row.find("[data-id='status']");

        $("#e_userId").val(userId.val());
        $("#e_title").val(title.text());
        $("#e_initials").val(initials.text());
        $("#e_name").val(name.text());
        $("#e_surname").val(surname.text());
        $("#e_cell").val(cell.text());
        $("#e_email").val(email.text());

        if (status.text() == "U") {
            $("#e_status").val("User");
        } else if (status.text() == "A") {
            $("#e_status").val("Admin");
        } else {
            $("#e_status").val("");
        }

        if(!isAdmin) {
            $("#e_status").prop("disabled", true);
        } else if(userPK == pk) {
            $("#resetPassword").show();
        } else {
            $("#resetPassword").hide();
        }

        $("#updateConfirm").on("click", function () {
            var uStatus = "";

            if ($("#e_status").val() == "User") {
                uStatus = "U";
            } else if ($("#e_status").val() == "Admin") {
                uStatus = "A";
            }

            var data = {
                'userId': $("#e_userId").val(),
                'title': $("#e_title").val(),
                'initials': $("#e_initials").val(),
                'name': $("#e_name").val(),
                'surname': $("#e_surname").val(),
                'cell': $("#e_cell").val(),
                'email': $("#e_email").val(),
                'status': uStatus,
                'csrfmiddlewaretoken': token
            };

            $.ajax({
                type: 'POST',
                url: '/userAdmin/update/' + pk,
                data: data,
                success: function () {
                    userId.text($("#e_userId").val());
                    title.text($("#e_title").val());
                    initials.text($("#e_initials").val());
                    name.text($("#e_name").val());
                    surname.text($("#e_surname").val());
                    cell.text($("#e_cell").val());
                    email.text($("#e_email").val());
                    status.text(uStatus);
                }
            });
        });

        $("#resetPassword").on("click", function () {
            if (confirm("Are you sure you want to reset the password for this user?")) {
                $.ajax({
                    type: 'POST',
                    url: '/userAdmin/resetPassword/' + pk,
                    data: {
                        'csrfmiddlewaretoken': token
                    },
                    success: function () {
                        alert("Password reset");
                    }
                });
            }
        });
    });
});