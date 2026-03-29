<template>
  <div class="flex h-screen w-full items-center justify-center">
    <div
      class="LoginBox flex flex-col justify-center space-y-2.5 w-[450px] border border-[#00000018] rounded-[10px] p-5 pt-10"
    >
      <div class="LoginTitle text-center flex flex-col justify-center">
        <img
          class="rounded-full w-[50px] mb-2 self-center"
          :src="logo"
          alt="Logo"
        />
        <p class="inter-bold text-2xl mb-1">NoteHub</p>
        <p class="inter-regular opacity-75 mb-4">Sign in to your account.</p>
      </div>

      <div class="LoginInput text-[15px]">
        <form @submit.prevent="handleSubmit" class="flex flex-col">
          <div v-if="isRegister">
            <label>Name</label>
            <input
              v-model="name"
              type="text"
              class="h-[35px] mb-4 p-3 w-full inter-semibold rounded-[5px] border border-[#00000013]"
              placeholder="Your name"
            />
          </div>
          <label>Email</label>
          <input
            v-model="email"
            type="text"
            class="h-[35px] mb-4 p-3 w-full inter-semibold rounded-[5px] border border-[#00000013]"
            placeholder="name@gmail.com"
          />

          <label>Password</label>
          <input
            v-model="password"
            type="password"
            placeholder="******"
            class="h-[35px] mb-4 p-3 w-full inter-semibold rounded-[5px] border border-[#00000013]"
          />

          <input
            type="submit"
            :value="isRegister ? 'Register' : 'Sign-in'"
            class="inter-regular mt-5 w-full rounded-[3px] bg-purple-800 p-1 py-2.5 text-white cursor-pointer"
          />
        </form>

        <p class="mt-2 text-center text-[#0000007a]">
          Don't have an account?
          <span class="text-blue-600 underline opacity-100 cursor-pointer">
            <span
              @click="isRegister = !isRegister"
              class="text-blue-600 underline opacity-100 cursor-pointer"
            >
              {{ isRegister ? "Back to Login" : "Register Now" }}
            </span></span
          >
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import logo from "./assets/Logo.png";

const email = ref("");
const password = ref("");
const name = ref("");
const isRegister = ref(false);

const emit = defineEmits(["login-success"]);


async function handleSubmit() {
  if (!email.value || !password.value || (isRegister.value && !name.value)) {
    alert("Please fill all fields");
    return;
  }

  try {
    if (isRegister.value) {
      // REGISTER
      await axios.post("http://localhost:5000/api/register", {
        name: name.value,
        email: email.value,
        password: password.value,
      });

      alert("Registered successfully! You can now login.");
      isRegister.value = false;
    } else {
      // LOGIN
      const response = await axios.post("http://localhost:5000/api/login", {
        email: email.value,
        password: password.value,
      });

      const data = response.data;

      localStorage.setItem("token", data.access_token);
      localStorage.setItem("user", JSON.stringify(data.user));

      alert("Login successful!");
      emit("login-success");
    }
  } catch (error) {
    alert(error.response?.data?.message || "Something went wrong");
  }
}
</script>

<style></style>
