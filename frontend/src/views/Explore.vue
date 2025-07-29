<template>
  <section class="section">
    <div class="container">
      <!--
      <div class="control has-text-right is-7 mb-5">
        <label class="radio">
          <input
            type="radio"
            value="filters"
            v-model="searchMode"
          />
          🔍 Usar filtros
        </label>
        <label class="radio ml-4">
          <input
            type="radio"
            value="chat"
            v-model="searchMode"
          />
          💬 Buscar por chat
        </label>
      </div>
      -->

      <div class="has-text-centered">
        <h1 class="title is-4 has-text-info m-0">
          ¡Descubre tu próxima parada deliciosa!
        </h1>
        <h1 class="title is-3 has-text-primary">
          En la Ruta del Sabor Girardoteño 🍔🍧
        </h1>

        <p class="subtitle is-6 mb-5">
          Elige lo que tienes ganas de comer y te diremos a dónde ir hoy en Girardot 🌞
        </p>

        <div>
          <p v-if="coords.latitude && coords.longitude">
            <!--
            Estás en: lat {{ coords.latitude.toFixed(5) }}, long {{ coords.longitude.toFixed(5) }}
            -->
          </p>
          <p v-else-if="error"></p>
          <p v-else>Cargando tu ubicación...</p>
        </div>

        <div class="has-text-centered mt-6">
          <p
            v-if="error"
            class="has-text-danger is-size-6 has-text-weight-semibold"
          >
            ⚠️ {{ error }}
          </p>
        </div>

        <div v-if="searchMode === 'chat'" class="mt-6">
          <Chat :isLoading="isLoading" @message="handleChatMessage" @selectFilter="recommendByFilter" ref="chatRef" />
        </div>
        <div v-else-if="searchMode === 'filters' && places.length === 0" class="mt-6">
          <!-- Tipo de comida -->
          <div class="field mt-6">
            <label class="label">¿Qué se te antoja?</label>
            <div class="buttons are-medium is-flex-wrap-wrap is-justify-content-center">
              <button
                class="button is-primary is-light"
                :class="{ 'is-active has-text-weight-semibold': isSelectedValue('lunch', 'food') }"
                @click="selectValue('lunch', 'food')"
              >
                <span v-if="isSelectedValue('lunch', 'food')" class="mr-2">✓</span>
                🍛 Comida rápida / tradicional
              </button>
              <button
                class="button is-link is-light"
                :class="{ 'is-active has-text-weight-semibold': isSelectedValue('sweets', 'food') }"
                @click="selectValue('sweets', 'food')"
              >
                <span v-if="isSelectedValue('sweets', 'food')" class="mr-2">✓</span>
                🍰 Dulces / Postres
              </button>
              <button
                class="button is-info is-light"
                :class="{ 'is-active has-text-weight-semibold': isSelectedValue('drinks', 'food') }"
                @click="selectValue('drinks', 'food')"
              >
                <span v-if="isSelectedValue('drinks', 'food')" class="mr-2">✓</span>
                🍹 Bebidas
              </button>
            </div>
          </div>

          <!-- Tiempo disponible -->
          <div class="field mt-6">
            <label class="label">¿Cuánto tiempo tienes?</label>
            <div class="buttons are-medium is-flex-wrap-wrap is-justify-content-center">
              <button
                class="button is-primary is-light"
                :class="{ 'is-active has-text-weight-semibold': isSelectedValue('few_minutes', 'time_available') }"
                @click="selectValue('few_minutes', 'time_available')"
              >
                <span v-if="isSelectedValue('few_minutes', 'time_available')" class="mr-2">✓</span>
                🕒 Pocos minutos
              </button>
              <button
                class="button is-link is-light"
                :class="{ 'is-active has-text-weight-semibold': isSelectedValue('free_time', 'time_available') }"
                @click="selectValue('free_time', 'time_available')"
              >
                <span v-if="isSelectedValue('free_time', 'time_available')" class="mr-2">✓</span>
                🍰 Tiempo libre
              </button>
              <button
                class="button is-info is-light"
                :class="{ 'is-active has-text-weight-semibold': isSelectedValue('leisurely_stroll', 'time_available') }"
                @click="selectValue('leisurely_stroll', 'time_available')"
              >
                <span v-if="isSelectedValue('leisurely_stroll', 'time_available')" class="mr-2">✓</span>
                🚶 Estoy de paseo sin afán
              </button>
            </div>
          </div>

          <!-- Presupuesto -->
          <div class="field mt-6">
            <label class="label">¿Cuál es tu presupuesto?</label>
            <div class="buttons are-medium is-flex-wrap-wrap is-justify-content-center">
              <button
                class="button is-primary is-light"
                :class="{ 'is-active has-text-weight-semibold': isSelectedValue('cheap', 'budget') }"
                @click="selectValue('cheap', 'budget')"
              >
                <span v-if="isSelectedValue('cheap', 'budget')" class="mr-2">✓</span>
                🪙 Muy económico
              </button>
              <button
                class="button is-link is-light"
                :class="{ 'is-active has-text-weight-semibold': isSelectedValue('moderate', 'budget') }"
                @click="selectValue('moderate', 'budget')"
              >
                <span v-if="isSelectedValue('moderate', 'budget')" class="mr-2">✓</span>
                💵 Moderado
              </button>
              <button
                class="button is-info is-light"
                :class="{ 'is-active has-text-weight-semibold': isSelectedValue('luxury', 'budget') }"
                @click="selectValue('luxury', 'budget')"
              >
                <span v-if="isSelectedValue('luxury', 'budget')" class="mr-2">✓</span>
                💎 Quiero darme un gusto
              </button>
            </div>
          </div>

          <!-- Filtros rápidos -->
          <div class="field mt-6">
            <label class="label">Filtros rápidos</label>
            <div class="buttons are-medium is-flex-wrap-wrap is-justify-content-center">
              <button
                class="button is-primary is-light"
                :class="{ 'is-active has-text-weight-semibold': isSelectedValue('cheap', 'quick') }"
                @click="selectValue('cheap', 'quick')"
              >
                <span v-if="isSelectedValue('cheap', 'quick')" class="mr-2">✓</span>
                🪙 Algo barato
              </button>
              <button
                class="button is-link is-light"
                :class="{ 'is-active has-text-weight-semibold': isSelectedValue('lunch', 'quick') }"
                @click="selectValue('lunch', 'quick')"
              >
                🍛 Almuerzo rico
              </button>
              <button
                class="button is-info is-light"
                :class="{ 'is-active has-text-weight-semibold': isSelectedValue('nearby', 'quick') }"
                @click="selectValue('nearby', 'quick')"
              >
                <span v-if="isSelectedValue('nearby', 'quick')" class="mr-2">✓</span>
                📍 Cerca de mí
              </button>
              <button
                class="button is-success is-light"
                :class="{ 'is-active has-text-weight-semibold': isSelectedValue('breakfast', 'quick') }"
                @click="selectValue('breakfast', 'quick')"
              >
                <span v-if="isSelectedValue('breakfast', 'quick')" class="mr-2">✓</span>
                🥐 Desayuno delicioso
              </button>
              <button
                class="button is-warning is-light"
                :class="{ 'is-active has-text-weight-semibold': isSelectedValue('snacks', 'quick') }"
                @click="selectValue('snacks', 'quick')"
              >
                <span v-if="isSelectedValue('snacks', 'quick')" class="mr-2">✓</span>
                🍕 Antojitos rápidos
              </button>
            </div>
          </div>

          <div class="mt-6">
            <button class="button is-primary is-medium is-rounded is-fullwidth" @click="recommend">
              ¡Buscar lugares!
            </button>
          </div>

          <div v-if="isLoading" class="mt-6">
            <p>
              <span>Estoy buscando los mejores lugares para tí...</span>
            </p>
          </div>
        </div>
      </div>

      <div v-if="searchMode === 'filters' && places.length > 0">
        <button
          class="button is-primary is-light"
          @click="clearPlaces"
        >
          ⭠ Hacer otra búsqueda
        </button>

        <div v-if="showMapRoute" class="mt-6">
          <MapRoute :places="places" :userCoords="coords"></MapRoute>
        </div>

        <div v-for="(place, idx) in places" :key="idx" class="card my-5">
          <div class="card-content">
            <p class="title is-5">{{ place.place_name }}</p>
            <!--
            <p class="subtitle is-6">👤 {{ place.owner_name }}</p>
            -->

            <p class="mb-2"><strong>📍 Dirección:</strong> {{ place.address }}</p>
            <p v-if="place.neighborhood && place.neighborhood !== 'None'" class="mb-2">
              <strong>🏘️ Barrio:</strong> {{ place.neighborhood }}
            </p>

            <a
              class="button is-small is-success mr-2"
              :href="getWhatsappWebLink(place)"
              target="_blank"
              rel="noopener"
            >
              📞 Contactar
            </a>

            <!--
            <p class="mb-2"><strong>📧 Email:</strong> {{ place.email }}</p>

            <p class="mb-3"><strong>🔎 Actividad:</strong> {{ place.activity }}</p>
            -->

            <a
              class="button is-small is-info"
              :href="getGoogleMapsLink(place)"
              target="_blank"
              rel="noopener"
            >
              📌 Ver en Google Maps
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/services/apiClient'
import Chat from '@/components/Chat.vue'
import MapRoute from '@/components/MapRoute.vue'

