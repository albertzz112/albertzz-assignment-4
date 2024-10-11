document.getElementById('search-form').addEventListener('submit', function (event) {
    event.preventDefault();
    
    let query = document.getElementById('query').value;
    let resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'query': query
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);  // Check the structure of the data
        displayResults(data);
        displayChart(data);  // Display the chart with the results
    });
});

function displayResults(data) {
    let resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<h2>Results</h2>';
    for (let i = 0; i < data.documents.length; i++) {
        let docDiv = document.createElement('div');
        docDiv.innerHTML = `<strong>Document ${data.indices[i]}</strong><p>${data.documents[i]}</p><br><strong>Similarity: ${data.similarities[i]}</strong>`;
        resultsDiv.appendChild(docDiv);
    }
}

function displayChart(data) {
    const ctx = document.getElementById('similarity-chart').getContext('2d');

    const chartData = {
        labels: data.indices,  // Use document indices as labels
        datasets: [{
            label: 'Similarity Scores',
            data: data.similarities,  // Similarity scores
            backgroundColor: 'rgba(75, 192, 192, 0.2)',  // Bar background color
            borderColor: 'rgba(75, 192, 192, 1)',  // Border color of the bars
            borderWidth: 1  // Border width of the bars
        }]
    };

    const chartOptions = {
        responsive: true,  // Make the chart responsive
        scales: {
            y: {
                beginAtZero: true  // Set the y-axis to start at 0
            }
        }
    };

    // Clear any existing chart before creating a new one
    if (window.similarityChart) {
        window.similarityChart.destroy();  // Destroy the old chart
    }

    // Create a new chart
    window.similarityChart = new Chart(ctx, {
        type: 'bar',  // Type of chart (bar chart in this case)
        data: chartData,  // Data for the chart
        options: chartOptions  // Chart options
    });
}
