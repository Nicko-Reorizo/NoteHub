<template>
  <div>
    <!-- Navbar -->
    <div class="nav border-b border-[#0000002f] h-[50px]  xl:px-70 lg:px-40 md:px-30 flex items-center justify-between">
      <div class="flex items-center">
        <img :src="logo" alt="Logo" class="w-[100px] h-[100px]" />
        
      </div>

      <div class="space-x-8 text-sm">
        <button @click="currComponent='browsenotes'" class="inter-semibold HomeBtn opacity-75">Home</button>
        <button @click="currComponent='upload'" class="inter-semibold UploadBtn opacity-75">Upload</button>
        <button @click="currComponent='mynotes'" class="inter-semibold MyNotesBtn opacity-75">MyNotes</button>
        <button @click="logout" class="inter-semibold LogoutBtn p-2 px-3 rounded-[10px] text-white">Log out</button>
      </div>
    </div>

    <!-- Upload Section -->
    <div class=" xl:px-[18vw] lg:px-[20vw]  pt-10">
      <BrowseNotes v-if="currComponent==='browsenotes'"/>
      <Upload v-else-if="currComponent==='upload'"/>
      <MyNotes v-else-if="currComponent==='mynotes'"/>
    </div>
  </div>
</template>

<script>
import Upload from './NavPages/Upload.vue';
import BrowseNotes from './NavPages/BrowseNotes.vue';
import MyNotes from './NavPages/MyNotes.vue';
import logo from './assets/Logo2.png';
import {ref} from 'vue';

const currComponent = ref('browsenotes');



export default {
  name: "Home",
  components: { Upload, BrowseNotes, MyNotes },
  data() {
    return { logo,
      currComponent: 'browsenotes'
     }
  },
  methods:{
 logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("user");

      window.location.reload();
    }
  }
}
</script>