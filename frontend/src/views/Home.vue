<template>
  <section class="hero is-fullheight is-primary is-bold">
    <div class="hero-body">
      <div class="container has-text-centered">
        <h1 class="title is-1 has-text-white">
          Bienvenido a La Ruta del Sabor
        </h1>
        <h2 class="subtitle is-3 has-text-white-bis">
          Descubre los mejores sabores de Girardot, recomendados para ti 🍲
        </h2>
        <p class="has-text-white mt-5 is-size-5">
          Desde arepas hasta ceviches, nuestra inteligencia culinaria te sugiere
          lugares increíbles según lo que tienes y deseas.
        </p>
        <div class="buttons is-centered mt-6">
          <button class="button is-light is-large is-rounded" @click="$router.push('/explore')">
            Explorar ahora
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  background-image: linear-gradient(
      rgba(0, 0, 0, 0.6),
      rgba(0, 0, 0, 0.6)
    ),
    url('https://images.unsplash.com/photo-1600891964599-f61ba0e24092?auto=format&fit=crop&w=1350&q=80');
  background-size: cover;
  background-position: center;
}
</style>