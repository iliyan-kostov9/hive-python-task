document.addEventListener("mousemove", function (event) {
  var x = event.clientX;
  var y = event.clientY;

  document.getElementById("x-coord").innerText = x;
  document.getElementById("y-coord").innerText = y;

  console.log(window.location.hostname);

  var request = new XMLHttpRequest();
  request.open("POST", "/send-coords", true);
  request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  request.send(JSON.stringify({ x: x, y: y }));
});
