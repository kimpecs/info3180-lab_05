import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MoviesView from '../views/MoviesView.vue' 
import AddMovieFormView from '../views/AddMovieFormView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/movies',
      name: 'Movies',
      component: MoviesView // Should now be recognized
    },
    {
      path: '/movies/create',
      name: 'AddMovieForm',
      component: AddMovieFormView
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router