const ctx = document.getElementById("myChart");

new Chart(ctx, {
  type: "line",
  data: {
    labels: ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"],
    datasets: [
      {
        label: "# of Votes",
        data: [10, 6.5, 7.6, 7.9, 8.6, 8.5],
        borderWidth: 1,
      },
    ],
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  },
});
