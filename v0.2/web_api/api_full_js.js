
/*
gatherDataAjaxRunning = false;
function gatherData(){
    // stop overlapping requests
    if(gatherDataAjaxRunning) return;

    gatherDataAjaxRunning = true;
    let postData = {
        "action": "readData"
    };
    $.post( "/api", postData, function( data ) {
        // handle gauge
        potPercent = parseInt(parseInt(data.pot_value) * 100 / 65000);
        gauge.set(potPercent);
        $('#potValue').html(potPercent);
        $('#potValue').removeClass(["bg-success", "bg-warning", "bg-danger"]);
        if(potPercent <= 60) {
            $('#potValue').addClass("bg-success");
        }
        else if(potPercent <= 80) {
            $('#potValue').addClass("bg-warning");
        }
        else {
            $('#potValue').addClass("bg-danger");
        }

        // handle temp gauge
        temp = parseFloat(data.temp_value);
        tempGauge.set(temp);
        $('#tempValue').html(temp.toFixed(1));
        $('#tempValue').removeClass(["bg-success", "bg-warning", "bg-danger"]);
        if(temp <= 15) {
            $('#tempValue').addClass("bg-primary");
        }
        else if(temp <= 25) {
            $('#tempValue').addClass("bg-success");
        }
        else {
            $('#tempValue').addClass("bg-danger");
        }

        // handle rgb leds
        for(count = 0; count < 8; count ++){
            let colour = "rgb(" + (parseInt(data.rgb_leds[count][0])*2) + ", "
                    + (parseInt(data.rgb_leds[count][1])*2) + ", "
                    + (parseInt(data.rgb_leds[count][2])*2);
            $("#rgb_" + count).css("background-color", colour);
        }

        // allow next data gather call
        gatherDataAjaxRunning = false;

    });
}
*/

function load_character(game, pc_name) {
    let postData = {
        "action" : "load_character",
        "game_name": game,
        "pc_name" : pc_name
    };
    $.post("/api", postData, function(data) {
        console.log(data);
        if (data.status != "OK") {
            alert("Error loading character");
        }
        else {
            //load the character
        }
    });
}

function get_all_characters_in_game(game_name) {
    let postData = {
        "action" : "get_all_characters",
        "game_name": game_name
    };
    $.post("/api", postData, function(data) {
        console.log(data);
        if (data.status != "OK") {
            alert("Error getting characters");
        }
        else {
            //process data
        }
    });
}

var selected_game = "";
function set_game(game_name) {
    selected_game = game_name;
}

$( document ).ready(function() {
    
});
