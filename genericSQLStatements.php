<?php  
// Testing ////
//$values = array('name'=>'Piet', 'age'=>'37', 'city'=>'Pietoria');
// $values = array('name'=>'Johnny', 'age'=>'31', 'city'=>'Johnburg');
//  $where = array('id'=>'5');
//$values = array('name'=>'Johnny', 'name' => 'Piet');
//echo '<br>'.insertIntoTable('users', $values);
//print_r(insertIntoTable('users', $values));
//print_r(updateTable('users', $values, $where));
////////////

require_once '/htmlpurifier-4.6.0/library/HTMLPurifier.auto.php';

/**
* A function that runs a delete statement on a specified table in the database.
*
* @param table The name of the table to delete from
* @param values An associative array indexed with the column name and containing the values used for the delete statement. i.e.:
*        $values = array('name'=>'Piet', 'age'=>'37', 'city'=>'Pietoria');
* @param and Sets if ANDs are used for the where statement. Uses ORs if false. Default is true.
* @return The result of the query. See mysqli_prepared_query example below.
*/
function deleteFromTable($table, $values, $and = TRUE){
  /// @todo This connection or the values for it could be stored outside somewhere.
  $con = mysqli_connect("localhost","root","","peerreview");
  // Check connection
  if (mysqli_connect_errno())
  {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }

  $sql = 'DELETE FROM ' . $table . ' WHERE ';
  $count = 0;
  $typeDef = "";
  $params = array();

  foreach($values as $x => $x_value)
  {
    // Append column names
    if($count == count($values)-1)
    {
      $sql = $sql . $x . ' = ?';
    }
    else
    {
      $sql = ($and) ? $sql . $x . ' = ? AND ' : $sql . $x . ' = ? OR ' ;
      //$sql = $sql . $x . ' = ? AND ';
    }

    // Build typeDef string for mysqli_prepared_query
    /// @todo Improve this type inference. i.e. use mysqli_fetch_field
    if (is_int($x_value)) {
      $typeDef = $typeDef . 'i';
    }
    else if (is_double($x_value)) {
      $typeDef = $typeDef . 'd';
    }else{
      $typeDef = $typeDef . 's';
    }
    array_push($params, $x_value);
    
    ++$count;
  }
  
  // Uncomment for debug
  //echo $typeDef.'<br>';
  //print_r($params);
  //echo $sql;

  $result = mysqli_prepared_query($con, $sql, $typeDef, $params) or die(mysqli_error($link));

  return $result;
}

/**
* A function that runs a inner join on a 2 tables in the database.
*
* @param table1 The name of the first table
* @param table2 The name of the second table
* @param key The name of key to join on
* @param values An associative array indexed with the column name and containing the values used for the select statement. i.e.:
*        $values = array('name'=>'Piet', 'age'=>'37', 'city'=>'Pietoria');
* @param and Sets if ANDs are used for the where statement. Uses ORs if false. Default is true.
* @return The result of the query. See mysqli_prepared_query example below.
*/
function innerJoin($table1, $table2, $key, $values, $and = TRUE){
  /// @todo This connection or the values for it could be stored outside somewhere.
  $con = mysqli_connect("localhost","root","","peerreview");
  // Check connection
  if (mysqli_connect_errno())
  {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }

  /// @todo Select certain columns, not * (make * default?)
  $sql = 'SELECT * FROM '.$table1.' INNER JOIN'.$table2.' ON '.$table1.'.'.$key.'='.$table2.'.'.$key.' WHERE ';
  $count = 0;
  $typeDef = "";
  $params = array();

  foreach($values as $x => $x_value)
  {
    // Append column names
    if($count == count($values)-1)
    {
      $sql = $sql . $x . ' = ?';
    }
    else
    {
      $sql = ($and) ? $sql . $x . ' = ? AND ' : $sql . $x . ' = ? OR ' ;
      //$sql = $sql . $x . ' = ? AND ';
    }

    // Build typeDef string for mysqli_prepared_query
    /// @todo Improve this type inference. i.e. use mysqli_fetch_field
    if (is_int($x_value)) {
      $typeDef = $typeDef . 'i';
    }
    else if (is_double($x_value)) {
      $typeDef = $typeDef . 'd';
    }else{
      $typeDef = $typeDef . 's';
    }
    array_push($params, $x_value);

    ++$count;
  }
  $sql = $sql . 'inner join on '
  // Uncomment for debug
  //echo $typeDef.'<br>';
  //print_r($params);
  //echo $sql;

  $result = mysqli_prepared_query($con, $sql, $typeDef, $params) or die(mysqli_error($con));

  return $result;
}

