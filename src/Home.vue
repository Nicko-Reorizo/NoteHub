<template>
  <div>
    <!-- Navbar -->
    <div class="nav border-b border-[#0000002f] h-[60px]  xl:px-70 lg:px-40 md:px-30 flex items-center justify-between">
      <div class="flex items-center">
        <img :src="logo" alt="Logo" class="w-[100px] h-[100px]" />
        
      </div>

      <div class="space-x-8 text-sm flex items-center">
  <button @click="currComponent='browsenotes'" class="inter-semibold HomeBtn opacity-75">
    Home
  </button>

  <button @click="currComponent='upload'" class="inter-semibold UploadBtn opacity-75">
    Upload
  </button>

  <button @click="currComponent='mynotes'" class="inter-semibold MyNotesBtn opacity-75">
    MyNotes
  </button>

  <div class="relative">
    <button
      @click="showProfileMenu = !showProfileMenu"
      class="inter-semibold flex items-center gap-2 rounded-[10px] bg-black px-4 py-2 text-white"
    >
      {{ currentUser?.name || "Profile" }}

      <span class="text-xs">
        ▼
      </span>
    </button>

    <div
      v-if="showProfileMenu"
      class="absolute right-0 mt-2 w-[170px] rounded-[10px] border border-black/10 bg-white p-2 shadow-lg z-50"
    >
      <p class="px-3 py-2 text-xs text-black/50">
        Signed in as
      </p>

      <p class="px-3 pb-2 text-sm font-medium text-black truncate">
        {{ currentUser?.name }}
      </p>

      <button
        @click="logout"
        class="w-full rounded-[8px] px-3 py-2  text-sm text-red-500 hover:bg-red-400 font-medium text-white bg-red-500 text-center"
      >
        Log out
      </button>
    </div>
  </div>
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
      currComponent: 'browsenotes',
       showProfileMenu: false,
    currentUser: JSON.parse(localStorage.getItem("user")) || null
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