// Crear el mapa centrado en Bogotá
const map = L.map("bogota-map").setView([4.711, -74.0721], 13);

// Capa base de OpenStreetMap
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "© OpenStreetMap contributors"
}).addTo(map);

// Control de ruta
let controlRuta = null;

// Función para mostrar la ruta desde la ubicación actual
function mostrarRutaDesdeUbicacion(destinoLat, destinoLng) {
  if (!navigator.geolocation) {
    alert("Tu navegador no soporta geolocalización.");
    return;
  }

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const origen = [position.coords.latitude, position.coords.longitude];
      const destino = [destinoLat, destinoLng];

      if (controlRuta) {
        map.removeControl(controlRuta);
      }

      controlRuta = L.Routing.control({
        waypoints: [
          L.latLng(origen[0], origen[1]),
          L.latLng(destino[0], destino[1])
        ],
        routeWhileDragging: false,
        show: false,
        createMarker: () => null
      }).addTo(map);

      map.setView(origen, 14);
    },
    (error) => {
      console.error("Error de geolocalización:", error);
      alert("No se pudo obtener tu ubicación.");
    }
  );
}

// Lista de sitios turísticos
const zonasTuristicas = [
  { nombre: "La Candelaria", coords: [4.595, -74.074], descripcion: "Centro histórico y cultural." },
  { nombre: "Monserrate", coords: [4.605, -74.055], descripcion: "Mirador icónico de Bogotá." },
  { nombre: "Museo del Oro", coords: [4.601, -74.072], descripcion: "Museo con artefactos precolombinos." },
  { nombre: "Parque Simón Bolívar", coords: [4.658, -74.093], descripcion: "Gran parque urbano." },
  { nombre: "Zona T", coords: [4.669, -74.052], descripcion: "Zona moderna y de vida nocturna." },
  { nombre: "Museo Botero", coords: [4.598, -74.071], descripcion: "Obras de Botero y otros artistas." },
  { nombre: "Plaza de Bolívar", coords: [4.598, -74.074], descripcion: "Plaza histórica con edificios coloniales." }
];

// Mostrar sitios turísticos en el mapa
zonasTuristicas.forEach(zona => {
  const [lat, lng] = zona.coords;

  L.marker([lat, lng])
    .addTo(map)
    .bindPopup(`
      <strong>${zona.nombre}</strong><br>
      ${zona.descripcion}<br><br>
      <button onclick="mostrarRutaDesdeUbicacion(${lat}, ${lng})">
        Cómo llegar desde mi ubicación
      </button>
    `);
});

// Cargar paradas desde la API de Django (que consulta Transitland)
async function cargarParadas(lat, lon) {
  console.log("🛰️ Consultando paradas...");
  const response = await fetch(`/api/paradas-cercanas/?lat=${lat}&lon=${lon}&radius=1500`);
  const data = await response.json();
  console.log("📦 Paradas recibidas:", data);

  data.paradas.forEach(parada => {
    const [lng, lat] = parada.coordenadas;
    const nombre = parada.nombre || "Parada sin nombre";

    L.circleMarker([lat, lng], {
      radius: 5,
      color: "#ff0000",
      fillColor: "#ff6666",
      fillOpacity: 0.9
    }).addTo(map)
      .bindPopup(`<b>${nombre}</b><br>ID: ${parada.id}`);
  });
}

// Cargar paradas cercanas al centro histórico de Bogotá
cargarParadas(4.598, -74.074);
