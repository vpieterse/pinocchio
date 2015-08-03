$(document).ready(function()
{
	$('#search').keyup(function()
	{
		tableSearch($(this).val());
	});
});

function tableSearch(value)
{
	var table = $('#users');
	table.find('tr').each(function(index, row)
	{
		var cells = $(row).find('td');
		if(cells.length > 0)
		{
			var found = false;
			$(this).find('input[type="text"]').each(function() {
				var regExp = new RegExp(value, 'i');
				if(regExp.test($(this).val()))
				{
					found = true;
					return false;
				}
			});
			if(found == true)$(row).show();else $(row).hide();
		}
	});
}