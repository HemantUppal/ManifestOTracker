<script>
const pieCtx = document.getElementById('pieChart').getContext('2d');
new Chart(pieCtx, {
  type: 'pie',
  data: {
    labels: ['Completed', 'Not Completed'],
    datasets: [{
      label: 'Promise Completion',
      data: [{{ completed_percentage }}, {{ not_completed_percentage }}],
      backgroundColor: ['rgba(75, 192, 192, 0.7)', 'rgba(255, 99, 132, 0.7)']
    }]
  },
  options: {
    responsive: true,
    plugins: { title: { display: true, text: 'Promise Completion Status' } }
  }
});

const barCtx = document.getElementById('barChart').getContext('2d');
new Chart(barCtx, {
  type: 'bar',
  data: {
    labels: {{ bar_labels|tojson }},
    datasets: [{
      label: 'Number of Complaints',
      data: {{ bar_data|tojson }},
      backgroundColor: 'rgba(54, 162, 235, 0.6)',
      borderColor: 'rgba(54, 162, 235, 1)',
      borderWidth: 1
    }]
  },
  options: {
    responsive: true,
    scales: { y: { beginAtZero: true } },
    plugins: { title: { display: true, text: 'Complaints per Promise' } }
  }
});

function filterList(inputId, listId) {
  const input = document.getElementById(inputId);
  const filter = input.value.toLowerCase();
  const items = document.getElementById(listId).getElementsByClassName('promise-box');
  for (let i = 0; i < items.length; i++) {
    const txtValue = items[i].textContent || items[i].innerText;
    items[i].style.display = txtValue.toLowerCase().indexOf(filter) > -1 ? "" : "none";
  }
}
</script>