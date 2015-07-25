$('#userForm').submit(function(){
	alert("xxx");
})

// function validateUserForm() {
// 	alert("xxx");
// 	return false;

//     var title = $("#title").val();
//     var status = document.forms["userForm"]["status"].value;
//     var initials = document.forms["userForm"]["initials"].value;
//     var cell = document.forms["userForm"]["cellNumber"].value;
//     var firstname = document.forms["userForm"]["firstName"].value;
//     var email = document.forms["userForm"]["email"].value;
//     var surname = document.forms["userForm"]["surname"].value;
//     var password = document.forms["userForm"]["password"].value;
//     var studentnumber = document.forms["userForm"]["studentNumber"].value;
//     var passwordconfirm = document.forms["userForm"]["passwordConfirm"].value;
	
//     if (title == null || title == "" ||
// 		status == null || status == "" ||
// 		initials == null || initials == "" ||
// 		cell == null || cell == "" ||
// 		firstname == null || firstname == "" ||
// 		email == null || email == "" ||
// 		surname == null || surname == "" ||
// 		password == null || password == "" ||
// 		passwordconfirm == null || passwordconfirm == "") {
//         alert("Please fill in all fields");
//         return false;
//     }
	
// 	if (password != passwordconfirm){
// 		alert("Passwords do not correspond");
// 		return false;
// 	}
	
// 	if (status != 'A' && status != 'a' && status != 'S' && status != 's')
// 	{
// 		alert("Please enter a valid status (A for admin, S for student)");
// 		return false;
// 	}
	
// 	for (i = 0; i < studentnumber.length; ++i)
// 	{
// 		if (isNaN(studentnumber[i]))
// 		{
// 			alert("Please enter a valid student number");
// 			return false;
// 		}
// 	}
	
// 	for (i = 0; i < cell.length; ++i)
// 	{
// 		if (isNaN(cell[i]))
// 		{
// 			alert("Please enter a valid cell number");
// 			return false;
// 		}
// 	}
// }

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');