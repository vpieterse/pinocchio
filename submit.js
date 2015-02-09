 function userSubmit()
{
    var values = [];
    values["studentID"] = $("#studentnumber").val();
    values["Title"] = $("#title").val();
    values["Initials"] = $("#initials").val();
    values["Name"] = $("#firstname").val();
    values["Surname"] = $("#surname").val();
    values["Password"] = $("#password").val();
    values["Cell"] = $("#cell").val();
    values["Email"] = $("#email").val();
    values["Status"] = $("#status").val();
    
    var jsonValues = JSON.stringify(values);
    
    jQuery.ajax({
        type: "POST",
        url: "ajaxMiddleman.php",
        data: {table: "studentdetail", jsonValues: jsonValues, functionname: "userSubmit"},
        
        success: function(x)
        {
            alert(x + " SUCCESS");
        },
        error: function(x)
        {
            alert(x + " ERROR");
        }
    });
}

function csvSubmit()
{
    alert("Clicked CSV Submit");
}

function acceptEdit($stringRow)
{
    alert("Clicked Accept");
    /*<?php 
        $row = unserialize($stringRow);
        /// @TODO Update studentdetail as well
        updateTable("users", $row, $where = array("studentID" => $row["Student Number"]));
    ?>*/
}

function deleteRow($stringRow)
{
    alert("Clicked Delete");
    /*<?php 
        $row = unserialize($stringRow);
        deleteFromTable("users", $row);
    ?>*/
}