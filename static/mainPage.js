function init() {
  createCookie("test", "value", -1);
  loadJSON(function(response) {
    var actual_JSON = JSON.parse(response);
    console.log(actual_JSON)
  /*  var driverOneData = '{"routeId":"1","StartingPoint":"10N,70W", "Destination":"15N,50W", "DepartureTime":"4:15 4/24/19"}'

    var driverTwoData = '{"routeId":"2","StartingPoint":"70N,70W", "Destination":"20N,50W", "DepartureTime":"4:15 4/24/19"}'

    var driverThreeData = '{"routeId":"3","StartingPoint":"100N,70W", "Destination":"150N,50W", "DepartureTime":"4:15 4/24/19"}'

    //var totalJson = '{"data":[' + driverOneData + ',' + driverTwoData + ',' + driverTwoData+',' + driverTwoData + ','+ driverTwoData + ','+ driverTwoData + ','+ driverTwoData + ','+ driverTwoData + ','+ driverTwoData + ','+ driverThreeData + ']}';
    var totalJson = '{"data":[' + driverOneData + ',' + driverThreeData + ']}';
    console.log(totalJson);
    var actual_JSON = JSON.parse(totalJson);*/

    //console.log(actual_JSON)
    for (i in actual_JSON.data) {
      var node = document.createElement("DIV");
      node.innerHTML = '<div class="overflowContainer" id="rideCardId'+i+'" onClick="reply_click(this.id)"><div class="card"><div class="driveContainer"><div class="cardElement">Starting Point: '+actual_JSON.data[i].StartingPoint+' </div><div class="cardElement">Destination: '+actual_JSON.data[i].Destination+' </div><div class="cardElement">Departure Time: '+actual_JSON.data[i].DepartureTime+'</div><p hidden>'+actual_JSON.data[i].routeid+'</p></div></div></div>'
      document.getElementById("driverList").appendChild(node);

    }
 });
}

 function reply_click(id)
 {
   var card = document.getElementById(id).children[0].children[0].children[3];
   createCookie("routeid", card.innerHTML, 100);
   window.location.href = "/addStop";
 }