/**
* A function that inserts values into a specified table in the database.
*
* @param table The name of the table to insert into
* @param values An associative array indexed with the column name and containing the value to insert. i.e.:
*        $values = array('name'=>'Piet', 'age'=>'37', 'city'=>'Pietoria');
* @return The result of the query.
*/
function insertIntoTable($table, $values){
  /// @todo This connection or the values for it could be stored outside somewhere.
  $con = mysqli_connect("localhost","root","","peerreview");
  // Check connection
  if (mysqli_connect_errno())
  {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }

  $sql = 'INSERT into ' . $table . ' (';
  $count = 0;
  $typeDef = "";
  $params = array();

  foreach($values as $x => $x_value)
  {
    // Append column names
    if($count == 0)
    {
      $sql = $sql . $x;
    }
    else
    {
      $sql = $sql . ', ' . $x;
    }

    // Build typeDef string for mysqli_prepared_query
    /// @todo Improve this type inference. i.e. use mysqli_fetch_field
    if (is_int($x_value)) {
      $typeDef = $typeDef . 'i';
    }
    else if (is_double($x_value)) {
      $typeDef = $typeDef . 'd';
    }else{
      $typeDef = $typeDef . 's';
    }
    array_push($params, $x_value);
    
    ++$count;
  }

  $sql = $sql . ') VALUES (';
  for ($i=0; $i < count($values); $i++) 
  { 
    if ($i == 0) 
    {
      $sql = $sql . '?';
    }
    else
      $sql = $sql . ', ?';
  }
  $sql = $sql . ')';
  
  // Uncomment for debug
  //echo $typeDef.'<br>';
  //print_r($params);

  
  $result = mysqli_prepared_query($con, $sql, $typeDef, $params) or die(mysqli_error($link));

  return $result;
}

/**
* A function that runs a select statement on a specified table in the database.
*
* @param table The name of the table to select from
* @param values An associative array indexed with the column name and containing the values used for the select statement. i.e.:
*        $values = array('name'=>'Piet', 'age'=>'37', 'city'=>'Pietoria');
* @param and Sets if ANDs are used for the where statement. Uses ORs if false. Default is true.
* @return The result of the query. See mysqli_prepared_query example below.
*/
function selectFromTable($table, $values, $and = TRUE){
  /// @todo This connection or the values for it could be stored outside somewhere.
  $con = mysqli_connect("localhost","root","","peerreview");
  // Check connection
  if (mysqli_connect_errno())
  {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }

  $sql = 'SELECT * FROM ' . $table . ' WHERE ';
  $count = 0;
  $typeDef = "";
  $params = array();

  foreach($values as $x => $x_value)
  {
    // Append column names
    if($count == count($values)-1)
    {
      $sql = $sql . $x . ' = ?';
    }
    else
    {
      $sql = ($and) ? $sql . $x . ' = ? AND ' : $sql . $x . ' = ? OR ' ;
      //$sql = $sql . $x . ' = ? AND ';
    }

    // Build typeDef string for mysqli_prepared_query
    /// @todo Improve this type inference. i.e. use mysqli_fetch_field
    if (is_int($x_value)) {
      $typeDef = $typeDef . 'i';
    }
    else if (is_double($x_value)) {
      $typeDef = $typeDef . 'd';
    }else{
      $typeDef = $typeDef . 's';
    }
    array_push($params, $x_value);
    
    ++$count;
  }
  
  // Uncomment for debug
  //echo $typeDef.'<br>';
  //print_r($params);
  //echo $sql;

  $result = mysqli_prepared_query($con, $sql, $typeDef, $params) or die(mysqli_error($con));

  return $result;
}

