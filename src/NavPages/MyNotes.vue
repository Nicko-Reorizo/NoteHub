<template>
    <p class="text-3xl inter-bold">My Notes</p>
    <div class="grid 2xl:grid-cols-3 lg:grid-cols-2 justify-items-center space-y-5 mt-5">
    <NoteBox
      Title="Introduction to Calculus"
      Subject="Mathematics"
      Description="Comprehensive notes covering limits, derivatives, and integrals..."
      Username="Nicko Reorizo"
      Date="29/03/2026"
    />
    <NoteBox
      Title="Physics Notes"
      Subject="Physics"
      Description="Covers mechanics, waves, and thermodynamics with practice problems."
      Username="Maria Santos"
      Date="28/03/2026"
    />
    <NoteBox
      Title="Chemistry Notes"
      Subject="Chemistry"
      Description="Organic chemistry summary with reaction mechanisms."
      Username="Juan Dela Cruz"
      Date="27/03/2026"
    />
    </div>
</template>
<style></style>
<script>
import NoteBox from '../Components/NoteBox.vue'
    export default{
        components:{NoteBox}
}</script>