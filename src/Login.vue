<template>
  <div class="flex h-screen w-full items-center justify-center">
    <div
      class="LoginBox flex flex-col justify-center space-y-2.5 w-[450px] border border-[#00000018] rounded-[10px] p-5 pt-10 pb-15 px-10"
    >
      <div class="LoginTitle text-center flex flex-col justify-center">
        <img
          class="w-[150px] self-center"
          :src="logo"
          alt="Logo"
        />

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

        <p class="mt-2 text-center text-[#0000007a] pt-1">
          Don't have an account?
          <span
            @click="isRegister = !isRegister"
            class="text-blue-600 underline opacity-100 cursor-pointer"
          >
            {{ isRegister ? "Back to Login" : "Register Now" }}
          </span>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import axios from "axios"
import logo from "./assets/Logo.png"

const email = ref("")
const password = ref("")
const name = ref("")
const isRegister = ref(false)
const API_BASE_URL = "http://127.0.0.1:5000/api"

const emit = defineEmits(["login-success"])

async function handleSubmit() {
  if (!email.value || !password.value || (isRegister.value && !name.value)) {
    alert("Please fill all fields")
    return
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

  if (!emailRegex.test(email.value)) {
    alert("Invalid email format")
    return
  }

  if (password.value.length < 8) {
    alert("Password must be at least 8 characters")
    return
  }

  if (isRegister.value && name.value.length < 2) {
    alert("Name must be at least 2 characters")
    return
  }

  try {
    if (isRegister.value) {
      await axios.post(`${API_BASE_URL}/register`, {
        name: name.value,
        email: email.value,
        password: password.value
      })

      alert("Registered successfully! You can now login.")
      isRegister.value = false
      return
    }

    const response = await axios.post(`${API_BASE_URL}/login`, {
      email: email.value,
      password: password.value
    })

    const data = response.data

    localStorage.setItem("token", data.access_token)
    localStorage.setItem("user", JSON.stringify(data.user))

    alert("Login successful!")
    emit("login-success")
  } catch (error) {
    if (error.response?.data?.message) {
      alert(error.response.data.message)
      return
    }

    if (error.request) {
      alert("Could not reach the NoteHub server. Please make sure the Flask API is running on http://127.0.0.1:5000.")
      return
    }

    alert(error.message || "Something went wrong")
  }
}
</script>

<style></style>