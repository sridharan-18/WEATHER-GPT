// Initialize the map with hyperlocal zooming capability
const map = L.map('map', {
    center: [11.0047, 77.0153], // Centered on Sulur, India
    zoom: 10,
    minZoom: 3,
    maxZoom: 19, // Enable hyperlocal zooming
    zoomControl: true
});

// Add OpenStreetMap tiles with multiple layers for better visualization
const osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
}).addTo(map);

// Add satellite layer option
const satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles © Esri',
    maxZoom: 19
});

// Layer control for base maps
const baseMaps = {
    'Street Map': osmLayer,
    'Satellite': satelliteLayer
};

// Layer groups for different hazard types
const layers = {
    flood: L.layerGroup(),
    heat: L.layerGroup(),
    lightning: L.layerGroup(),
    visibility: L.layerGroup()
};

// Add all layers to map (initially empty)
Object.values(layers).forEach(layer => layer.addTo(map));

// Overlay layers control
const overlayMaps = {
    'Flood Risk': layers.flood,
    'Heat Risk': layers.heat,
    'Lightning Risk': layers.lightning,
    'Visibility Risk': layers.visibility
};

// Add layer control to map
L.control.layers(baseMaps, overlayMaps, {
    position: 'topright',
    collapsed: false
}).addTo(map);

// Hazard risk data (simulated data for demonstration)
const hazardData = {
    flood: [
        { lat: 11.0047, lng: 77.0153, risk: 'high', location: 'Sulur Town', intensity: 85 },
        { lat: 11.0200, lng: 77.0300, risk: 'medium', location: 'Near Airport', intensity: 60 },
        { lat: 10.9900, lng: 77.0000, risk: 'low', location: 'Rural Area', intensity: 30 },
        { lat: 11.0100, lng: 77.0200, risk: 'high', location: 'River Bank', intensity: 90 },
        { lat: 10.9950, lng: 77.0150, risk: 'medium', location: 'Low-lying Area', intensity: 55 }
    ],
    heat: [
        { lat: 11.0047, lng: 77.0153, risk: 'high', location: 'Sulur Town', intensity: 88 },
        { lat: 11.0150, lng: 77.0250, risk: 'medium', location: 'Industrial Zone', intensity: 65 },
        { lat: 10.9950, lng: 77.0050, risk: 'high', location: 'Urban Center', intensity: 82 },
        { lat: 11.0250, lng: 77.0350, risk: 'low', location: 'Green Belt', intensity: 40 }
    ],
    lightning: [
        { lat: 11.0047, lng: 77.0153, risk: 'medium', location: 'Sulur Town', intensity: 50 },
        { lat: 10.9950, lng: 77.0100, risk: 'high', location: 'Open Fields', intensity: 75 },
        { lat: 11.0300, lng: 77.0400, risk: 'medium', location: 'Transmission Lines', intensity: 60 },
        { lat: 10.9850, lng: 77.0200, risk: 'high', location: 'High Ground', intensity: 80 }
    ],
    visibility: [
        { lat: 11.0047, lng: 77.0153, risk: 'low', location: 'Sulur Town', intensity: 20 },
        { lat: 11.0300, lng: 77.0400, risk: 'medium', location: 'Highway Area', intensity: 55 },
        { lat: 10.9800, lng: 77.0000, risk: 'high', location: 'Fog Zone', intensity: 85 },
        { lat: 11.0100, lng: 77.0500, risk: 'medium', location: 'Industrial Area', intensity: 60 }
    ]
};

// Risk level colors with opacity for better visualization
const riskColors = {
    high: '#ff4444',
    medium: '#ffbb33',
    low: '#00C851'
};

// Risk level opacity based on intensity
function getOpacity(intensity) {
    return 0.3 + (intensity / 100) * 0.5;
}

// Risk level radius based on intensity
function getRadius(intensity) {
    return 500 + (intensity / 100) * 1500; // 500m to 2000m radius
}

// Risk level circle markers for better hazard visualization
function createRiskCircle(lat, lng, risk, intensity) {
    return L.circle([lat, lng], {
        color: riskColors[risk],
        fillColor: riskColors[risk],
        fillOpacity: getOpacity(intensity),
        radius: getRadius(intensity),
        weight: 2
    });
}

// Risk level icons for precise location markers
function createRiskIcon(risk) {
    return L.divIcon({
        className: 'custom-marker',
        html: `<div style="
            background-color: ${riskColors[risk]};
            width: 24px;
            height: 24px;
            border-radius: 50%;
            border: 3px solid white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.4);
            animation: pulse 2s infinite;
        "></div>`,
        iconSize: [24, 24],
        iconAnchor: [12, 12]
    });
}

