<template>
  <div class="flex h-screen w-full items-center justify-center">
    <div class="LoginBox flex flex-col justify-center space-y-2.5 w-[450px] border border-[#00000018] rounded-[10px] p-5 pt-10">
      
      <div class="LoginTitle text-center flex flex-col justify-center">
        <img class="rounded-full w-[50px] mb-2 self-center" :src="logo" alt="Logo" />
        <p class="inter-bold text-2xl mb-1">NoteHub</p>
        <p class="inter-regular opacity-75 mb-4">Sign in to your account.</p>
      </div>

      <div class="LoginInput text-[15px]">
        <form @submit.prevent="handleLogin" class="flex flex-col">
          
          <label>Email</label>
          <input v-model="email" type="text"class="h-[35px] mb-4 p-3 w-full inter-semibold rounded-[5px] border border-[#00000013]" placeholder="name@gmail.com" />

          <label>Password</label>
          <input v-model="password" type="password" placeholder="******"  class="h-[35px] mb-4 p-3 w-full inter-semibold rounded-[5px] border border-[#00000013]"/>

          <input type="submit" value="Sign-in" class="inter-regular mt-5 w-full rounded-[3px] bg-purple-800 p-1 py-2.5 text-white cursor-pointer" />
        </form>

        <p class="mt-2 text-center text-[#0000007a]">
          Don't have an account? 
          <span class="text-blue-600 underline opacity-100 cursor-pointer">
            <a href="#">
              Register Now.
            </a></span>
        </p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import logo from './assets/Logo.png';

const email = ref('');
const password = ref('');


const emit = defineEmits(['login-success']);

function handleLogin() {
  
  if (email.value === '' && password.value === '') {
    alert('Login successful!');
    emit('login-success'); 
  } else {
    alert('Login failed');
  }
}
</script>

<style>

</style>