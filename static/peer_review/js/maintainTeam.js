/**
 * Created by jeffreyrussell on 8/18/17.

function addTeam()
{
    if(roundId == '')
    {
        alert("Please select a round");
    }
    else
    {
        var teamID = prompt('Team name:', 'Team'+(numTeams+1));
        while($("#"+teamID).length != 0 || teamID == "emptyTeam" || teamID.includes(' '))
        {
            if(teamID.includes(' '))
                teamID = prompt('Spaces are not allowed. Please use the "_" or "-" character instead:', teamID);
            else
                teamID = prompt('Team name already in use:', teamID);
        }
        if(teamID != null)
        {
            addTeamCont(teamID, 0);
        }
    }
}

function addTeamCont(teamID, teamSize)
{
    numTeams++;
    var newTeam = '<div class="panel panel-default">'+
                  '     <div class="panel-heading" data-toggle="collapse" data-parent="#teams" href="#'+teamID+'">'+
                  '         <div class="panel-title">'+
                  '             <div class="pull-left">'+
                  '                <h4>'+
                  '                   <input type="button" value="-" class="btn btn-info btn-xs minus" field="" onclick="removeTeam(\''+teamID+'\')"/>'+
                  '                   <a data-toggle="collapse" style="color:black" data-parent="#teams" href="#'+teamID+'">'+
                  '                       '+teamID+''+
                  '                   </a>'+
                  '                </h4>'+
                  '             </div>'+
                  '             <div class="panel-title pull-right">'+
                  '                 <a data-toggle="collapse" data-parent="#teams" href="#'+teamID+'">'+
                  '                     <h4>'+
                  '                         <span class="team-size">'+teamSize+'</span><b class="caret"></b>'+
                  '                     </h4>'+
                  '                 </a>'+
                  '             </div>'+
                  '         </div>'+
                  '      <div class="clearfix"></div>'+
                  '      <div id="'+teamID+'" class="panel-collapse collapse  panel-team">'+
                  '          <div class="panel-body">'+
                  '              <table class="table sortable moveable teamTable">'+
                  '                  <thead>'+
                  '                      <tr>'+
                  '                          <th>User Name</th>'+
                  '                          <th>Name</th>'+
                  '                          <th>Surname</th>'+
                  '                          <th></th>'+
                  '                      </tr>'+
                  '                  </thead>'+
                  '                  <tbody>'+
                  '                  </tbody>'+
                  '              </table>'+
                  '          </div>'+
                  '      </div>'+
                  '  </div>';
    $("#teams").append(newTeam);

    $("#"+teamID).find(".teamTable").DataTable({
        "orderClasses": false,
            "columnDefs": [{
                "orderable": false,
                "searchable": false,
                "render": function (data, type, full, meta) {
                    return "<div class=\"removeUser button\" '><span class=\"glyphicon glyphicon-remove-circle\"></span></div>"
                },
                "targets": [3]}]
    });
}

function removeTeam(teamID)
{
    if(confirm("You are about to delete team " + teamID +". Do you want to do this?"))
    {
        $("#"+teamID).find('div.removeUser').click();
        $("#"+teamID).parent(1).remove();
    }
}

function moveUser(fromTable, toTable, row)
{
    var tr = fromTable.row(row);
    var node = tr.node();
    tr.remove();
    toTable.row.add(node).draw();
}

function changeStatus(teamId, newStatus)
{
    $.ajax({
        url: "/maintainTeam/changeTeamStatus/"+teamId+"/"+newStatus,
        type: "GET",
        success: function(data) {
            if(data["success"] == true)
            {
                console.log("Changed team: "+teamId+" to status: "+status);
            }
            else
            {
                console.log("ERROR: Could not change team: "+teamId+" to status: "+status);
            }
        },
        failure: function(data) {
            console.log("ERROR: Could not change team: "+teamId+" to status: "+status);
        }
    });
}

$(document).ready(function () {

    if ('{{ roundPk }}' != 'none')
    {
        $("#selectedRound").val('{{ roundPk }}')
        $("#selectedRound").change();
    }

    $("#teamViewTable").DataTable({
        "orderClasses": false
    });

    var users = $("#users").DataTable({
        "orderClasses": false,
        "columnDefs": [{
            "orderable": false,
            "searchable": false,
            "render": function (data, type, full, meta) {
                return "<div class=\"addUser button\"><span class=\"glyphicon glyphicon-chevron-right\"></span></div>"
            },
            "targets": [3]}]
    });

    $('#teams').on('hide.bs.collapse', '.panel-team', function() {
        selected = "";
    });

    $('#teams').on('shown.bs.collapse', '.panel-team', function(e) {
        selected = e.currentTarget.id;
    });

    function changeTeam(user_id, roundId, newTeam)
    {
        $.ajax({
            url: '/maintainTeam/changeUserTeamForRound/'+roundId+'/'+user_id+'/'+newTeam+'/',
            type: 'GET',
            success: function(data) {
                if(data["success"] == true)
                {
                    console.log("Changed user: "+user_id+" to team: "+newTeam+" for round: "+roundId);
                }
                else
                {
                    console.log("ERROR: Could not change user: "+user_id+" to team: "+newTeam+" for round: "+roundId);
                }
            },
            failure: function(data) {
                console.log("ERROR: Could not change user: "+user_id+" to team: "+newTeam+" for round: "+roundId);
            }
        });
    }

    $('.moveable tbody').on('click', 'div.addUser', function() {
        if(selected != "" && $("#"+selected+" .in") != null)
        {
            var teamTable = $("#"+selected).find(".teamTable").DataTable();
            if(teamTable != null)
            {
                var row = $(this).parents('tr');
                if (!loading)
                {
                    var user_id=row[0].id;
                    var newTeam = selected;
                    changeTeam(user_id, roundId, newTeam);
                }
                moveUser(users, teamTable, row);
            }
        }
    });

    $(document).on('click', 'div.removeUser', function() {
        var teamSizeElement = $(this).closest(".panel-heading").find(".team-size");
        var newTeamSize = teamSizeElement.text()*1-1;
        teamSizeElement.text(newTeamSize);
        var teamTable = $(this).parents("table").DataTable();

        var row = $(this).parents('tr');
        moveUser(teamTable, users, row);

        if(!loading)
        {
            var user_id = row[0].id;
            changeTeam(user_id, roundId, "emptyTeam");
        }
    });

    $('#selectedRound').on('change', function() {
        loading = true;
        $("#teams").find("div.removeUser").click();
        $("#teams").html("");
        roundId = this.value;
        desc = $("#selectedRound > option[value="+roundId+"]").attr("desc");
        if(roundId == '')
        {
            $("#roundDesc").html("Please select a round above");
        }
        else
        {
            $("#roundDesc").html(desc);
            $.ajax({
                url: '/maintainTeam/getTeamsForRound/' + roundId,
                type: 'GET',
                success: function(data) {
                    for(var team in data)
                    {
                        team = data[team];
                        if($("#"+team["teamName"]).length == 0)
                        {
                            addTeamCont(team["teamName"], team["teamSize"]);
                        }

                        selected = team["teamName"];
                        $("#"+team["teamName"]).addClass("in");

                        $("#users").find("#"+team["user_id"]).find('div.addUser').click();

                        $("#"+team["teamName"]).removeClass("in");
                        selected = "";
                    }
                },
                failure: function(data) {
                    console.log('Error: getTeamsForRound');
                }
            });
        }
        loading = false;
    });

    $("#collapseThree").on('shown.bs.collapse', function() {
        $.ajax({
            url: '/maintainTeam/getTeams/',
            type: 'GET',
            success: function(data) {
                var table = $("#teamViewTable").DataTable();
                table.clear().draw();
                for(var team in data) {
                    team = data[team];
                    var teamName = team["team"];
                    var status = team["status"];
                    var row = table.row.add([
                            team["user_id"],
                            team["initials"],
                            team["surname"],
                            team["round"],
                            teamName,

                        ]).draw(false).node();
                    $(row).attr("id", team["teamId"]);
                    $(row).find("."+status).attr("selected", "selected");
                }
            },
            failure: function(data) {
                console.log("ERROR: Could not change user: "+user_id+" to team: "+newTeam+" for round: "+roundId)
            }
        });
    });

    $("#teamViewTable").on('change', '.status', function() {
        var row = $(this).parents('tr');
        changeStatus($(row).attr("id"), $(this).val());
    });
});*/

