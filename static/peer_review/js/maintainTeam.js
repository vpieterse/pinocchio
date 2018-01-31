/**
 * Created by Jeffrey Russell on 8/18/17.
*/

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
function isAlphaNumeric(str) {
  var code, i, len;

  for (i = 0, len = str.length; i < len; i++) {
    code = str.charCodeAt(i);
    if (!(code > 47 && code < 58) && // numeric (0-9)
        !(code > 64 && code < 91) && // upper alpha (A-Z)
        !(code > 96 && code < 123)) { // lower alpha (a-z)
      return false;
    }
  }
  return true;
}


var UserHandler = function(userTableElement) {
    var self = this;
    this.users = {};
    //this.userDataTable;
    this.userTableElement = userTableElement;
    this.teamDataTables = [];
    this.currentTeam = "";
    this.roundID = "";
    this.init = function() {
        self.userDataTable = self.userTableElement.DataTable({
            "orderClasses": false,
            "columnDefs": [{
                "orderable": false,
                "searchable": false,
                "render": function (data, type, full) {
                    return "<div class=\"addUser button\" data-id='" + full.DT_RowId + "'><span class=\"glyphicon glyphicon-chevron-right\"></span></div>"
                },
                "targets": [3]}]
        });

        self.userDataTable.on("draw", self.onDraw);
        self.userDataTable.draw(false);

        self.addUsers(self.userDataTable.rows().data(), true);
    };

    this.addUser = function(user, redraw, dontAdd) {
        redraw = typeof redraw !== 'undefined' ? redraw : true;
        dontAdd = typeof dontAdd !== 'undefined' ? dontAdd : false;
        /** @namespace user.DT_RowId */
        if(user.DT_RowId && !user.id) {
            user.id = user.DT_RowId;
        }
        if(!user.id) {
            console.log(user);
            throw "User must have an id";
        }
        if(self.users[user.id]) {
            throw "This user already exists";
        }
        if(!user.status) {
            user.status = "list";
        }
        if(!user.team) {
            user.team = "";
        }
        self.users[user.id] = user;
        if(!dontAdd) {
            self.userDataTable.row.add(user);
        }
        if(redraw) {
            self.userDataTable.draw(false);
        }
    };

    this.addUsers = function(users, dontAdd) {
        console.log(users);
        for(var i in users) {
            if(!isNaN(Number(i)) && users.hasOwnProperty(i)) {

                self.addUser(users[i], false, dontAdd);
            }
        }
        self.userDataTable.draw(false);
    };

    this.moveUserUpdateAJAX = function(userID, teamID) {
        $.ajax({
            url: '/maintainTeam/changeUserTeamForRound/'+self.roundID+'/'+userID+'/'+teamID+'/',
            type: 'GET',
            success: function(data) {
                console.log(data);
                if(data["success"] === true)
                {
                    console.log("Changed user: "+userID+" to team: "+teamID+" for round: "+self.roundID);
                }
                else
                {
                    console.log("ERROR: Could not change user: "+userID+" to team: "+teamID+" for round: "+self.roundID);
                }
            },
            error: function() {
                console.log("ERROR: Could not change user: "+userID+" to team: "+teamID+" for round: "+self.roundID);
            }
        });
    };

    this.moveUserToTeam = function(userID, teamID, dontAdd) {
        dontAdd = typeof dontAdd !== 'undefined' ? dontAdd : false;
        var user = self.users[userID];
        if(!user) {
            throw "Cannot find user, " + userID + ", in users";
        }
        if(user.status !== "list") {
            throw "Cannot move user from one team directly to another";
        }
        user.status = "team";
        user.team = teamID;

        self.userDataTable.row("#" + userID).remove();
        self.userDataTable.draw(false);


        if(!dontAdd) {
            self.moveUserUpdateAJAX(userID, teamID);
            self.teamDataTables[teamID].row.add(user);
            self.teamDataTables[teamID].draw(false);
            $("#" + teamID + "_size").text(self.teamDataTables[teamID].rows().count());
        }
    };

    this.removeUserFromTeam = function(userID, justGraphical) {
        var user = self.users[userID];
        if(!user) {
            throw "Cannot find user, " + userID + ", in users";
        }
        if(user.status !== "team") {
            throw "Cannot remove user from a team if they are not already in a team";
        }
        var oldTeamID = user.team;

        user.status = "list";
        user.team = "";

        if(!justGraphical) {
            self.moveUserUpdateAJAX(userID, "emptyTeam");
        }

        self.teamDataTables[oldTeamID].row("#" + userID).remove();
        self.teamDataTables[oldTeamID].draw(false);
        $("#" + oldTeamID + "_size").text(self.teamDataTables[oldTeamID].rows().count());

        self.userDataTable.row.add(user);
        self.userDataTable.draw(false);
    };

    this.onDraw = function(e) {
        var dt = $(e.currentTarget).DataTable();
        dt.$(".removeUser").removeClass("removeUser").on("click", self.onRemoveUser);
        dt.$(".addUser").removeClass("addUser").on("click", self.onAddUser);
    };

    this.onRemoveUser = function(e) {
        self.removeUserFromTeam(e.currentTarget.getAttribute("data-id"));
    };

    this.onAddUser = function(e) {
        if(self.currentTeam === "") {
            alert("You must open a team on the right in order to add this person to it");
            return;
        }
        self.moveUserToTeam(e.currentTarget.getAttribute("data-id"), self.currentTeam);
    };

    this.addTeam = function(html, teamID) {
        if(self.teamDataTables[teamID]) {
            throw "That team already exists";
        }
        var $teams = $("#teams");
        $teams.append(html);
        self.teamDataTables[teamID] = $("#" + teamID + " .teamTable").DataTable({
            "orderClasses": false,
            "columnDefs": [{
                "orderable": false,
                "searchable": false,
                "render": function (data, type, full) {
                    return "<div class=\"removeUser button\" data-id='" + full.DT_RowId + "'><span class=\"glyphicon glyphicon-chevron-left\"></span></div>"
                },
                "targets": [3]}]
        });
        $teams.find(".panel-heading").unbind("click").on("click", function(event) {
            console.log(event.currentTarget.classList.contains("collapsed"));
            self.currentTeam = event.currentTarget.getAttribute("href").substring(1);
        });
        self.teamDataTables[teamID].on("draw", self.onDraw);
        self.teamDataTables[teamID].draw(false);

        var rows = self.teamDataTables[teamID].rows().data();

        for(var i in rows) {
            if(!isNaN(Number(i)) && rows.hasOwnProperty(i)) {
                self.moveUserToTeam(rows[i].DT_RowId, teamID, true);
            }
        }
    };

    this.resetTeams = function() {
        for(var i in self.users) {
            if(self.users.hasOwnProperty(i)) {
                if(self.users[i].status === "team") {
                    self.removeUserFromTeam(i, true);
                }
            }
        }
        $("#teams").empty();
        self.teamDataTables = {};
        self.currentTeam = "";
    };

    this.hasTeam = function(teamID) {
        return self.teamDataTables[teamID];
    }
};

