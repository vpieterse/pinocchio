/**
* Created by jeffreyrussell on 5/26/17.
*/
$(document).on("ready", function() {
    $(".edit").on("click", function () {
        var pk = $(this).data("pk");
        $("#more").attr("data-pk", pk);
        var token = $(this).data("csrf");
        var row = $("#users > tbody > tr#" + pk);

        var userId = row.children("[data-id='userId']");
        var title = row.children("[data-id='title']");
        var initials = row.children("[data-id='initials']");
        var name = row.children("[data-id='name']");
        var surname = row.children("[data-id='surname']");
        var cell = row.children("[data-id='cell']");
        var email = row.children("[data-id='email']");
        var status = row.children("[data-id='status']");

        $("#e_userId").val(userId.text());
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

        $("#more").on("click", function () {
            var pk = $(this).data("pk");
            window.location.href = "/userAdmin/userProfile/" + pk;
        });
    });
});