html_1 = '''<!doctype html>
<html lang="en">
<head>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
          integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="
          crossorigin=""/>
    <style>
        body{background-color: #3d85c6;}
        #main {
            height: 84vh;
            width: 90vw;
            margin: 0;
            position: absolute;
            top: 50%;
            left: 50%;
            -ms-transform: translate(-50%, -50%);
            transform: translate(-50%, -50%);
        }
        .mapid{
            height: 79vh;
            width: 90vw;
        }
        #Pic{
            width: 100%;
        }
        #topbar{            
            margin-left: auto;
            margin-right: auto;
            left: 0;
            right: 0;
            text-align: center; 
            padding: 1px;
            color: white;           
        }
    </style>
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"
            integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA=="
            crossorigin=""></script>
    <title>Telegram bot</title>
</head>
<body>
    <div id = main>'''

html_2 = '''
    <div id="topbar"><b>%s</b>, click an object for the popup</div>
    <div id="mapid" class="mapid"></div>
    </div>    
<script>
    "use strict"
    var Source_point = %s;
    var Source_polygon = %s;
    var map = L.map('mapid', {
        center: [%f,%f],
        zoom: %d
    });'''

html_3 = '''
    var CartoDB_Positron = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; ' +
            '<a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 19
    }).addTo(map);
    var Esri_WorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/'+
    'MapServer/tile/{z}/{y}/{x}', {	attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX,'+
    'GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
    });
    var Points = L.geoJSON(Source_point,{
        pointToLayer: function (feature, latlng) {
            return L.marker(latlng, {icon: L.icon({
                    iconUrl: 'https://telegra.ph/file/bc24c001d928ca59c469d.png',
                    iconSize: [20, 20],
                    iconAnchor: [10, 10],
                    popupAnchor: [0, -10]
                })})
        },
        onEachFeature: function(feature, layer) {
            layer.bindPopup(`
            <p><b>Name:</b> ${feature.properties.user}
            <br>
            <b>Date/Time (non-local):</b> ${feature.properties.time}
            <br>
            <b>Question:</b> ${feature.properties.question}            
            <b>Latitude:</b> <i>${feature.geometry.coordinates[1].toFixed(4)}</i>,
            <b>Longitude:</b> <i>${feature.geometry.coordinates[0].toFixed(4)}</i>
            <br>
            <b>Video:</b> ${feature.properties.video}           
            <br>
            <b>Photo:</b> ${feature.properties.photo}
            </p>`);
        }
    }).addTo(map);

    var Polygons = L.geoJSON(Source_polygon,
        {style: {},
        onEachFeature: function(feature, layer) {
            layer.bindPopup(`
            <p><b>Name:</b> ${feature.properties.user}
            <br>
            <b>Date/Time (non-local):</b> ${feature.properties.time}
            <br>
            <b>Question:</b> ${feature.properties.question}
            <b>Video:</b> ${feature.properties.video}           
            <br>
            <b>Photo:</b> ${feature.properties.photo}
            </p>`);
        }    
    }).addTo(map);

    var baseMaps = {
        "Map": CartoDB_Positron,
        "Imagery": Esri_WorldImagery
    };
    var vectorL = {
        "Points": Points,
        "Polygons":Polygons
    };
    L.control.layers(baseMaps,vectorL).addTo(map);
    var count = 0
    var scbr = L.control.scale({imperial:false})
    map.addEventListener("zoomend",function (){
        if (map.getZoom() > 5 && count === 0){
            scbr.addTo(map);
            count ++;
        }
        else if (map.getZoom() <= 5) {
            scbr.remove();
            count = 0;
        }
    })
</script>
</body>
</html> '''''
