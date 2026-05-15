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

        const res = await fetch("http://127.0.0.1:5000/api/notes", {
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
  <p class="inter-bold text-3xl text-left md:px-30 lg:px-0">
    Browse Notes
  </p>

  <div class="grid 2xl:grid-cols-3 md:grid-cols-2 justify-items-center space-y-10 mt-5">
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
</template>