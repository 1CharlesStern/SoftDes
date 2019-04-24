function myFunction() {

  init();
}

function loadJSON(callback) {

    var xobj = new XMLHttpRequest();
        xobj.overrideMimeType("application/json");
    xobj.open('GET', 'http://time.jsontest.com', true); // Replace 'my_data' with the path to your file
    xobj.onreadystatechange = function () {
          if (xobj.readyState == 4 && xobj.status == "200") {
            // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
            callback(xobj.responseText);
          }
    };
    xobj.send(null);
 }

 function reply_click(id)
 {
   var card = document.getElementById(id).children[0].children[0].children[3];
   //var c = document.getElementById("myDIV").children;
   console.log(card.innerHTML);
 }

function init() {
 loadJSON(function(response) {
    //var actual_JSON = JSON.parse(response);

    var driverOneData = '{"driverId":"driverOne","StartingPoint":"10N,70W", "Destination":"15N,50W", "DepartureTime":"4:15 4/24/19"}'

    var driverTwoData = '{"driverId":"driverTwo","StartingPoint":"70N,70W", "Destination":"20N,50W", "DepartureTime":"4:15 4/24/19"}'

    var driverThreeData = '{"driverId":"driverThree","StartingPoint":"100N,70W", "Destination":"150N,50W", "DepartureTime":"4:15 4/24/19"}'



    var totalJson = '{"data":[' + driverOneData + ',' + driverTwoData + ',' + driverThreeData + ']}';
    console.log(totalJson);
    var actual_JSON = JSON.parse(totalJson);

    //console.log(actual_JSON)
    for (i in actual_JSON.data) {
      var node = document.createElement("DIV");
      node.innerHTML = '<div class="overflowContainer" id="rideCardId'+i+'" onClick="reply_click(this.id)"><div class="card"><div class="driveContainer"><div class="cardElement">Starting Point: '+actual_JSON.data[i].StartingPoint+' </div><div class="cardElement">Destination: '+actual_JSON.data[i].Destination+' </div><div class="cardElement">Departure Time: '+actual_JSON.data[i].DepartureTime+'</div><p hidden>'+actual_JSON.data[i].driverId+'</p></div></div></div>'
      document.getElementById("driverList").appendChild(node);

    }
 });
}
