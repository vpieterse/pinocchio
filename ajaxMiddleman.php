<?php
	/**
	* AJAX function call translator.
	*/
	
	$errorFeedback = array();

	if( !isset($_POST['functionname']) )
	{
		$errorFeedback['error'] = "No function name!";
	}
	
	if( !isset($_POST['table']) )
	{
		$errorFeedback['error'] = "No table name!";
	}
	
	if( !isset($_POST['jsonValues']) )
	{
		$errorFeedback['error'] = "No json values!";
	}

	if (!isset($errorFeedback['error']))
	{
		if ($_POST['functionname'] == "userSubmit")
		{
			include 'genericSQLStatements.php';
			$insertTable = $_POST["table"];
			$userValues = json_decode($_POST["jsonValues"], true);
			insertIntoTable($insertTable, $userValues);
		}
	}

	if (isset($errorFeedback['error']))
	{
		echo $errorFeedback['error'];
	}
?>