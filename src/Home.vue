<template>
  <div>
    <!-- Navbar -->
    <div class="nav border-b border-[#0000002f] h-[50px] 2xl:px-100 xl:px-70 lg:px-40 md:px-30 flex items-center justify-between">
      <div class="flex items-center">
        <img :src="logo" alt="Logo" class="w-[30px] h-[30px] rounded-full" />
        <p class="inter-semibold ml-3">NoteHub</p>
      </div>

      <div class="space-x-8 text-sm">
        <a href="" class="inter-semibold HomeBtn">Home</a>
        <a href="" class="inter-semibold UploadBtn">Upload</a>
        <a href="" class="inter-semibold MyNotesBtn">MyNotes</a>
        <a href="" class="inter-semibold LogoutBtn p-2 px-3 rounded-[20px] text-white">Log out</a>
      </div>
    </div>

    <!-- Upload Section -->
    <div class="test flex justify-center">
      <Upload />
    </div>
  </div>
</template>

<script>
import Upload from './Upload.vue';
import logo from './assets/Logo.png';

export default {
  name: "Home",
  components: { Upload },
  data() {
    return { logo }
  }
}
</script>