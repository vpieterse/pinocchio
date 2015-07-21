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
			cells.each(function(index, td)
			{
				var regExp = new RegExp(value, 'i');
				if(regExp.test($(td).text()))
				{
					found = true;
					return false;
				}
			});
			if(found == true)$(row).show();else $(row).hide();
		}
	});
}