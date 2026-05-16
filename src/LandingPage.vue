<template>
  <div class="min-h-screen bg-[#faf9ff] text-black">
    <nav class="flex items-center justify-between px-8 py-6">
      <div class="flex items-center gap-3">
         <img :src="logo" alt="Logo" class=" h-[60px]" />
        
      </div>

      <div class="flex gap-3">
        <button
          @click="$emit('login')"
          class="px-5 py-2 rounded-[8px] border border-black/10 hover:bg-black/5 transition"
        >
          Login
        </button>

        <button
          @click="$emit('login')"
          class="px-5 py-2 rounded-[8px] bg-purple-800 text-white hover:bg-purple-900 transition"
        >
          Register
        </button>
      </div>
    </nav>

    <main class="flex flex-col items-center justify-center text-center px-6 pt-20">
      <p class="mb-4 rounded-full bg-purple-100 px-4 py-2 text-sm font-medium text-purple-800">
        Organize. Share. Collaborate.
      </p>

      <h1 class="max-w-[850px] text-5xl md:text-6xl inter-black ">
        YOUR MODERN SPACE FOR <span class="text-purple-800">SMARTER</span>  NOTE SHARING.
      </h1>

      <p class="mt-6 max-w-[620px] text-lg text-black/60 leading-8">
        NoteHub helps students upload, manage, edit, and share notes with file links,
        attached resources, edit permissions, and version history.
      </p>

      <div class="mt-9 flex flex-col sm:flex-row gap-4">
        <button
          @click="$emit('login')"
          class="rounded-[10px] bg-purple-800 px-20 py-5 text-white font-medium hover:bg-black/80 transition"
        >
          Login
        </button>

        <button
          @click="$emit('login')"
          class="rounded-[10px] border border-black/10 bg-white px-20 py-5 font-medium  hover:bg-purple-50 hover:text-purple-800 transition"
        >
          Register
        </button>
      </div>

      <div class="mt-16 grid gap-6 md:grid-cols-3 max-w-[1050px] w-full">
  <div class="group rounded-[22px] border border-purple-200 bg-white p-7 text-left shadow-[0_20px_60px_rgba(88,28,135,0.10)] transition duration-300 hover:-translate-y-2 hover:shadow-[0_25px_70px_rgba(88,28,135,0.18)]">
    <div class="mb-5 flex h-12 w-12 items-center justify-center rounded-[14px] bg-purple-100 text-purple-800">
      <svg class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path d="M12 5v14" />
        <path d="M5 12h14" />
      </svg>
    </div>

    <p class="text-xl font-bold mb-3">Upload Notes</p>
    <p class="text-sm text-black/60 leading-7">
      Save notes with subjects, descriptions, file links, and helpful resources in one clean space.
    </p>
  </div>

  <div class="group rounded-[22px] border border-purple-200 bg-white p-7 text-left shadow-[0_20px_60px_rgba(88,28,135,0.10)] transition duration-300 hover:-translate-y-2 hover:shadow-[0_25px_70px_rgba(88,28,135,0.18)]">
    <div class="mb-5 flex h-12 w-12 items-center justify-center rounded-[14px] bg-purple-100 text-purple-800">
      <svg class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
        <circle cx="9" cy="7" r="4" />
        <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
        <path d="M16 3.13a4 4 0 0 1 0 7.75" />
      </svg>
    </div>

    <p class="text-xl font-bold mb-3">Collaborate</p>
    <p class="text-sm text-black/60 leading-7">
      Let other logged-in users contribute when needed using flexible edit permissions.
    </p>
  </div>

  <div class="group rounded-[22px] border border-purple-200 bg-white p-7 text-left shadow-[0_20px_60px_rgba(88,28,135,0.10)] transition duration-300 hover:-translate-y-2 hover:shadow-[0_25px_70px_rgba(88,28,135,0.18)]">
    <div class="mb-5 flex h-12 w-12 items-center justify-center rounded-[14px] bg-purple-100 text-purple-800">
      <svg class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path d="M12 8v5l3 2" />
        <path d="M3 12a9 9 0 1 0 3-6.7" />
        <path d="M3 3v5h5" />
      </svg>
    </div>

    <p class="text-xl font-bold mb-3">Version History</p>
    <p class="text-sm text-black/60 leading-7">
      Track edits, view previous changes, and restore older note versions anytime.
    </p>
  </div>
</div>
    </main>
  </div>
</template>
<script setup>
import logo from "./assets/Logo3.png"

defineEmits(["login"])
</script>