<template>
  <div class="movies-view">
    <h1>Movie Collection</h1>
    <div class="movie-cards">
      <div v-for="movie in movies" :key="movie.id" class="movie-card">
        <div class="card-body">
          <h2>{{ movie.title }}</h2>
          <p class="description">{{ movie.description }}</p>
          <img :src="movie.poster" :alt="movie.title + ' poster'" class="poster">
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const movies = ref([])

async function fetchMovies() {
  try {
    const response = await fetch('/api/v1/movies')
    const data = await response.json()
    movies.value = data.movies
  } catch (error) {
    console.error('Error fetching movies:', error)
  }
}

onMounted(() => {
  fetchMovies()
})
</script>

<style scoped>
.movie-cards {
  display: grid;
  gap: 2rem;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

.movie-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.poster {
  width: 100%;
  max-height: 400px;
  object-fit: cover;
  border-radius: 4px;
  margin-top: 1rem;
}

.description {
  color: #666;
  margin: 0.5rem 0;
}
</style>