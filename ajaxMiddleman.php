<?php
	/**
	* AJAX function call translator.
	*/

	echo "BLAH";
	
	$aResult = array();

	if( !isset($_POST['functionname']) ) { $aResult['error'] = 'No function name!'; }

	if( !isset($_POST['arguments']) ) { $aResult['error'] = 'No function arguments!'; }

	if( !isset($aResult['error']) ) {

		switch($_POST['functionname']) {
			case 'insertIntoTable':{
				include 'genericSQLStatements.php';
				insertIntoTable("A");
				$table = $_POST["table"];
				$jsonValues = $_POST["jsonValues"];
				$values = json_decode($jsonValues, true);
				
				insertIntoTable($table, $values);
				
				
			}
			  break;

			default:
			   $aResult['error'] = 'Not found function '.$_POST['functionname'].'!';
			break;
		}

	}

	json_encode($aResult);
	
	echo $aResult;

?>