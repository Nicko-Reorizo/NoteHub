<script setup>
import { ref } from 'vue'
import Login from './Login.vue'
import Home from './Home.vue'
import Upload from './NavPages/Upload.vue'
import LandingPage from './LandingPage.vue'

const currPage = ref('landing')

function handleLoginSuccess() {
  currPage.value = 'home'
}

function showLogin() {
  currPage.value = 'login'
}
</script>

<template>
  <LandingPage v-if="currPage === 'landing'" @login="showLogin" />
  <Login v-else-if="currPage === 'login'" @login-success="handleLoginSuccess" />
  <Home v-else-if="currPage === 'home'" />
  <Upload v-else-if="currPage === 'upload'" />
</template>