const searchMode = ref('chat') // 'filters' or 'chat'
const error = ref(null)
const isLoading = ref(false)
const showMapRoute = ref(false)
const chatRef = ref(null)

const places = ref([])
const coords = ref({
  latitude: null,
  longitude: null
})

const message = ref(null)
const typeFood = ref(null)
const timeAvailable = ref(null)
const budget = ref(null)
const quickFilter = ref(null)

const foodTypeMap = {
  lunch: "lunch,meal,comida,almuerzo,desayuno",
  sweets: "dessert,cake,dulces,postres",
  drinks: "drinks,bebidas,jugos,refrescos,bar",
};

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms))

const handleChatMessage = async (text) => {
  message.value = text

  if (chatRef.value) {
    await delay(500)
    chatRef.value.pushMessage("Buscando lugares ...")
  }

  recommend()
}

const recommend = async () => {
  if (searchMode.value === 'filters' && !typeFood.value) {
    error.value = 'Por favor selecciona qué se te antoja para darte una buena recomendación 🍽️'
    return
  }

  isLoading.value = true

  try {
    const response = await apiClient.get('/places/recommendations', {
      params: {
        search_mode: searchMode.value,
        message: message.value,
        type_food: foodTypeMap[typeFood.value],
        time_available: timeAvailable.value,
        budget: budget.value,
        quick_filter: quickFilter.value,
        coords: coords.value ? `${coords.value.latitude},${coords.value.longitude}` : null
      }
    })
    console.log('Recomendaciones recibidas:', response.data)

    places.value = response.data

    if (searchMode.value === 'chat') {
      if (places.value.length === 0) {
        if (chatRef.value) {
          chatRef.value.pushMessage("Lo siento 🙈 no encontré lugares relacionados. ¿Podrías preguntarme por algo de comida o bebida? 🍽️")

          await delay(500)

          chatRef.value.pushFilters()
        }
      } else {
        chatRef.value.pushMessage("Encontré algunos lugares para tí 🍽️")

        await delay(500)

        chatRef.value.pushPlaces(places.value)
        chatRef.value.setCoords(coords.value)
      }
    }

    clearFilters()
    isLoading.value = false
  } catch (err) {
    error.value = 'No se pudieron obtener recomendaciones 😢'
    console.error(err)

    clearFilters()
    isLoading.value = false
  }
}

