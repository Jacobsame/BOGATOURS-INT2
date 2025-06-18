document.addEventListener("DOMContentLoaded", function () {
  const map = L.map("bogota-map", {
    minZoom: 11,
    maxBounds: [
      [4.45, -74.30],
      [4.85, -73.95],
    ]
  }).setView([4.611, -74.0721], 13);

  L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
    attribution: "&copy; OpenStreetMap & CartoDB"
  }).addTo(map);

  let controlRuta = null;

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

      const parada = data.paradas[0];
      const [paradaLng, paradaLat] = parada.coordenadas;
      const nombreParada = parada.nombre || "Parada cercana";

      if (controlRuta) map.removeControl(controlRuta);

      controlRuta = L.Routing.control({
        waypoints: [
          L.latLng(userLat, userLon),
          L.latLng(paradaLat, paradaLng),
          L.latLng(destinoLat, destinoLng)
        ],
        routeWhileDragging: false,
        createMarker: function (i, wp) {
          const iconConfig = {
            iconSize: [30, 30],
            iconAnchor: [15, 30],
          };

          const icons = ["/static/lugares/img/yo.png", "/static/lugares/img/transbordo.png", "/static/lugares/img/parada.png"];
          return L.marker(wp.latLng, {
            icon: L.icon({ iconUrl: icons[i], ...iconConfig })
          }).bindPopup(i === 0 ? "📍 Tú estás aquí" :
                       i === 1 ? `🚏 ${nombreParada}` :
                                 "🎯 Destino turístico");
        },
        show: false
      }).on("routesfound", (e) => {
        const r = e.routes[0];
        const t = Math.round(r.summary.totalTime / 60);
        const d = Math.round(r.summary.totalDistance);
        alert(`🧭 Ruta estimada:\n🕒 ${t} min\n📏 ${d} m`);
      }).addTo(map);

      map.setView([userLat, userLon], 14);
    });
  }

  // Mostrar todas las paradas iniciales
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

  cargarParadas(4.598, -74.074); // punto céntrico inicial

  // Función para mostrar detalles en tarjeta
  async function mostrarDetallesLugar(lugar) {
    const card = document.getElementById("detalles-lugar");
    card.style.display = "block";
    document.getElementById("detalle-nombre").innerText = lugar.nombre;
    document.getElementById("detalle-descripcion").innerText = lugar.descripcion;

    // Coordenadas y ruta
    if (lugar.latitud && lugar.longitud) {
      comoTransmiApp(lugar.latitud, lugar.longitud);
      map.setView([lugar.latitud, lugar.longitud], 15);
    }

    // Cargar reseñas
    const res = await fetch(`/api/resenas/${lugar.id}/`);
    const data = await res.json();
    const ul = document.getElementById("detalle-reseñas");
    ul.innerHTML = "";
    data.resenas.forEach(r => {
      const li = document.createElement("li");
      li.innerText = `⭐️${r.calificacion} - ${r.nombre_usuario}: ${r.comentario}`;
      ul.appendChild(li);
    });

    // Guardar ID actual para nueva reseña
    card.dataset.idLugar = lugar.id;
  }

  // Búsqueda por nombre
  window.buscarLugar = async function () {
    const q = document.getElementById("busqueda-input").value;
    if (!q) return alert("Escribe un lugar a buscar.");

    const res = await fetch(`/api/sitios/?q=${q}`);
    const data = await res.json();

    if (data.sitios.length === 0) {
      alert("❌ Lugar no encontrado.");
    } else {
      mostrarDetallesLugar(data.sitios[0]);
    }
  };

  // Botón "Más detalles"
  window.mostrarDetallesDesdeID = async function (id) {
    const res = await fetch(`/api/sitios/${id}/`);
    const lugar = await res.json();
    mostrarDetallesLugar(lugar);
  };

  // Enviar reseña
  window.enviarReseña = async function () {
    const card = document.getElementById("detalles-lugar");
    const id = card.dataset.idLugar;
    const nombre = document.getElementById("nombre_usuario").value;
    const comentario = document.getElementById("comentario").value;
    const calificacion = document.getElementById("calificacion").value;

    const res = await fetch(`/api/resenas/${id}/agregar/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken")
      },
      body: JSON.stringify({ nombre_usuario: nombre, comentario, calificacion })
    });

    if (res.ok) {
      alert("✅ Reseña enviada.");
      document.getElementById("comentario").value = "";
      mostrarDetallesDesdeID(id);
    } else {
      alert("❌ Error al enviar reseña.");
    }

    return false; // evitar recarga
  };

  // Obtener CSRF token para POST
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const c = cookies[i].trim();
        if (c.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(c.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
