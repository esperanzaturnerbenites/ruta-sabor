<template>
  <div id="map" style="height: 500px; width: 100%"></div>
</template>

<script setup>
import { onMounted } from 'vue'
import L from 'leaflet'

const props = defineProps({
  places: Array
})

onMounted(() => {
  navigator.geolocation.getCurrentPosition(position => {
    const userCoords = [position.coords.latitude, position.coords.longitude]

    const map = L.map('map').setView(userCoords, 14)

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map)

    // Añadir marcador del usuario
    L.marker(userCoords).addTo(map).bindPopup("📍 Tú estás aquí").openPopup()

    // Lista de puntos: primero el usuario, luego los lugares
    const routePoints = [userCoords]

    props.places.forEach(place => {
      const coords = [place.geolocation.lat, place.geolocation.lng]
      routePoints.push(coords)

      L.marker(coords).addTo(map)
        .bindPopup(`<b>${place.place_name}</b><br>${place.address}`)
    })

    // Dibujar la línea de ruta
    L.polyline(routePoints, { color: 'blue' }).addTo(map)
  })
})
</script>