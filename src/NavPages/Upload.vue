<template>
  <div class="flex justify-center px-4">
    <div class="w-full max-w-[720px] rounded-[18px] border border-[#00000018] bg-white p-8 shadow-sm mt-6">
      <div class="mb-7">
        <p class="text-3xl inter-bold">Upload Note</p>
        <p class="text-sm text-black/50 mt-1">
          Share a study note, file, and helpful links with NoteHub.
        </p>
      </div>

      <form class="flex flex-col gap-5" @submit.prevent="handleUpload">
        <div>
          <label class="text-sm font-medium text-black/70">Title</label>
          <input
            v-model="title"
            type="text"
            placeholder="e.g. Trends in Application Development"
            class="mt-2 w-full rounded-[10px] border border-black/10 bg-black/[0.03] px-4 py-3 outline-none transition focus:border-purple-400 focus:bg-white"
          />
        </div>

        <div>
          <label class="text-sm font-medium text-black/70">Description</label>
          <textarea
            v-model="description"
            rows="5"
            placeholder="Write a short description of your note..."
            class="mt-2 w-full resize-none rounded-[10px] border border-black/10 bg-black/[0.03] px-4 py-3 outline-none transition focus:border-purple-400 focus:bg-white"
          ></textarea>
        </div>

        <div class="grid gap-5 md:grid-cols-2">
          <div>
            <label class="text-sm font-medium text-black/70">Subject</label>
            <input
              v-model="subject"
              type="text"
              placeholder="e.g. CSDC105"
              class="mt-2 w-full rounded-[10px] border border-black/10 bg-black/[0.03] px-4 py-3 outline-none transition focus:border-purple-400 focus:bg-white"
            />
          </div>

          <div>
            <label class="text-sm font-medium text-black/70">File Link</label>
            <input
              v-model="fileLink"
              type="text"
              placeholder="https://"
              class="mt-2 w-full rounded-[10px] border border-black/10 bg-black/[0.03] px-4 py-3 outline-none transition focus:border-purple-400 focus:bg-white"
            />
          </div>
        </div>

        <div class="rounded-[14px] border border-black/10 bg-black/[0.025] p-5">
          <label class="text-sm font-medium text-black/70">Edit Permission</label>

          <select
            v-model="editableByOthers"
            class="mt-2 w-full rounded-[10px] border border-black/10 bg-white px-4 py-3 text-sm outline-none transition focus:border-purple-400"
          >
            <option :value="false">Only I can edit this note</option>
            <option :value="true">Other logged-in users can edit this note</option>
          </select>
        </div>

        <div class="rounded-[14px] border border-black/10 bg-black/[0.025] p-5">
          <div class="mb-3">
            <p class="text-sm font-medium text-black/70">Attached Links</p>
            <p class="text-xs text-black/45">Add references, docs, or helpful resources.</p>
          </div>

          <div class="flex gap-2">
            <input
              v-model="linkInput"
              type="url"
              placeholder="https://example.com/resource"
              class="flex-1 rounded-[10px] border border-black/10 bg-white px-4 py-3 text-sm outline-none transition focus:border-purple-400"
              @keydown.enter.prevent="addLink"
            />

            <button
              type="button"
              class="rounded-[10px] bg-black px-5 py-3 text-sm font-medium text-white transition hover:bg-black/80"
              @click="addLink"
            >
              Add
            </button>
          </div>

          <p v-if="linkError" class="mt-2 text-sm text-red-600">
            {{ linkError }}
          </p>

          <div v-if="links.length" class="mt-4 flex flex-wrap gap-2">
            <div
              v-for="link in links"
              :key="link"
              class="flex max-w-full items-center gap-2 rounded-full border border-purple-100 bg-purple-50 px-3 py-2 text-sm text-purple-800"
            >
              <span class="max-w-[260px] truncate">{{ link }}</span>

              <button
                type="button"
                class="text-purple-500 hover:text-red-500"
                :aria-label="`Remove ${link}`"
                @click="removeLink(link)"
              >
                ×
              </button>
            </div>
          </div>
        </div>

        <button
          type="submit"
          class="inter-regular mt-2 w-full rounded-[10px] bg-purple-800 px-4 py-3 text-white transition hover:bg-purple-900"
        >
          Upload Note
        </button>
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
      editableByOthers: false,
      linkInput: "",
      links: [],
      linkError: ""
    }
  },

  methods: {
    normalizeUrl(value) {
      const trimmedUrl = value.trim()

      if (!trimmedUrl) {
        return ""
      }

      try {
        const parsedUrl = new URL(trimmedUrl)

        if (!["http:", "https:"].includes(parsedUrl.protocol) || !parsedUrl.hostname) {
          return ""
        }

        return parsedUrl.href
      } catch {
        return ""
      }
    },

    addLink() {
      this.linkError = ""
      const normalizedLink = this.normalizeUrl(this.linkInput)

      if (!normalizedLink) {
        this.linkError = "Please enter a valid http or https URL."
        return
      }

      if (this.links.includes(normalizedLink)) {
        this.linkError = "This link has already been added."
        return
      }

      this.links.push(normalizedLink)
      this.linkInput = ""
    },

    removeLink(link) {
      this.links = this.links.filter(existingLink => existingLink !== link)
    },

    async handleUpload() {
      try {
        if (!this.title || !this.description || !this.subject || !this.fileLink) {
          alert("Please fill in all fields")
          return
        }

        if (this.linkInput.trim()) {
          this.addLink()

          if (this.linkError) {
            return
          }
        }

        const token = localStorage.getItem("token")

        if (!token) {
          alert("You must be logged in to upload a note.")
          return
        }

        const res = await fetch("http://127.0.0.1:5000/api/notes", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + token
          },
          body: JSON.stringify({
            title: this.title,
            description: this.description,
            subject: this.subject,
            fileLink: this.fileLink,
            links: this.links,
            editable_by_others: this.editableByOthers
          })
        })

        const data = await res.json()

        if (!res.ok) {
          throw new Error(data.message || "Upload failed")
        }

        alert("Note uploaded successfully!")

        this.title = ""
        this.description = ""
        this.subject = ""
        this.fileLink = ""
        this.editableByOthers = false
        this.linkInput = ""
        this.links = []
        this.linkError = ""
      } catch (err) {
        console.error("Upload failed:", err)
        alert("Upload failed: " + err.message)
      }
    }
  }
}
</script>