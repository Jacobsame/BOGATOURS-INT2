// Crear el mapa centrado en Bogotá
const map = L.map("map").setView([4.65, -74.1], 12);

// Capa base de OpenStreetMap
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "© OpenStreetMap contributors"
}).addTo(map);

// Coordenadas garantizadas: Portal Norte
const centro = { lat: 4.765251, lon: -74.031243 };

// Obtener paradas de la API Django
async function cargarParadas(lat, lon) {
  const response = await fetch(`/api/paradas-cercanas/?lat=${lat}&lon=${lon}&radius=2000`);
  const data = await response.json();

  data.paradas.forEach(parada => {
    const [lng, lat] = parada.coordenadas;
    const nombre = parada.nombre || "Parada sin nombre";
    L.marker([lat, lng])
      .addTo(map)
      .bindPopup(`<b>${nombre}</b><br>${parada.id}`);
  });
}

// Llamar la función para cargar paradas
cargarParadas(centro.lat, centro.lon);


console.log("🛰️ Consultando paradas...");

async function cargarParadas(lat, lon) {
  const response = await fetch(`/api/paradas-cercanas/?lat=${lat}&lon=${lon}&radius=2000`);
  const data = await response.json();

  console.log("📦 Paradas recibidas:", data);

  data.paradas.forEach(parada => {
    const [lng, lat] = parada.coordenadas;
    const nombre = parada.nombre || "Parada sin nombre";
    L.marker([lat, lng])
      .addTo(map)
      .bindPopup(`<b>${nombre}</b><br>${parada.id}`);
  });
}
