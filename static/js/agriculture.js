// Agricultural features JavaScript

function showSection(section) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    
    // Show selected section
    document.getElementById(`${section}-section`).classList.add('active');
    
    // Update navigation
    event.target.classList.add('active');
}

// Crop Recommendations
async function getCropRecommendations() {
    const location = document.getElementById('crop-location').value;
    const resultsDiv = document.getElementById('crop-results');
    
    if (!location) {
        resultsDiv.innerHTML = '<p class="error">Please enter a location</p>';
        return;
    }
    
    resultsDiv.innerHTML = '<p>Loading recommendations...</p>';
    
    try {
        const response = await fetch(`/api/agriculture/recommendations/${location}`);
        const data = await response.json();
        
        if (data.error) {
            resultsDiv.innerHTML = `<p class="error">${data.error}</p>`;
            return;
        }
        
        let html = `<h4>Current Conditions in ${location}</h4>
                   <p>Temperature: ${data.current_conditions.temperature}°C | 
                   Humidity: ${data.current_conditions.humidity}% | 
                   Wind: ${data.current_conditions.wind_speed} km/h</p>
                   <h4>Top Crop Recommendations</h4>`;
        
        data.recommendations.forEach(crop => {
            const scoreColor = crop.suitability_score >= 70 ? 'green' : 
                              crop.suitability_score >= 40 ? 'orange' : 'red';
            
            html += `<div class="crop-card">
                     <h5>${crop.crop} (${crop.category})</h5>
                     <p>Suitability Score: <span style="color: ${scoreColor}; font-weight: bold;">${crop.suitability_score}/100</span></p>
                     <p>Suitable: ${crop.suitable ? '✅ Yes' : '❌ No'}</p>
                     <ul>`;
            
            crop.recommendations.forEach(rec => {
                html += `<li>${rec}</li>`;
            });
            
            html += `</ul></div>`;
        });
        
        html += `<p><em>${data.summary}</em></p>`;
        resultsDiv.innerHTML = html;
        
    } catch (error) {
        resultsDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
}

// Irrigation Scheduler
async function getIrrigationSchedule() {
    const crop = document.getElementById('irrigation-crop').value;
    const soilMoisture = document.getElementById('soil-moisture').value;
    const resultsDiv = document.getElementById('irrigation-results');
    
    if (!crop) {
        resultsDiv.innerHTML = '<p class="error">Please select a crop</p>';
        return;
    }
    
    resultsDiv.innerHTML = '<p>Generating irrigation schedule...</p>';
    
    try {
        const response = await fetch('/api/agriculture/irrigation', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                crop: crop,
                location: 'Sulur',
                soil_moisture: parseInt(soilMoisture)
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            resultsDiv.innerHTML = `<p class="error">${data.error}</p>`;
            return;
        }
        
        let html = `<h4>Irrigation Schedule for ${data.crop}</h4>
                   <p>Water Requirement: ${data.water_requirement}</p>
                   <p>Current Soil Moisture: ${data.irrigation_needs.current_soil_moisture}%</p>
                   <p>Urgency: <strong>${data.irrigation_needs.urgency}</strong></p>
                   <h4>Schedule</h4>`;
        
        data.schedule.forEach(item => {
            html += `<div class="schedule-item">
                     <p><strong>${item.day} - ${item.time}</strong></p>
                     <p>Amount: ${item.amount_mm}mm | Method: ${item.method}</p>
                     <p>Priority: ${item.priority}</p>
                     </div>`;
        });
        
        html += `<h4>Next Irrigation</h4>
                <p>${data.next_irrigation.timing}</p>
                <p>${data.next_irrigation.reason}</p>
                <p>${data.next_irrigation.recommended}</p>`;
        
        resultsDiv.innerHTML = html;
        
    } catch (error) {
        resultsDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
}

// Farmer Action Plan
async function getActionPlan() {
    const location = document.getElementById('action-location').value;
    const resultsDiv = document.getElementById('action-results');
    
    if (!location) {
        resultsDiv.innerHTML = '<p class="error">Please enter a location</p>';
        return;
    }
    
    resultsDiv.innerHTML = '<p>Generating action plan...</p>';
    
    try {
        const response = await fetch('/api/agriculture/action-plan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                location: location,
                crops: []
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            resultsDiv.innerHTML = `<p class="error">${data.error}</p>`;
            return;
        }
        
        let html = `<h4>Action Plan for ${location}</h4>
                   <p>Priority Level: <strong>${data.priority_level}</strong></p>
                   <h4>Immediate Actions</h4><ul>`;
        
        data.immediate_actions.forEach(action => {
            html += `<li>${action}</li>`;
        });
        
        html += `</ul><h4>Short-term Actions</h4><ul>`;
        data.short_term_actions.forEach(action => {
            html += `<li>${action}</li>`;
        });
        
        html += `</ul><h4>Safety Considerations</h4><ul>`;
        data.safety_considerations.forEach(safety => {
            html += `<li>${safety}</li>`;
        });
        
        resultsDiv.innerHTML = html;
        
    } catch (error) {
        resultsDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
}

// Harvest Advisor
async function getHarvestAdvice() {
    const crop = document.getElementById('harvest-crop').value;
    const growthStage = document.getElementById('growth-stage').value;
    const resultsDiv = document.getElementById('harvest-results');
    
    if (!crop) {
        resultsDiv.innerHTML = '<p class="error">Please select a crop</p>';
        return;
    }
    
    resultsDiv.innerHTML = '<p>Getting harvest advice...</p>';
    
    try {
        const response = await fetch('/api/agriculture/harvest', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                crop: crop,
                location: 'Sulur',
                growth_stage: growthStage
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            resultsDiv.innerHTML = `<p class="error">${data.error}</p>`;
            return;
        }
        
        let html = `<h4>Harvest Recommendations for ${data.crop}</h4>
                   <p>Growth Stage: ${data.growth_stage}</p>
                   <p>Overall: <strong>${data.overall_recommendation}</strong></p>
                   <h4>Harvest Assessment</h4>
                   <p>Suitability Level: ${data.harvest_assessment.suitability_level}</p>
                   <p>Can Harvest Now: ${data.harvest_window.can_harvest_now ? '✅ Yes' : '❌ No'}</p>
                   <p>Optimal Time: ${data.harvest_window.optimal_time}</p>
                   <h4>Precautions</h4><ul>`;
        
        data.precautions.forEach(precaution => {
            html += `<li>${precaution}</li>`;
        });
        
        html += `</ul><h4>Post-Harvest Recommendations</h4><ul>`;
        data.post_harvest_recommendations.forEach(rec => {
            html += `<li>${rec}</li>`;
        });
        
        resultsDiv.innerHTML = html;
        
    } catch (error) {
        resultsDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
}

// Storm Impact Analyzer
async function getStormImpact() {
    const crop = document.getElementById('storm-crop').value;
    const resultsDiv = document.getElementById('storm-results');
    
    if (!crop) {
        resultsDiv.innerHTML = '<p class="error">Please select a crop</p>';
        return;
    }
    
    resultsDiv.innerHTML = '<p>Analyzing storm impact...</p>';
    
    try {
        const response = await fetch('/api/agriculture/storm-impact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                crop: crop,
                location: 'Sulur',
                growth_stage: 'mature'
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            resultsDiv.innerHTML = `<p class="error">${data.error}</p>`;
            return;
        }
        
        const riskColor = data.overall_risk_level === 'EXTREME RISK' ? 'red' : 
                         data.overall_risk_level === 'HIGH RISK' ? 'orange' : 
                         data.overall_risk_level === 'MODERATE RISK' ? 'yellow' : 'green';
        
        let html = `<h4>Storm Impact Analysis for ${data.crop}</h4>
                   <p>Storm Severity: <strong>${data.storm_severity.level}</strong></p>
                   <p>Overall Risk: <strong style="color: ${riskColor};">${data.overall_risk_level}</strong></p>
                   <p>Action Priority: <strong>${data.action_priority}</strong></p>
                   <h4>Impact Analysis</h4>
                   <p>Impact Level: ${data.impact_analysis.impact_level}</p>
                   <p>Expected Damage: ${data.impact_analysis.expected_damage_percentage}</p>
                   <h4>Protection Measures</h4><ul>`;
        
        data.protection_measures.immediate.forEach(measure => {
            html += `<li>${measure}</li>`;
        });
        
        html += `</ul><h4>Recovery Recommendations</h4><ul>`;
        data.recovery_recommendations.immediate_actions.forEach(rec => {
            html += `<li>${rec}</li>`;
        });
        
        resultsDiv.innerHTML = html;
        
    } catch (error) {
        resultsDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
}