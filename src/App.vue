<script setup>
import {ref} from 'vue';
import Login from './Login.vue';
import Home from './Home.vue';
import Upload from './NavPages/Upload.vue';
import BrowseNotes from './NavPages/BrowseNotes.vue';

const currPage = ref('login');

function handleLoginSuccess() {
  currPage.value = 'home';
}
</script>

<template>
  <Login v-if="currPage === 'login'" @login-success="handleLoginSuccess" />
  <Home v-else-if="currPage === 'home'" />
  <Upload v-else-if="currPage === 'upload'" />
</template>

<style scoped>

</style>
