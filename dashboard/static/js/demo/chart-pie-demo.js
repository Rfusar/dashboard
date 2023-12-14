// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

fetch('/dati')
  .then(res => res.json())
  .then(data => {
    const mesi = data[1]
    const token = data[0]




    var ctx = document.getElementById("myPieChart");
    var myPieChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: mesi,
        datasets: [{
          data: token,
          backgroundColor: ['green', 'green', 'green', "red", "red", "red", "orange", "orange", "orange", "blue", "blue", "blue"],
          hoverBackgroundColor: ['violet', 'violet', 'violet', 'violet', 'violet', 'violet', 'violet', 'violet', 'violet', 'violet', 'violet', 'violet'],
          hoverBorderColor: "rgba(234, 236, 244, 1)",
        }],
      },
      options: {
        maintainAspectRatio: false,
        tooltips: {
          backgroundColor: "rgb(255,255,255)",
          bodyFontColor: "#858796",
          borderColor: '#dddfeb',
          borderWidth: 1,
          xPadding: 15,
          yPadding: 15,
          displayColors: false,
          caretPadding: 10,
        },
        legend: {
          display: false
        },
        cutoutPercentage: 80,
      },
    });
  });


