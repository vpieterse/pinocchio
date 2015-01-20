<!DOCTYPE html>
<html lang="en">
<script src="jquery.min.js"></script>
<script src="js/bootstrap.js"></script>
<script src="bootstrap-sortable.js"></script>
<head>
    <title>Pinocchio</title>
    <meta charset="utf-8" name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="css/bootstrap.min.css" />
    <link rel="stylesheet" href="style.css" />
    <link rel="stylesheet" href="bootstrap-sortable.css" />
</head>
<body>
    <nav class="navbar navbar-inverse navbar-static-top">
        <div class="container">
            <div class="navbar-header">
                <a href="index.html" class="navbar-brand">Pinocchio</a>
                <button class="navbar-toggle" data-toggle="collapse" data-target=".navHeaderCollapse">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
            </div>
            <div class="collapse navbar-collapse navHeaderCollapse">
                <ul class="nav navbar-nav navbar-right">
                    <li class="active"><a href="userAdmin.php">User Admin</a></li>
                    <li><a href="roundAdmin.html">Round Admin</a></li>
                    <li><a href="teamAdmin.html">Team Admin</a></li>
                    <li><a href="questionAdmin.html">Question Admin</a></li>
                    <li><a href="questionnaireAdmin.html">Questionnaire Admin</a></li>
                    <li><a href="fileManager.html">File Manager</a></li>
                    <li><a href="serverManager.html">Server Manager</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="panel-group" id="accordion">
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a data-toggle="collapse" data-parent="#accordion" href="#collapseOne">
                            User Registration <b class="caret"></b>
                        </a>
                    </h4>
                </div>
                <div id="collapseOne" class="panel-collapse collapse in">
                    <div class="panel-body">
                        <form class="form-horizontal" role="form" method="post" action="#">
                            <div class="form-group">
                                <label for="title" class="col-sm-2 control-label">Title:</label>
                                <div class="col-sm-3">
                                    <input type="text" class="form-control" id="title" placeholder="Title">
                                </div>

                                <label for="status" class="col-sm-2 control-label">Status:</label>
                                <div class="col-sm-3">
                                    <input type="text" class="form-control" id="status" placeholder="Status">
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="initials" class="col-sm-2 control-label">Initials:</label>
                                <div class="col-sm-3">
                                    <input type="text" class="form-control" id="initials" placeholder="Initials">
                                </div>

                                <label for="cell" class="col-sm-2 control-label">Cell Number:</label>
                                <div class="col-sm-3">
                                    <input type="text" class="form-control" id="cell" placeholder="Cell Number">
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="firstname" class="col-sm-2 control-label">First Name:</label>
                                <div class="col-sm-3">
                                    <input type="text" class="form-control" id="firstname" placeholder="First Name">
                                </div>

                                <label for="email" class="col-sm-2 control-label">Email:</label>
                                <div class="col-sm-3">
                                    <input type="email" class="form-control" id="email" placeholder="Email">
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="surname" class="col-sm-2 control-label">Surname:</label>
                                <div class="col-sm-3">
                                    <input type="text" class="form-control" id="surname" placeholder="Surname">
                                </div>

                                <label for="password" class="col-sm-2 control-label">Password:</label>
                                <div class="col-sm-3">
                                    <input type="password" class="form-control" id="password" placeholder="Password">
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="studentnumber" class="col-sm-2 control-label">Student Number:</label>
                                <div class="col-sm-3">
                                    <input type="text" class="form-control" id="studentnumber" placeholder="Student Number">
                                </div>

                                <label for="passwordconfirm" class="col-sm-2 control-label">Confirm Password:</label>
                                <div class="col-sm-3">
                                    <input type="password" class="form-control" id="passwordconfirm" placeholder="Confirm Password">
                                </div>
                            </div>

                            <div class="form-group">
                                <div class="col-sm-offset-2 col-sm-10">
                                    <button type="submit" class="btn btn-info" id="submitUser" onclick="userSubmit()">Submit</button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a data-toggle="collapse" data-parent="#accordion" href="#collapseTwo">
                            User Registration Via CSV File <b class="caret"></b>
                        </a>
                    </h4>
                </div>
                <div id="collapseTwo" class="panel-collapse collapse">
                    <div class="panel-body">
                        <form role="form" method="post" action="#">
                            <div class="form-group">
                                <label for="inputfile">Upload CSV File:</label>
                                <input type="file" id="inputfile">
                                <p class="help-block">Select a CSV file to register users</p>
                            </div>
                            <button type="submit" class="btn btn-info" id="submitCSV" onclick="csvSubmit()">Submit</button>
                        </form>
                    </div>
                </div>
            </div>
			
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h4 class="panel-title">
                        <a data-toggle="collapse" data-parent="#accordion" href="#collapseThree">
                            Maintain Users <b class="caret"></b>
                        </a>
                    </h4>
                </div>	
				
				<div id="collapseThree" class="panel-collapse collapse">
                    <div class="panel-body">
					
						<input type="text" class="form-control" id="search" placeholder="Search" onkeyup="showResult(this.value)">
						
						<?php
							include 'genericSQLStatements.php';
							
							$con = mysqli_connect("localhost","root","","peerreview"); // @todo replace this with appropriate login info and database name etc.
							// Check connection
							if (mysqli_connect_errno())
							{
								echo "Failed to connect to MySQL: " . mysqli_connect_error();
							}
							
							//$result = mysqli_query($con, "SELECT * FROM users");
							$result = selectFromTable("student",array(1=>1));
							echo " <div class='table-responsive'>
							<table class='table sortable' id='users'>
								<thead>
									<tr>
										<th>#</th>
										<th>Student Number</th>
										<th>Title</th>
										<th>Initials</th>
										<th>First Name</th>
										<th>Surname</th>
										<th data-defaultsort='disabled'>Password</th>
										<th data-defaultsort='disabled'>Cell</th>
										<th>Email</th>
										<th>Status</th>
										<th></th>
										<th></th>
									</tr>
								</thead>
								<tbody>";
							
							$list = array();
							foreach($result as $row) //used to display the info within the database
							{
								$list[] = $row;
							}
							
							$count = 0;
							$out  = "";
							foreach($list as $key => $element)
							{
								$row = array();
								$out .= "<tr>";
								foreach($element as $subkey => $subelement)
								{
									$out .= "<td contenteditable=true>$subelement</td>";
									$row[$subkey] = $subelement;
								}
								$stringRow = serialize($row);
								$out.= "<td><button type='button' class='btn btn-success btn-xs' id='accept' onclick='acceptEdit($stringRow)'>&#10004;</button></td>";
								$out.= "<td><button type='button' class='btn btn-warning btn-xs' id='delete' onclick='deleteRow($stringRow)'>&#10008;</button></td>";
								$out .= "</tr>";
								$count = $count + 1;
							}
							$out .= "</tbody>";
							$out .= "</table>";

							echo $out;							
							mysqli_close($con);
						?>
						
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
	
    <div class="navbar navbar-default navbar-fixed-bottom">
        <div class="container">
            <p class="navbar-text pull-left">&copy; Dillon Heins</p>
            <a class="navbar-btn btn-danger btn pull-right">Log Out</a>
        </div>
    </div>

	<script> //script used to search table
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
	</script>
	<script>
		function userSubmit()
		{
			alert("Clicked User Submit");
		}
		
		function csvSubmit()
		{
			alert("Clicked CSV Submit");
		}
		
		function acceptEdit($stringRow)
		{
			alert("Clicked Accept");
			<?php 
				$row = unserialize($stringRow);
                /// @TODO Update studentdetail as well
				updateTable("users", $row, $where = array("studentID" => $row["Student Number"]));
			?>
		}
		
		function deleteRow($stringRow)
		{
			alert("Clicked Delete");
			<?php 
				$row = unserialize($stringRow);
				deleteFromTable("users", $row);
			?>
		}
	<script>
</body>
</html>