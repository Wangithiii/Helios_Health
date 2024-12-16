document.addEventListener('DOMContentLoaded', () => {
    // Fetch the health logs data from the back end
    fetch('http://127.0.0.1:5000/health_logs')
      .then(response => response.json())
      .then(data => {
        const healthLogsTable = document.getElementById('health-logs').getElementsByTagName('tbody')[0];
        data.forEach(log => {
          const row = healthLogsTable.insertRow();
          row.innerHTML = `
            <td>${log.id}</td>
            <td>${log.date}</td>
            <td>${log.medication}</td>
            <td>${log.notes}</td>
          `;
        });
      })
      .catch(error => console.error('Error fetching health logs:', error));
  });
  