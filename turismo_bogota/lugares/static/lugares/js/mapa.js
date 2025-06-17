const map = L.map("bogota-map").setView([4.711, -74.0721], 13);

// Estilo de mapa oscuro como TransmiApp
L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
  attribution: "&copy; OpenStreetMap & CartoDB",
}).addTo(map);

let controlRuta = null;

// Función que simula la lógica de TransmiApp
function comoTransmiApp(destinoLat, destinoLng) {
  if (!navigator.geolocation) {
    alert("Tu navegador no soporta geolocalización.");
    return;
  }

  navigator.geolocation.getCurrentPosition(async (position) => {
    const userLat = position.coords.latitude;
    const userLon = position.coords.longitude;

    const response = await fetch(`/api/paradas-cercanas/?lat=${userLat}&lon=${userLon}&radius=1500`);
    const data = await response.json();

    if (!data.paradas.length) {
      alert("No se encontraron paradas cercanas.");
      return;
    }

    const parada = data.paradas[0]; // Más cercana
    const [paradaLng, paradaLat] = parada.coordenadas;
    const nombreParada = parada.nombre || "Parada cercana";

    if (controlRuta) {
      map.removeControl(controlRuta);
    }

    controlRuta = L.Routing.control({
      waypoints: [
        L.latLng(userLat, userLon),
        L.latLng(paradaLat, paradaLng),
        L.latLng(destinoLat, destinoLng)
      ],
      routeWhileDragging: false,
      createMarker: function (i, wp) {
        if (i === 0) {
          return L.marker(wp.latLng, {
            icon: L.icon({
              iconUrl: "/static/lugares/img/yo.png",
              iconSize: [32, 32],
              iconAnchor: [16, 32],
            }),
          }).bindPopup("📍 Estás aquí");
        } else if (i === 1) {
          return L.marker(wp.latLng, {
            icon: L.icon({
              iconUrl: "/static/lugares/img/transbordo.png",
              iconSize: [32, 32],
              iconAnchor: [16, 32],
            }),
          }).bindPopup(`🚏 Transbordo en: ${nombreParada}`);
        } else {
          return L.marker(wp.latLng, {
            icon: L.icon({
              iconUrl: "/static/lugares/img/parada.png",
              iconSize: [30, 30],
              iconAnchor: [15, 30],
            }),
          }).bindPopup("🎯 Destino turístico");
        }
      },
      show: false,
    }).on("routesfound", (e) => {
      const ruta = e.routes[0];
      const tiempo = Math.round(ruta.summary.totalTime / 60);
      const distancia = Math.round(ruta.summary.totalDistance);
      alert(`🧭 Ruta estimada:\n🕒 ${tiempo} min\n📏 ${distancia} m`);
    }).addTo(map);

    map.setView([userLat, userLon], 14);
  },
  (error) => {
    console.error("Error geolocalización:", error);
    alert("No se pudo obtener tu ubicación.");
  });
}

// Lista de destinos turísticos
const zonasTuristicas = [
  { nombre: "La Candelaria", coords: [4.595, -74.074], descripcion: "Centro histórico y cultural." },
  { nombre: "Monserrate", coords: [4.605, -74.055], descripcion: "Mirador icónico de Bogotá." },
  { nombre: "Museo del Oro", coords: [4.601, -74.072], descripcion: "Museo con artefactos precolombinos." },
  { nombre: "Parque Simón Bolívar", coords: [4.658, -74.093], descripcion: "Gran parque urbano." },
  { nombre: "Zona T", coords: [4.669, -74.052], descripcion: "Zona moderna y de vida nocturna." },
  { nombre: "Museo Botero", coords: [4.598, -74.071], descripcion: "Obras de Botero y otros artistas." },
  { nombre: "Plaza de Bolívar", coords: [4.598, -74.074], descripcion: "Plaza histórica con edificios coloniales." }
];

// Mostrar los destinos turísticos en el mapa
zonasTuristicas.forEach(zona => {
  const [lat, lng] = zona.coords;
  L.marker([lat, lng])
    .addTo(map)
    .bindPopup(`
      <strong>${zona.nombre}</strong><br>
      ${zona.descripcion}<br><br>
      <button onclick="comoTransmiApp(${lat}, ${lng})">
        🚶 Cómo llegar desde mi ubicación
      </button>
    `);
});

// Mostrar paradas en el mapa
async function cargarParadas(lat, lon) {
  const response = await fetch(`/api/paradas-cercanas/?lat=${lat}&lon=${lon}&radius=1500`);
  const data = await response.json();

  data.paradas.forEach(parada => {
    const [lng, lat] = parada.coordenadas;
    const nombre = parada.nombre || "Parada sin nombre";

    L.circleMarker([lat, lng], {
      radius: 6,
      color: "#ffa500",
      fillColor: "#ffcc00",
      fillOpacity: 0.8
    }).addTo(map)
      .bindPopup(`🚌 ${nombre}`);
  });
}

// Paradas iniciales (opcional)
cargarParadas(4.598, -74.074);