var userList = [];
var RoundHandler;
RoundHandler = function (dropdownSelector, userHandler) {
    var self = this;
    this.dropdownSelector = dropdownSelector;
    this.roundDescriptionSelector = "#roundDesc";
    this.userHandler = userHandler;
    self.roundID = "";
    this.init = function () {
        self.dropdown = $(self.dropdownSelector);
        self.dropdown.on("change", self.changeRoundClicked);
        self.roundDescription = $(self.roundDescriptionSelector);
    };

    this.changeRoundClicked = function (event) {
        var options = event.target.options;
        var selectedOption = options[options.selectedIndex];
        self.changeRound(selectedOption.getAttribute("value"), selectedOption.getAttribute("desc"));
    };
    this.changeRound = function (roundID, description) {
        self.roundID = roundID;
        self.userHandler.roundID = roundID;
        if (roundID === '') {
            self.roundDescription.html("Please select a round above");
        }
        else {
            self.roundDescription.html(description);
            $.ajax({
                url: '/maintainTeam/getTeamsForRound/' + roundID,
                type: 'GET',
                success: self.changeRoundResult,
                error: function () {
                    console.log('Error: getTeamsForRound');
                }
            });
        }
    };

    this.changeRoundResult = function (data) {
        /** @namespace data.teamTables */
        var teamTables = data.teamTables,
            $teams = $("#teams"),
            i,
            teamTable;
        $teams.empty();
        self.userHandler.resetTeams();
        for (i in teamTables) {
            if (teamTables.hasOwnProperty(i)) {
                console.log("hey");
                teamTable = teamTables[i];
                self.userHandler.addTeam(teamTable, i);
            }
        }
        $teams.find(".panel-heading").first().addClass("collapsed").trigger("click");

    };
};
var PageHandler = function() {
    var self = this;
    this.userTableSelector = "#users";
    this.roundDropdownSelector = "#selectedRound";
    this.init = function() {
        self.userTable = $(self.userTableSelector);
        self.userHandler = new UserHandler(self.userTable);
        self.userHandler.init();
        self.roundHandler = new RoundHandler(self.roundDropdownSelector, self.userHandler);
        self.roundHandler.init();
        $("#addTeam").parent("h4").parent("div").on("click", self.addTeamClick);
    };

    this.addTeamClick = function() {
        if(self.roundHandler.roundID !== "") {
            var teamName = prompt("Please enter a team name");
            if(teamName !== null) {
                if (teamName !== "") {
                    if(isAlphaNumeric(teamName)) {
                        if (!self.userHandler.hasTeam(teamName)) {
                            $.ajax({
                                url: "/maintainTeam/getNewTeam/" + teamName,
                                type: "GET",
                                success: function (data) {
                                    self.userHandler.addTeam(data['team'], teamName);
                                },
                                error: function () {
                                    console.log("ERROR: Could not add new team: " + teamName + " to status: ");
                                }
                            });
                        } else {
                            alert("That team already exists");
                        }
                    } else {
                        alert("Please only use numbers and letters");
                    }
                } else {
                    alert("That name was blank");
                }
            }
        } else {
            alert("Please select a round");
        }
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