// Add markers and circles for a specific hazard type
function addHazardMarkers(hazardType) {
    const data = hazardData[hazardType];
    data.forEach(point => {
        // Add circle for area coverage
        const circle = createRiskCircle(point.lat, point.lng, point.risk, point.intensity);
        circle.bindPopup(`
            <strong>${hazardType.charAt(0).toUpperCase() + hazardType.slice(1)} Risk Area</strong><br>
            Location: ${point.location}<br>
            Risk Level: ${point.risk.toUpperCase()}<br>
            Intensity: ${point.intensity}%<br>
            Coverage Radius: ${(getRadius(point.intensity) / 1000).toFixed(1)} km
        `);
        layers[hazardType].addLayer(circle);
        
        // Add marker for precise location
        const marker = L.marker([point.lat, point.lng], {
            icon: createRiskIcon(point.risk)
        });
        
        marker.bindPopup(`
            <strong>${hazardType.charAt(0).toUpperCase() + hazardType.slice(1)} Risk Point</strong><br>
            Location: ${point.location}<br>
            Risk Level: ${point.risk.toUpperCase()}<br>
            Intensity: ${point.intensity}%<br>
            Coordinates: ${point.lat.toFixed(4)}, ${point.lng.toFixed(4)}
        `);
        
        layers[hazardType].addLayer(marker);
    });
}

// Remove markers for a specific hazard type
function removeHazardMarkers(hazardType) {
    layers[hazardType].clearLayers();
}

// Toggle layer visibility with improved feedback
function toggleLayer(hazardType) {
    const checkbox = document.getElementById(`${hazardType}-layer`);
    
    if (checkbox.checked) {
        addHazardMarkers(hazardType);
        // Sync with Leaflet layer control
        if (map.hasLayer(layers[hazardType])) {
            layers[hazardType].addTo(map);
        }
    } else {
        removeHazardMarkers(hazardType);
        map.removeLayer(layers[hazardType]);
    }
}

// Sync checkbox state with layer control
map.on('overlayadd', function(e) {
    const layerName = e.name.toLowerCase().replace(' risk', '');
    const checkbox = document.getElementById(`${layerName}-layer`);
    if (checkbox && !checkbox.checked) {
        checkbox.checked = true;
        addHazardMarkers(layerName);
    }
});

map.on('overlayremove', function(e) {
    const layerName = e.name.toLowerCase().replace(' risk', '');
    const checkbox = document.getElementById(`${layerName}-layer`);
    if (checkbox && checkbox.checked) {
        checkbox.checked = false;
        removeHazardMarkers(layerName);
    }
});

// Add click event to get location info and weather
map.on('click', function(e) {
    const lat = e.latlng.lat.toFixed(4);
    const lng = e.latlng.lng.toFixed(4);
    
    L.popup()
        .setLatLng(e.latlng)
        .setContent(`
            <strong>Location Details</strong><br>
            Latitude: ${lat}<br>
            Longitude: ${lng}<br>
            <em>Ask in chat: "What's the weather at ${lat}, ${lng}?"</em>
        `)
        .openOn(map);
});

// Add scale control with imperial and metric
L.control.scale({
    position: 'bottomleft',
    imperial: true,
    metric: true
}).addTo(map);

// Add zoom control with better positioning
map.zoomControl.remove();
L.control.zoom({
    position: 'bottomright'
}).addTo(map);

// Add fullscreen control for better map viewing
L.Control.Fullscreen = L.Control.extend({
    onAdd: function(map) {
        const button = L.DomUtil.create('button', 'leaflet-control-fullscreen');
        button.innerHTML = '⛶';
        button.title = 'Toggle Fullscreen';
        button.style.cssText = 'width: 30px; height: 30px; font-size: 18px; cursor: pointer;';
        
        L.DomEvent.on(button, 'click', function() {
            if (!document.fullscreenElement) {
                document.getElementById('map').requestFullscreen();
            } else {
                document.exitFullscreen();
            }
        });
        
        return button;
    }
});

L.control.fullscreen = function(opts) {
    return new L.Control.Fullscreen(opts);
};

L.control.fullscreen({ position: 'topleft' }).addTo(map);

// Add current location button
L.Control.CurrentLocation = L.Control.extend({
    onAdd: function(map) {
        const button = L.DomUtil.create('button', 'leaflet-control-location');
        button.innerHTML = '📍';
        button.title = 'Show My Location';
        button.style.cssText = 'width: 30px; height: 30px; font-size: 18px; cursor: pointer;';
        
        L.DomEvent.on(button, 'click', function() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    const lat = position.coords.latitude;
                    const lng = position.coords.longitude;
                    map.setView([lat, lng], 15);
                    L.marker([lat, lng]).addTo(map)
                        .bindPopup('Your Location').openPopup();
                }, function() {
                    alert('Unable to get your location');
                });
            } else {
                alert('Geolocation is not supported by your browser');
            }
        });
        
        return button;
    }
});

L.control.currentLocation = function(opts) {
    return new L.Control.CurrentLocation(opts);
};

L.control.currentLocation({ position: 'topleft' }).addTo(map);

// Add CSS animation for pulse effect
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.2); opacity: 0.7; }
        100% { transform: scale(1); opacity: 1; }
    }
`;
document.head.appendChild(style);

// Initialize map with better responsive behavior
function invalidateMapSize() {
    setTimeout(function() {
        map.invalidateSize();
    }, 100);
}

// Invalidate map size on window resize
window.addEventListener('resize', invalidateMapSize);

// Initial map size invalidation
invalidateMapSize();