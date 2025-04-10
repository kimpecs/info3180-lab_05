<template>
  <div v-for="movie in movies" :key="movie.id">
    <h2>{{ movie.title }}</h2>
    <p>{{ movie.description }}</p>
    <img :src="movie.poster" alt="Poster">
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

let movies = ref([])

function fetchMovies() {
  fetch('/api/v1/movies')
    .then(response => response.json())
    .then(data => movies.value = data.movies)
}

onMounted(fetchMovies)
</script>