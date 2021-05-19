
var ctx = document.getElementById('myChart').getContext('2d');

var graphData = {
    type: 'bar',
    data: {
        labels: [1, 2, 3, 4, 5, 6],
        datasets: [{
            label: 'PM2.5',
            data: [0, 0, 0, 0, 0, 0],
            backgroundColor: [
                'rgba(73, 198, 230, 0.5)',
            ],
            borderWidth: 1
        }]
    },
    options: { }
}

var myChart = new Chart(ctx, graphData);


var socket = new WebSocket('ws://localhost:8000/ws/graph/');

socket.onmessage = function(e) {
  var djangoData = JSON.parse(e.data);
  console.log(djangoData)

  var newGraphData = graphData.data.datasets[0].data;
  newGraphData.shift();
  newGraphData.push(djangoData.pm25);

  graphData.data.datasets[0].data = newGraphData;
  myChart.update();
}
