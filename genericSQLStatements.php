<?php  

function insertIntoDatabase($table, $values){
  $sql = 'INSERT into ' . $table . ' (';
  $count = 0;

  foreach($values as $x => $x_value)
  {
    if($count == 0)
    {
      $sql = $sql . $x;
    }
    else
    {
      $sql = $sql . ', ' . $x;
    }
    ++$count;
  }

  $sql = $sql . ') VALUES (';

  $count = 0;
  foreach($values as $x => $x_value)
  {
    if($count == 0)
    {
      $sql = $sql . $x_value;
    }
    else
    {
      $sql = $sql . ', ' . $x_value;
    }
    ++$count;
  }

  $sql = $sql . ')';
  
  return $sql;
}

$values = array('Name'=>'Piet', 'age'=>'37', 'city'=>'Pietoria');

echo insertIntoDatabase('users', $values);

function insertIntoDatabase($table, $values){
  $sql = 'INSERT into ' . $table . ' (';
  $count = 0;
  $typeDef = "";

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

    if (is_int($x_value)) {
      $typeDef = $typeDef . 'i';
    }
    else if (is_double($x_value)) {
      $typeDef = $typeDef . 'd';
    }else{
      $typeDef = $typeDef . 's';
    }
    
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
  echo $typeDef;
  return $sql;
}





?>