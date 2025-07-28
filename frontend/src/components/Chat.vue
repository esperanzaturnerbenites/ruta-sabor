<template>
  <div class="chat-box box p-0">
    <div class="chat-messages px-4 py-3">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['message-bubble', msg.from === 'user' ? 'is-user' : 'is-app']"
      >
        <p v-if="msg.type === 'text'" class="message-text">{{ msg.text }}</p>

        <div v-if="msg.type === 'filters'">
          <p class="message-text mb-4">{{ msg.text }}</p>

          <div class="buttons are-small is-flex-wrap-wrap is-justify-content-center">
            <button
              class="button is-primary is-light"
              :class="{ 'is-active has-text-weight-semibold': isSelectedFilter('lunch') }"
              @click="selectFilter('lunch')"
            >
              <span v-if="isSelectedFilter('lunch')" class="mr-2">✓</span>
              🍛 Comidas
            </button>
            <button
              class="button is-link is-light"
              :class="{ 'is-active has-text-weight-semibold': isSelectedFilter('sweets') }"
              @click="selectFilter('sweets')"
            >
              <span v-if="isSelectedFilter('sweets')" class="mr-2">✓</span>
              🍰 Dulces / Postres
            </button>
            <button
              class="button is-info is-light"
              :class="{ 'is-active has-text-weight-semibold': isSelectedFilter('drinks') }"
              @click="selectFilter('drinks')"
            >
              <span v-if="isSelectedFilter('drinks')" class="mr-2">✓</span>
              🍹 Bebidas
            </button>
          </div>
        </div>

        <div v-if="msg.type === 'place'">
          <div class="card-content">
            <p class="title is-5">{{ msg.place.place_name }}</p>
            <!--
            <p class="subtitle is-6">👤 {{ msg.place.owner_name }}</p>
            -->

            <p class="mb-2"><strong>📍 Dirección:</strong> {{ msg.place.address }}</p>
            <p v-if="msg.place.neighborhood && msg.place.neighborhood !== 'None'" class="mb-2">
              <strong>🏘️ Barrio:</strong> {{ msg.place.neighborhood }}
            </p>

            <a
              class="button is-small is-success mr-2"
              :href="getWhatsappWebLink(msg.place)"
              target="_blank"
              rel="noopener"
            >
              📞 Contactar
            </a>

            <!--
            <p class="mb-2"><strong>📧 Email:</strong> {{ msg.place.email }}</p>

            <p class="mb-3"><strong>🔎 Actividad:</strong> {{ msg.place.activity }}</p>
            -->

            <a
              class="button is-small is-info"
              :href="getGoogleMapsLink(msg.place)"
              target="_blank"
              rel="noopener"
            >
              📌 Ver en Google Maps
            </a>
          </div>
        </div>

        <div v-if="msg.type === 'button'">
          <button
            class="button is-primary is-light"
            @click="msg.action === 'renderMapRoute' ? renderMapRoute() : null"
          >
            <span>✓ {{ msg.text }}</span>
          </button>
        </div>

        <div v-if="msg.type === 'map'">
          <div v-if="showMapRoute && places.length > 0 && coords.latitude !== null && coords.longitude !== null" style="height: 400px; width: 600px;">
            <MapRoute :places="places" :userCoords="coords"></MapRoute>
          </div>
          <div v-else>
            <p>No hay lugares para mostrar en el mapa.</p>
          </div>
        </div>
      </div>
    </div>

    <form class="chat-input px-4 py-3" @submit.prevent="sendMessage">
      <div class="field has-addons">
        <div class="control is-expanded">
          <input
            v-model="newMessage"
            class="input"
            type="text"
            placeholder="Escribe un mensaje..."
            :disabled="isLoading"
          />
        </div>
        <div class="control">
          <button class="button is-primary" :disabled="isLoading || !newMessage || newMessage.trim() === ''">
            Enviar
          </button>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'

import MapRoute from '@/components/MapRoute.vue'

const props = defineProps({
  isLoading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['message', 'selectFilter'])

const showMapRoute = ref(false)
const places = ref([])
const coords = ref([])
const typeFood = ref(null)
const newMessage = ref(null)
const messages = ref([
  { from: 'app', type: 'text', action: null, text: 'Hola 👋 ¿En qué te puedo ayudar hoy?' }
])

const pushMessage = (text, from = 'app') => {
  messages.value.push({ from, type: 'text', action: null, text })
}

const pushFilters = () => {
  messages.value.push({ from: 'app', type: 'filters', action: null, text: '¿Qué tipo de comida te gustaría explorar? 🍽️' })
}

const pushPlaces = (newPlaces) => {
  places.value = newPlaces

  for (const place of places.value) {
    messages.value.push({
      from: 'app',
      text: `🗺️ ${place.place_name} ubicado en ${place.address}. Contacto: ${place.phone}`,
      type: 'place',
      action: null,
      place
    })
  }

  messages.value.push({
    from: 'app',
    type: 'button',
    action: 'renderMapRoute',
    text: 'Quiero ver la ruta en el mapa 🗺️',
  })
}

const setCoords = (newCoords) => {
  coords.value = newCoords
}

const removeMessagesByType = (type) => {
  messages.value = messages.value.filter(msg => msg.type !== type)
}

const sendMessage = () => {
  if (!newMessage.value.trim()) return

  messages.value.push({ from: 'user', type: 'text', text: newMessage.value })

  emit('message', newMessage.value )

  newMessage.value = null
}

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms))

function renderMapRoute() {
  removeMessagesByType('map')

  showMapRoute.value = true

  messages.value.push({ from: 'user', type: 'text', action: null, text: 'Quiero ver la ruta en el mapa 🗺️' })

  delay(500)

  messages.value.push({ from: 'app', type: 'map', action: null, text: 'Ruta del sabor' })
}

function isSelectedFilter(value) {
  return typeFood.value === value
}

function selectFilter(value) {
  typeFood.value = value

  if (value === 'lunch') {
    pushMessage('Comidas 🍛', 'user')
  } else if (value === 'sweets') {
    pushMessage('Dulces 🍰', 'user')
  } else if (value === 'drinks') {
    pushMessage('Bebidas 🍹', 'user')
  }

  emit('selectFilter', value, 'food')
}

function getWhatsappWebLink(place) {
  return `https://api.whatsapp.com/send?phone=57${place.phone}&text=Hola, que platos venden?`
}

function getGoogleMapsLink(place) {
  return `https://www.google.com/maps?q=${place.geolocation.lat},${place.geolocation.lng}`;
}

defineExpose({ pushMessage, pushFilters, pushPlaces, setCoords })
</script>

<style scoped>
.chat-box {
  display: flex;
  flex-direction: column;
  height: 500px;
  max-height: 100%;
  border-radius: 12px;
  overflow: hidden;
  background: #fefefe;
}

.chat-messages {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow-y: auto;
  background: #f9f9f9;
  padding-bottom: 1rem;
}

.message-bubble {
  display: inline-block;
  align-self: flex-start;
  max-width: 75%;
  margin-bottom: 0.75rem;
  padding: 0.6rem 1rem;
  border-radius: 16px;
  line-height: 1.3;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.is-user {
  background-color: #d1ffd6;
  align-self: flex-end;
  border-bottom-right-radius: 4px;
}

.is-app {
  background-color: #e0e0e0;
  align-self: flex-start;
  border-bottom-left-radius: 4px;
}

.chat-input {
  border-top: 1px solid #dbdbdb;
  background: white;
}
</style>