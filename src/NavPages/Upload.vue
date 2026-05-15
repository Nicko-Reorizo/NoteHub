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

      <label class="mt-5">Add Link</label>
      <div class="flex gap-2">
        <input
          v-model="linkInput"
          type="url"
          placeholder="https://example.com/resource"
          class="flex-1"
          @keydown.enter.prevent="addLink"
        />
        <button
          type="button"
          class="rounded-[3px] border border-[#00000018] px-4 py-2 text-sm hover:bg-black/5"
          @click="addLink"
        >
          Add Link
        </button>
      </div>
      <p v-if="linkError" class="mt-2 text-sm text-red-600">{{ linkError }}</p>

      <div v-if="links.length" class="mt-3 flex flex-wrap gap-2">
        <div
          v-for="link in links"
          :key="link"
          class="flex max-w-full items-center gap-2 rounded-[6px] border border-[#00000018] bg-black/[0.03] px-3 py-2 text-sm"
        >
          <span class="max-w-[260px] truncate">{{ link }}</span>
          <button
            type="button"
            class="text-black/50 hover:text-red-600"
            :aria-label="`Remove ${link}`"
            @click="removeLink(link)"
          >
            x
          </button>
        </div>
      </div>

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
      fileLink: "",
      linkInput: "",
      links: [],
      linkError: ""
    }
  },
  methods: {
  normalizeUrl(value) {
    const trimmedUrl = value.trim();

    if (!trimmedUrl) {
      return "";
    }

    try {
      const parsedUrl = new URL(trimmedUrl);
      if (!["http:", "https:"].includes(parsedUrl.protocol) || !parsedUrl.hostname) {
        return "";
      }
      return parsedUrl.href;
    } catch {
      return "";
    }
  },

  addLink() {
    this.linkError = "";
    const normalizedLink = this.normalizeUrl(this.linkInput);

    if (!normalizedLink) {
      this.linkError = "Please enter a valid http or https URL.";
      return;
    }

    if (this.links.includes(normalizedLink)) {
      this.linkError = "This link has already been added.";
      return;
    }

    this.links.push(normalizedLink);
    this.linkInput = "";
  },

  removeLink(link) {
    this.links = this.links.filter(existingLink => existingLink !== link);
  },

  async handleUpload() {
  try {
    if (!this.title || !this.description || !this.subject || !this.fileLink) {
      alert("Please fill in all fields");
      return;
    }

    if (this.linkInput.trim()) {
      this.addLink();
      if (this.linkError) return;
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
        fileLink: this.fileLink,
        links: this.links
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
    this.linkInput = "";
    this.links = [];
    this.linkError = "";

  } catch (err) {
    console.error("Upload failed:", err);
    alert("Upload failed: " + err.message);
  }
}
}
}
</script>
