// Weather Intelligence Analytics Dashboard
let temperatureChart, humidityChart, windChart, hazardChart;

// Load analytics for a location
async function loadAnalytics() {
    const location = document.getElementById('analytics-location').value;
    if (!location) {
        alert('Please enter a location');
        return;
    }

    try {
        // Fetch weather analytics
        const weatherResponse = await fetch(`/api/analytics/weather/${location}`);
        const weatherData = await weatherResponse.json();

        if (weatherData.error) {
            alert(weatherData.error);
            return;
        }

        // Update overview cards
        updateOverviewCards(weatherData);

        // Update charts
        updateCharts(weatherData);

        // Fetch hazard analytics
        const hazardResponse = await fetch(`/api/analytics/hazards/${location}`);
        const hazardData = await hazardResponse.json();

        if (!hazardData.error) {
            updateHazardBreakdown(hazardData);
        }

    } catch (error) {
        console.error('Error loading analytics:', error);
        alert('Failed to load analytics data');
    }
}

// Update overview cards
function updateOverviewCards(data) {
    document.getElementById('temp-value').textContent = data.temperature.current ? `${data.temperature.current.toFixed(1)}°C` : '--';
    document.getElementById('feels-like').textContent = data.temperature.feels_like ? `${data.temperature.feels_like.toFixed(1)}°C` : '--';
    document.getElementById('temp-min').textContent = data.temperature.min ? `${data.temperature.min.toFixed(1)}°C` : '--';
    document.getElementById('temp-max').textContent = data.temperature.max ? `${data.temperature.max.toFixed(1)}°C` : '--';

    document.getElementById('humidity-value').textContent = data.humidity || '--';
    document.getElementById('pressure-value').textContent = data.pressure || '--';

    document.getElementById('wind-value').textContent = data.wind.speed ? data.wind.speed.toFixed(1) : '--';
    document.getElementById('wind-direction').textContent = data.wind.direction || '--';

    if (data.safety_score !== null) {
        document.getElementById('safety-value').textContent = data.safety_score;
        document.getElementById('risk-level').textContent = data.risk_level;
    } else {
        document.getElementById('safety-value').textContent = 'N/A';
        document.getElementById('risk-level').textContent = 'Not available';
    }
}

// Update charts
function updateCharts(data) {
    // Temperature Chart
    const tempCtx = document.getElementById('temperature-chart').getContext('2d');
    if (temperatureChart) {
        temperatureChart.destroy();
    }
    temperatureChart = new Chart(tempCtx, {
        type: 'bar',
        data: {
            labels: ['Current', 'Feels Like', 'Min', 'Max'],
            datasets: [{
                label: 'Temperature (°C)',
                data: [
                    data.temperature.current || 0,
                    data.temperature.feels_like || 0,
                    data.temperature.min || 0,
                    data.temperature.max || 0
                ],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(255, 159, 64, 0.7)',
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(255, 205, 86, 0.7)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 205, 86, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Humidity & Pressure Chart
    const humCtx = document.getElementById('humidity-chart').getContext('2d');
    if (humidityChart) {
        humidityChart.destroy();
    }
    humidityChart = new Chart(humCtx, {
        type: 'doughnut',
        data: {
            labels: ['Humidity', 'Remaining'],
            datasets: [{
                data: [data.humidity || 0, 100 - (data.humidity || 0)],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(201, 203, 207, 0.7)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(201, 203, 207, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    // Wind Chart
    const windCtx = document.getElementById('wind-chart').getContext('2d');
    if (windChart) {
        windChart.destroy();
    }
    windChart = new Chart(windCtx, {
        type: 'polarArea',
        data: {
            labels: ['Wind Speed', 'Direction', 'Visibility', 'Clouds'],
            datasets: [{
                data: [
                    data.wind.speed || 0,
                    (data.wind.direction || 0) / 10,
                    (data.visibility || 0) / 1000,
                    data.clouds || 0
                ],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 205, 86, 0.7)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 205, 86, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    // Hazard Chart (placeholder - will be updated with hazard data)
    const hazardCtx = document.getElementById('hazard-chart').getContext('2d');
    if (hazardChart) {
        hazardChart.destroy();
    }
    hazardChart = new Chart(hazardCtx, {
        type: 'radar',
        data: {
            labels: ['Flood', 'Heat', 'Wind', 'Visibility', 'Storm'],
            datasets: [{
                label: 'Risk Level',
                data: [0, 0, 0, 0, 0],
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

// Update hazard breakdown
function updateHazardBreakdown(data) {
    document.getElementById('flood-risk').textContent = data.flood_risk;
    document.getElementById('heat-risk').textContent = data.heat_risk;
    document.getElementById('wind-risk').textContent = data.wind_risk;
    document.getElementById('visibility-risk').textContent = data.visibility_risk;
    document.getElementById('storm-risk').textContent = data.storm_risk;

    // Update hazard chart
    const riskMap = { 'low': 20, 'medium': 50, 'high': 80 };
    if (hazardChart) {
        hazardChart.data.datasets[0].data = [
            riskMap[data.flood_risk] || 0,
            riskMap[data.heat_risk] || 0,
            riskMap[data.wind_risk] || 0,
            riskMap[data.visibility_risk] || 0,
            riskMap[data.storm_risk] || 0
        ];
        hazardChart.update();
    }
}

// Compare multiple locations
async function compareLocations() {
    const locationsInput = document.getElementById('compare-locations').value;
    if (!locationsInput) {
        alert('Please enter locations to compare');
        return;
    }

    const locations = locationsInput.split(',').map(loc => loc.trim()).filter(loc => loc);
    if (locations.length < 2) {
        alert('Please enter at least 2 locations to compare');
        return;
    }

    try {
        const response = await fetch('/api/analytics/compare', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ locations })
        });

        const data = await response.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        displayComparisonResults(data.comparisons);

    } catch (error) {
        console.error('Error comparing locations:', error);
        alert('Failed to compare locations');
    }
}

// Display comparison results
function displayComparisonResults(comparisons) {
    const container = document.getElementById('comparison-results');
    const table = document.getElementById('comparison-table');

    container.style.display = 'block';

    let html = `
        <table class="comparison-table">
            <thead>
                <tr>
                    <th>Location</th>
                    <th>Temperature (°C)</th>
                    <th>Humidity (%)</th>
                    <th>Conditions</th>
                    <th>Safety Score</th>
                    <th>Risk Level</th>
                </tr>
            </thead>
            <tbody>
    `;

    comparisons.forEach(comp => {
        html += `
            <tr>
                <td>${comp.location}</td>
                <td>${comp.temperature ? comp.temperature.toFixed(1) : 'N/A'}</td>
                <td>${comp.humidity || 'N/A'}</td>
                <td>${comp.conditions || 'N/A'}</td>
                <td>${comp.safety_score !== undefined ? comp.safety_score : 'N/A'}</td>
                <td>${comp.risk_level || 'N/A'}</td>
            </tr>
        `;
    });

    html += `
            </tbody>
        </table>
    `;

    table.innerHTML = html;
}

// Show section helper
function showSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });

    // Show selected section
    document.getElementById(`${sectionName}-section`).classList.add('active');

    // Update nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');

    // Load analytics if switching to analytics section
    if (sectionName === 'analytics') {
        loadAnalytics();
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Load analytics for default location when analytics section is shown
    const analyticsBtn = document.querySelector('button[onclick="showSection(\'analytics\')"]');
    if (analyticsBtn) {
        analyticsBtn.addEventListener('click', loadAnalytics);
    }
});
