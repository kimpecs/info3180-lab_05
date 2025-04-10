<template>
  <form id="movieForm" @submit.prevent="saveMovie">
    <!-- Form fields here -->
  </form>
</template>

<script setup>
import { ref, onMounted } from 'vue'

let csrf_token = ref('')

function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then(response => response.json())
    .then(data => csrf_token.value = data.csrf_token)
}

function saveMovie() {
  const formData = new FormData(document.getElementById('movieForm'))
  fetch('/api/v1/movies', {
    method: 'POST',
    body: formData,
    headers: { 'X-CSRFToken': csrf_token.value }
  })
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error))
}

onMounted(getCsrfToken)
</script>