var userList = [];
var RoundHandler = function(dropdownSelector) {
    var self = this;
    this.dropdownSelector = dropdownSelector;
    this.roundDescriptionSelector = "#roundDesc";
    this.init = function() {
        self.dropdown = $(self.dropdownSelector)
        self.dropdown.on("change", self.changeRoundClicked);
        self.roundDescription = $(self.roundDescriptionSelector);
    };

    this.changeRoundClicked = function(event) {
        var options = event.target.options;
        var selectedOption = options[options.selectedIndex];
        self.changeRound(selectedOption.getAttribute("value"), selectedOption.getAttribute("desc"));
    };
    this.changeRound = function(roundId, description) {
        if (roundId == '') {
            self.roundDescription.html("Please select a round above");
        }
        else {
            self.roundDescription.html(description);
            $.ajax({
                url: '/maintainTeam/getTeamsForRound/' + roundId,
                type: 'GET',
                success: self.changeRoundResult,
                error: function () {
                    console.log('Error: getTeamsForRound');
                }
            });
        }
    };

    this.changeRoundResult = function(data) {
        var users = data.users,
            teamTables = data.teamTables,
            userId,
            user,
            i,
            teamTable;
        for(userId in users){
            if(users.hasOwnProperty(userId)) {
                user = users[userId];
                userList[userId].addClass("hidden");
            }
        }

        for(i in teamTables) {
            if(teamTables.hasOwnProperty(i)) {
                teamTable = teamTables[i];
                $("#teams").append(teamTable);
            }
        }

    };
};
var PageHandler = function() {
    var self = this;
    this.userTableSelector = "#users";
    this.roundDropdownSelector = "#selectedRound";
    this.init = function() {
        self.userTable = $(self.userTableSelector);
        self.userTable.DataTable({
            "orderClasses": false,
            "columnDefs": [{
                "orderable": false,
                "searchable": false,
                "render": function (data, type, full, meta) {
                    return "<div class=\"addUser button\"><span class=\"glyphicon glyphicon-chevron-right\"></span></div>"
                },
                "targets": [3]}]
        });
        self.roundHandler = new RoundHandler(self.roundDropdownSelector);
        self.roundHandler.init();
    }
};

function createUserList() {
    $("#users").find("tbody tr").each(function() {
        var $this = $(this);
        userList[$this.attr("id")] = $this;
    });
}
var pageHandler = new PageHandler();
$(document).ready(pageHandler.init);
$(document).ready(createUserList);