/**
* A function that updates certain values in a specific table in the database.
*
* @param table The name of the table to update.
* @param values An associative array indexed with the column name and containing the new values. i.e.:
*         This is for the 'set' part of the statement SET column1=value1,column2=value2,...
*        $values = array('name'=>'Piet', 'age'=>'37', 'city'=>'Pietoria');
* @param whereValues An associative array indexed with the column name and containing the values for the
*         where part of the statement. i.e.: WHERE some_column=some_value;
* @param and Sets if ANDs are used for the where statement. Uses ORs if false. Default is true.
* @return The result of the query.
*/
function updateTable($table, $values, $whereValues, $and = TRUE){
  /// @todo This connection or the values for it could be stored outside somewhere.
  $con = mysqli_connect("localhost","root","","peerreview");
  // Check connection
  if (mysqli_connect_errno())
  {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }

  $sql = 'UPDATE ' . $table . ' SET ';
  $count = 0;
  $typeDef = "";
  $params = array();

  foreach($values as $x => $x_value)
  {
    // Append column names
    if($count == count($values)-1)
    {
      $sql = $sql . $x . ' = ?';
    }
    else
    {
      $sql = $sql . $x . ' = ?, ' ;
    }
    
    // Build typeDef string for mysqli_prepared_query
    /// @todo Improve this type inference. i.e. use mysqli_fetch_field
    if (is_int($x_value)) {
      $typeDef = $typeDef . 'i';
    }
    else if (is_double($x_value)) {
      $typeDef = $typeDef . 'd';
    }else{
      $typeDef = $typeDef . 's';
    }
    array_push($params, $x_value);

    ++$count;
  }


  $sql = $sql . ' WHERE ';
  $count = 0;

  foreach($whereValues as $x => $x_value)
  {
   // Append column names
   if($count == count($whereValues)-1)
   {
     $sql = $sql . $x . ' = ' . $x_value;
   }
   else
   {
     $sql = ($and) ? $sql . $x . ' = ' . $x_value . ' AND ' : $sql . $x . ' = ' . $x_value . ' OR ' ;
     //$sql = $sql . $x . ' = ? AND ';
   }
   
   ++$count;
  }
  
  // Uncomment for debug
  //echo $typeDef.'<br>';
  //print_r($params);
  //echo $sql;
  
  //$result = mysqli_prepared_query($con, $sql, $typeDef, $params) or die(mysqli_error($link));
  $result = mysqli_prepared_query($con, $sql, $typeDef, $params) or die(mysqli_error($con));

  return $result;
}


