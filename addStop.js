function init() {
  var routeId = getCookie("routeId");
  if(routeId == ""){
    window.location.href = "./mainPage.html";
  }
}
