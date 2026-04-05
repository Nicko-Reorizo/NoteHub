<template>
<div class="flex justify-center">
  <div class="UploadForm border border-[#00000018] rounded-[10px] p-7 mt-5">
    <p class="text-2xl inter-bold">Upload Note</p>

    <form class="flex flex-col" @submit.prevent="handleUpload">
      <label class="mt-5">Title</label>
      <input v-model="title" type="text" placeholder="Note Title." />

      <label class="mt-5">Description</label>
      <textarea v-model="description" placeholder="Note Description..."></textarea>

      <label class="mt-5">Subject</label>
      <input v-model="subject" type="text" placeholder="Type your subject." />

      <label class="mt-5">File Link</label>
      <input v-model="fileLink" type="text" placeholder="https://" />

      <input type="submit" value="Upload Note" class="inter-regular mt-5 w-full rounded-[3px] cursor-pointer bg-purple-800 p-1 py-2.5 text-white" />
    </form>
  </div>
</div>
</template>

<script>
export default {
  name: "Upload",
  data() {
    return {
      title: "",
      description: "",
      subject: "",
      fileLink: ""
    }
  },
  methods: {
  async handleUpload() {
  try {
    if (!this.title || !this.description || !this.subject || !this.fileLink) {
      alert("Please fill in all fields");
      return;
    }

    const token = localStorage.getItem("token");
    if (!token) {
      alert("You must be logged in to upload a note.");
      return;
    }

    const res = await fetch("http://127.0.0.1:5000/api/notes", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
      },
      body: JSON.stringify({
        title: this.title,
        description: this.description,
        subject: this.subject,
        fileLink: this.fileLink
      })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.message || "Upload failed");

    alert("Note uploaded successfully!");
    
    // Clear the form
    this.title = "";
    this.description = "";
    this.subject = "";
    this.fileLink = "";

  } catch (err) {
    console.error("Upload failed:", err);
    alert("Upload failed: " + err.message);
  }
}
}
}
</script>