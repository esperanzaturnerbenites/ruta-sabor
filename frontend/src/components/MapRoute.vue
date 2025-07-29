<template>
  <div id="map" style="height: 400px; width: 100%"></div>
</template>

<script setup>
import { onMounted } from 'vue'
import * as L from 'leaflet'
import OpenRouteService from 'openrouteservice-js'

// Props
const props = defineProps({
  places: {
    type: Array,
    required: true,
  },
  userCoords: {
    type: Object,
    required: true,
  },
})

// API key de OpenRouteService (cambia por la tuya)
const apiKey = import.meta.env.VITE_MAP_KEY_OPEN_ROUTE_SERVICE

// Función para trazar la ruta
function drawRoute(map, coordsArray) {
  if (!apiKey) {
    console.error('❌ No se ha configurado la API Key de OpenRouteService')
    return
  }

  const ors = new OpenRouteService.Directions({ api_key: apiKey })

  ors
    .calculate({
      coordinates: coordsArray,
      profile: 'foot-walking', // o 'driving-car'
      format: 'geojson',
    })
    .then((geojson) => {
      L.geoJSON(geojson, {
        style: {
          color: 'blue',
          weight: 4,
        },
      }).addTo(map)
    })
    .catch((err) => {
      console.error('❌ Error al calcular la ruta:', err)
    })
}

// Mostrar mapa
onMounted(async () => {
  if (!props.userCoords.latitude || !props.userCoords.longitude) {
    alert('No se pudo obtener tu ubicación actual')
    return
  }

  const map = L.map('map').setView([props.userCoords.latitude, props.userCoords.longitude], 14)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap',
  }).addTo(map)

  // Coordenadas de origen (usuario) + lugares
  const routeCoords = [[props.userCoords.longitude, props.userCoords.latitude]]

  // Marcador de ubicación actual
  L.marker([props.userCoords.latitude, props.userCoords.longitude])
    .addTo(map)
    .bindPopup('Tu ubicación actual')
    .openPopup()

  // Agregar marcadores de lugares
  props.places.forEach((place) => {
    const { lat, lng } = place.geolocation

    L.marker([lat, lng])
      .addTo(map)
      .bindPopup(`<strong>${place.place_name}</strong><br>${place.address}<br><a href="https://maps.google.com/?q=${lat},${lng}" target="_blank">Ver en Google Maps</a>`)

    routeCoords.push([lng, lat])
  })

  // Dibujar ruta real
  if (routeCoords.length > 1) {
    drawRoute(map, routeCoords)
  }
})
</script>