/**
*  For queries: 
*  Results of single queries are given as arrays[row#][associated Data Array] 
*  Results of multiple queries are given as arrays[query#][row#][associated Data Array] 
*
*  For queries which return an affected row#, affected rows are returned instead of (array[row#][associated Data Array]) 
*  Example below the function @todo include in docs?
*
* @param link The SQL link
* @param sql The SQL statement
* @param typeDef The type of each parameter that will be bound. 
*        i.e if there are 2 string types then this will be 'ss'. Available types s(string), i(int), d(double), b(blob).
* @param params An array of the values to be bound
* @return An array containing the results of the queries 
*/
function mysqli_prepared_query($link, $sql, $typeDef = FALSE, $params = FALSE){
  // Set up HTML Purifier
	$config = HTMLPurifier_Config::createDefault();
  $purifier = new HTMLPurifier($config);
  $cleanSql = $purifier->purify($sql);

  $multiQuery = TRUE; // bugfix: pre-initialize multiQuery to solve for "Undefined variable" error
  if($stmt = mysqli_prepare($link,$cleanSql)){
    if(count($params) == count($params,1)){ 
      $params = array($params); 
      $multiQuery = FALSE; 
    } else { 
      $multiQuery = TRUE; 
    }  
    
    if($typeDef){ 
      $bindParams = array();
      $bindParamsReferences = array(); 
      $bindParams = array_pad($bindParams,(count($params,1)-count($params))/count($params),"");
      foreach($bindParams as $key => $value){ 
        $bindParamsReferences[$key] = &$bindParams[$key];  
      } 
      array_unshift($bindParamsReferences,$typeDef); 
      $bindParamsMethod = new ReflectionMethod('mysqli_stmt', 'bind_param'); 
      $bindParamsMethod->invokeArgs($stmt,$bindParamsReferences); 
    } 
    
    $result = array();
    foreach($params as $queryKey => $query){
      foreach($bindParams as $paramKey => $value){
        $bindParams[$paramKey] = $query[$paramKey];
      } 
      $queryResult = array();
      if(mysqli_stmt_execute($stmt)){
        $resultMetaData = mysqli_stmt_result_metadata($stmt);
        if($resultMetaData){                                                                    
          $stmtRow = array();
          $rowReferences = array();
          while ($field = mysqli_fetch_field($resultMetaData)) {
            $rowReferences[] = &$stmtRow[$field->name];
          }
          mysqli_free_result($resultMetaData); 
          $bindResultMethod = new ReflectionMethod('mysqli_stmt', 'bind_result'); 
          $bindResultMethod->invokeArgs($stmt, $rowReferences); 
          while(mysqli_stmt_fetch($stmt)){ 
            $row = array(); 
            foreach($stmtRow as $key => $value){ 
              $row[$key] = $value;           
            } 
            $queryResult[] = $row; 
          } 
          mysqli_stmt_free_result($stmt); 
        } else { 
          $queryResult[] = mysqli_stmt_affected_rows($stmt); 
        } 
      } else { 
        $queryResult[] = FALSE; 
      } 
      $result[$queryKey] = $queryResult; 
    } 
    mysqli_stmt_close($stmt);
  } else { 
    $result = FALSE; 
  } 
  
  if($multiQuery){ 
    return $result; 
  } else { 
    return $result[0]; 
  } 
} 

/*
Example(s): 
For a table of firstName and lastName: 
John Smith 
Mark Smith 
Jack Johnson 
Bob Johnson 

<?php 
//single query, single result 
$query = "SELECT * FROM names WHERE firstName=? AND lastName=?"; 
$params = array("Bob","Johnson"); 

mysqli_prepared_query($link,$query,"ss",$params) 
/* 
returns array( 
0=> array('firstName' => 'Bob', 'lastName' => 'Johnson') 
) 
//
//single query, multiple results 
$query = "SELECT * FROM names WHERE lastName=?"; 
$params = array("Smith"); 

mysqli_prepared_query($link,$query,"s",$params) 
/* 
returns array( 
0=> array('firstName' => 'John', 'lastName' => 'Smith') 
1=> array('firstName' => 'Mark', 'lastName' => 'Smith') 
) 
//

//multiple query, multiple results 
$query = "SELECT * FROM names WHERE lastName=?"; 
$params = array(array("Smith"),array("Johnson")); 

mysqli_prepared_query($link,$query,"s",$params) 
/* 
returns array( 
0=> 
array( 
0=> array('firstName' => 'John', 'lastName' => 'Smith') 
1=> array('firstName' => 'Mark', 'lastName' => 'Smith') 
) 
1=> 
array( 
0=> array('firstName' => 'Jack', 'lastName' => 'Johnson') 
1=> array('firstName' => 'Bob', 'lastName' => 'Johnson') 
) 
) 
*/ 



?>