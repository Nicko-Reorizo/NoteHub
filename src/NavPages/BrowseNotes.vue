<script>
import NoteBox from '../Components/NoteBox.vue'

export default {
  components: { NoteBox },

  data() {
    return {
      notes: []
    }
  },

  mounted() {
    this.fetchNotes()
  },

  methods: {
    async fetchNotes() {
      try {
        const token = localStorage.getItem("token")

        const res = await fetch("https://notehub-4mi4.onrender.com/api/notes", {
          headers: token ? { Authorization: "Bearer " + token } : {}
        })

        this.notes = await res.json()
      } catch (err) {
        console.error("Failed to fetch notes:", err)
      }
    }
  }
}
</script>

<template>
  <section class="max-w-7xl mx-auto px-6 py-10">
  
  <!-- Header -->
  <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">
    
    <div>
      <p class="inter-bold text-4xl text-gray-900">
        Browse Notes
      </p>

      <p class="text-gray-500 mt-2">
        Discover reviewer notes, summaries, and study materials shared by others.
      </p>
    </div>

    
  </div>


  <!-- Notes Grid -->
  <div
    class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6"
  >
    <NoteBox
      v-for="note in notes"
      :key="note.id"
     
      :id="note.id"
      :fileLink="note.fileLink"
      :links="note.links"
      :Title="note.title"
      :Description="note.description"
      :Subject="note.subject"
      :Username="note.Username"
      :Date="note.Date"
      :userId="note.user_id"
      :canEdit="note.can_edit"
      :editableByOthers="note.editable_by_others"

      @note-updated="fetchNotes"
      @note-deleted="fetchNotes"
    />
  </div>

</section>
</template>