const recommendByFilter = async (value, type) => {
  selectValue(value, type)

  if (chatRef.value) {
    await delay(500)

    let text = ''
    if (value === 'lunch') {
      text = 'Comidas 🍛'
    } else if (value === 'sweets') {
      text = 'Dulces 🍰'
    } else if (value === 'drinks') {
      text = 'Bebidas 🍹'
    }

    chatRef.value.pushMessage(`Buscando lugares para "${text}"...`)
  }

  recommend()
}

function selectValue(value, type) {
  if (type === 'food') {
      typeFood.value = value
  } else if (type === 'time_available') {
      timeAvailable.value = value
  } else if (type === 'budget') {
      budget.value = value
  } else if (type === 'quick') {
      quickFilter.value = value
  }
}

function isSelectedValue(value, type) {
  if (type === 'food') {
      return typeFood.value === value
  } else if (type === 'time_available') {
      return timeAvailable.value === value
  } else if (type === 'budget') {
      return budget.value === value
  } else if (type === 'quick') {
      return quickFilter.value === value
  }
}

function clearPlaces() {
  places.value = []
}

function clearFilters() {
  message.value = null
  typeFood.value = null
  timeAvailable.value = null
  budget.value = null
  quickFilter.value = null
}

function getWhatsappWebLink(place) {
  return `https://api.whatsapp.com/send?phone=57${place.phone}&text=Hola, que platos venden?`
}

function getGoogleMapsLink(place) {
  return `https://www.google.com/maps?q=${place.geolocation.lat},${place.geolocation.lng}`;
}

onMounted(() => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        coords.value = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude
        }
      },
      (err) => {
        error.value = "No pudimos obtener tu ubicación 😓"
        console.error(err)
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0,
      }
    )
  } else {
    error.value = "Tu navegador no permite geolocalización 😥"
  }
})
</script>
