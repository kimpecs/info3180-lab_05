<template>
  <div class="movie-form">
    <!-- Success Message -->
    <div v-if="successMessage" class="alert alert-success">
      {{ successMessage }}
    </div>

    <!-- Error Messages -->
    <div v-if="errors.length" class="alert alert-danger">
      <div v-for="(error, index) in errors" :key="index">
        {{ error }}
      </div>
    </div>

    <form @submit.prevent="saveMovie" id="movieForm" enctype="multipart/form-data">
      <div class="form-group mb-3">
        <label class="form-label">Movie Title</label>
        <input type="text" v-model="formData.title" name="title" class="form-control" required>
      </div>

      <div class="form-group mb-3">
        <label class="form-label">Description</label>
        <textarea v-model="formData.description" name="description" class="form-control" required></textarea>
      </div>

      <div class="form-group mb-3">
        <label class="form-label">Poster</label>
        <input type="file" name="poster" accept="image/*" class="form-control" required>
      </div>

      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const csrf_token = ref('');
const successMessage = ref('');
const errors = ref([]);
const formData = ref({
  title: '',
  description: ''
});

// Fetch CSRF Token on component mount
onMounted(() => {
  fetch('/api/v1/csrf-token')
    .then(response => response.json())
    .then(data => csrf_token.value = data.csrf_token);
});

// Submit handler
function saveMovie() {
  const form = document.getElementById('movieForm');
  const formData = new FormData(form);

  fetch('/api/v1/movies', {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': csrf_token.value
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.errors) {
      errors.value = data.errors;
      successMessage.value = '';
    } else {
      successMessage.value = data.message;
      errors.value = [];
      form.reset();
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
}
</script>