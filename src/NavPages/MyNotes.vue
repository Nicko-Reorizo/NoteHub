<template>
    <p class="text-3xl inter-bold">My Notes</p>
    <div class="grid 2xl:grid-cols-3 lg:grid-cols-2 justify-items-center space-y-5 mt-5">
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
      @note-updated="fetchNotes"
      @note-deleted="fetchNotes"
    />
    </div>
</template>
<style></style>
<script>
import NoteBox from '../Components/NoteBox.vue'
    export default{
        components:{NoteBox},
        data(){
          return{
            notes: []
          }
        },
        async mounted() {
  try {
    const res = await fetch("http://127.0.0.1:5000/api/my_notes", {
      headers: {
        "Authorization": "Bearer " + localStorage.getItem("token")
      }
    });
    this.notes = await res.json();
  } catch (err) {
    console.error("Failed to fetch notes:", err);
  }
}
    }</script>
