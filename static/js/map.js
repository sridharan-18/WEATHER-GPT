// Initialize the map
const map = L.map('map').setView([11.0047, 77.0153], 10); // Centered on Sulur, India

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Layer groups for different hazard types
const layers = {
    flood: L.layerGroup(),
    heat: L.layerGroup(),
    lightning: L.layerGroup(),
    visibility: L.layerGroup()
};

// Add all layers to map (initially empty)
Object.values(layers).forEach(layer => layer.addTo(map));

// Hazard risk data (simulated data for demonstration)
const hazardData = {
    flood: [
        { lat: 11.0047, lng: 77.0153, risk: 'high', location: 'Sulur Town' },
        { lat: 11.0200, lng: 77.0300, risk: 'medium', location: 'Near Airport' },
        { lat: 10.9900, lng: 77.0000, risk: 'low', location: 'Rural Area' }
    ],
    heat: [
        { lat: 11.0047, lng: 77.0153, risk: 'high', location: 'Sulur Town' },
        { lat: 11.0150, lng: 77.0250, risk: 'medium', location: 'Industrial Zone' }
    ],
    lightning: [
        { lat: 11.0047, lng: 77.0153, risk: 'medium', location: 'Sulur Town' },
        { lat: 10.9950, lng: 77.0100, risk: 'high', location: 'Open Fields' }
    ],
    visibility: [
        { lat: 11.0047, lng: 77.0153, risk: 'low', location: 'Sulur Town' },
        { lat: 11.0300, lng: 77.0400, risk: 'medium', location: 'Highway Area' }
    ]
};

// Risk level colors
const riskColors = {
    high: '#ff4444',
    medium: '#ffbb33',
    low: '#00C851'
};

// Risk level icons
function createRiskIcon(risk) {
    return L.divIcon({
        className: 'custom-marker',
        html: `<div style="
            background-color: ${riskColors[risk]};
            width: 20px;
            height: 20px;
            border-radius: 50%;
            border: 3px solid white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        "></div>`,
        iconSize: [20, 20],
        iconAnchor: [10, 10]
    });
}

// Add markers for a specific hazard type
function addHazardMarkers(hazardType) {
    const data = hazardData[hazardType];
    data.forEach(point => {
        const marker = L.marker([point.lat, point.lng], {
            icon: createRiskIcon(point.risk)
        });
        
        marker.bindPopup(`
            <strong>${hazardType.charAt(0).toUpperCase() + hazardType.slice(1)} Risk</strong><br>
            Location: ${point.location}<br>
            Risk Level: ${point.risk.toUpperCase()}
        `);
        
        layers[hazardType].addLayer(marker);
    });
}

// Remove markers for a specific hazard type
function removeHazardMarkers(hazardType) {
    layers[hazardType].clearLayers();
}

// Toggle layer visibility
function toggleLayer(hazardType) {
    const checkbox = document.getElementById(`${hazardType}-layer`);
    
    if (checkbox.checked) {
        addHazardMarkers(hazardType);
    } else {
        removeHazardMarkers(hazardType);
    }
}

// Add click event to get location info
map.on('click', function(e) {
    const lat = e.latlng.lat.toFixed(4);
    const lng = e.latlng.lng.toFixed(4);
    
    L.popup()
        .setLatLng(e.latlng)
        .setContent(`
            <strong>Location Details</strong><br>
            Latitude: ${lat}<br>
            Longitude: ${lng}<br>
            <em>Click on chat to ask about weather here</em>
        `)
        .openOn(map);
});

// Add scale control
L.control.scale().addTo(map);