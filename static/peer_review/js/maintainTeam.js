/**
 * Created by Jeffrey Russell on 8/18/17.
*/

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

var tableLayout =
    "<'row text-right'<'col-lg-6'l><'col-lg-6'f>>" +
    "<'row'<'col-xs-12'tr>>" +
    "<'row'<'col-lg-6 text-center'i><'col-lg-6'p>>";

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
                "targets": [3]}],
            dom: tableLayout
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
                "targets": [3]}],
            dom: tableLayout
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