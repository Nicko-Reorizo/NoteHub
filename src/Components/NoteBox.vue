<template>
  <div>
    <div class="w-[320px] h-[200px] border border-[#00000018] rounded-[5px]">
      <div class="titleDiv p-6">
        <p class="inter-bold pb-1 text-lg">{{ localTitle }}</p>

        <p :class="['text-xs inline-block mb-3 px-3 py-1 rounded-2xl font-medium', subjectColor]">
          {{ localSubject }}
        </p>

        <div class="description pb-3">
          <p class="text-sm opacity-75 line-clamp-2 min-h-[2.5rem]">
            {{ localDescription }}
          </p>
        </div>

        <div class="details flex justify-between items-center">
          <div class="namedate flex gap-2">
            <p class="text-xs opacity-55">{{ Username }}</p>
            <p class="text-xs opacity-55">{{ Date }}</p>
          </div>

          <button
            @click="showModal = true"
            class="text-sm px-3 p-2 font-medium border bg-black text-white rounded-[5px] border-[#0000004b]"
          >
            View Details
          </button>
        </div>
      </div>
    </div>

    <div v-if="showModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 px-4">
      <div class="bg-white w-full max-w-[700px] rounded-[10px] border border-[#00000018] shadow-lg p-6 relative overflow-hidden">
        <button
          @click="closeModal"
          class="absolute top-6 right-4 text-sm px-3 py-1 border rounded-[5px] border-[#00000030]"
        >
          Close
        </button>

        <div v-if="isEditing" class="pr-24">
          <label class="text-sm font-medium text-black/70">Title</label>
          <input v-model="editTitle" type="text" class="mb-3 mt-1 w-full rounded-[6px] border border-black/20 px-3 py-2" />

          <label class="text-sm font-medium text-black/70">Subject</label>
          <input v-model="editSubject" type="text" class="mb-3 mt-1 w-full rounded-[6px] border border-black/20 px-3 py-2" />

          <label class="text-sm font-medium text-black/70">Description</label>
          <textarea v-model="editDescription" rows="5" class="mb-3 mt-1 w-full rounded-[6px] border border-black/20 px-3 py-2 resize-none"></textarea>

          <label class="text-sm font-medium text-black/70">File Link</label>
          <input v-model="editFileLink" type="text" class="mb-3 mt-1 w-full rounded-[6px] border border-black/20 px-3 py-2" />

          <div v-if="isOwner" class="mb-4 rounded-[8px] border border-black/10 p-3">
            <p class="mb-2 text-sm font-medium text-black/70">Edit Permission</p>

            <label class="mb-2 flex items-center gap-3 cursor-pointer text-sm">
              <input v-model="editEditableByOthers" type="radio" :value="false" class="h-4 w-4" />
              <span>Only I can edit this note</span>
            </label>

            <label class="flex items-center gap-3 cursor-pointer text-sm">
              <input v-model="editEditableByOthers" type="radio" :value="true" class="h-4 w-4" />
              <span>Other logged-in users can edit this note</span>
            </label>
          </div>

          <label class="text-sm font-medium text-black/70">Add Link</label>
          <div class="mt-1 flex gap-2">
            <input
              v-model="editLinkInput"
              type="url"
              placeholder="https://example.com/resource"
              class="flex-1 rounded-[6px] border border-black/20 px-3 py-2"
              @keydown.enter.prevent="addEditLink"
            />

            <button type="button" class="rounded-[6px] border border-black/20 px-4 py-2 text-sm hover:bg-black/5" @click="addEditLink">
              Add
            </button>
          </div>

          <p v-if="editLinkError" class="mt-2 text-sm text-red-600">
            {{ editLinkError }}
          </p>

          <div v-if="editLinks.length" class="mt-3 flex flex-wrap gap-2">
            <div
              v-for="link in editLinks"
              :key="link"
              class="flex max-w-full items-center gap-2 rounded-[6px] border border-[#00000018] bg-black/[0.03] px-3 py-2 text-sm"
            >
              <span class="max-w-[260px] truncate">{{ link }}</span>

              <button type="button" class="text-black/50 hover:text-red-600" @click="removeEditLink(link)">
                x
              </button>
            </div>
          </div>
        </div>

        <div v-else>
          <div class="flex justify-between items-start gap-4 mb-4">
            <div class="w-full pr-24">
              <h2 class="text-3xl font-semibold mb-2">
                {{ localTitle }}
              </h2>

              <div class="flex gap-2 text-sm text-black/60">
                <p>By {{ Username }}</p>
                <p>·</p>
                <p>{{ Date }}</p>
              </div>

              <p class="mt-2 text-xs text-black/50">
                {{ localEditableByOthers ? "Editable by other logged-in users" : "Editable by owner only" }}
              </p>
            </div>

            <p :class="['text-xs inline-block px-3 py-1 rounded-2xl whitespace-nowrap mr-15', subjectColor]">
              {{ localSubject }}
            </p>
          </div>

          <p class="text-base leading-7 text-black/80 mb-6 break-words whitespace-pre-wrap max-h-[180px] overflow-y-auto">
            {{ localDescription }}
          </p>

          <div v-if="normalizedLinks.length" class="mb-6">
            <p class="mb-2 text-sm font-medium text-black/70">Attached Links</p>

            <div class="flex flex-wrap gap-2">
              <a
                v-for="link in normalizedLinks"
                :key="link"
                :href="link"
                target="_blank"
                rel="noopener noreferrer"
                class="max-w-full truncate rounded-[6px] border border-[#00000018] bg-black/[0.03] px-3 py-2 text-sm text-purple-800 hover:bg-purple-50"
              >
                {{ link }}
              </a>
            </div>
          </div>
        </div>

        <div class="pt-5 flex gap-3">
          <button
            title="Open File"
            @click="openFile"
            class="w-10 h-10 rounded-[6px] flex items-center justify-center transition bg-black text-white shadow-sm hover:bg-black/80 hover:shadow-md"
          >
            Open
          </button>

          <button
            title="Edit"
            :disabled="!canEditNote"
            @click="handleEditClick"
            :class="[
              'w-10 h-10 rounded-[6px] flex items-center justify-center transition',
              canEditNote ? 'hover:bg-black/20 cursor-pointer' : 'opacity-30 cursor-not-allowed'
            ]"
          >
            {{ isEditing ? "Save" : "Edit" }}
          </button>

          <button
            title="Version History"
            :disabled="!canEditNote"
            @click="openVersionHistory"
            :class="[
              'w-20 h-10 rounded-[6px] flex items-center justify-center transition text-sm',
              canEditNote ? 'hover:bg-black/20 cursor-pointer' : 'opacity-30 cursor-not-allowed'
            ]"
          >
            History
          </button>

          <button
            title="Delete"
            :disabled="!isOwner"
            @click="showDeleteConfirm = true"
            :class="[
              'w-14 h-10 rounded-[6px] flex items-center justify-center text-red-500 transition text-sm',
              isOwner ? 'hover:bg-black/20 cursor-pointer' : 'opacity-30 cursor-not-allowed'
            ]"
          >
            Delete
          </button>
        </div>
      </div>
    </div>

    <div v-if="showEditConfirm" class="fixed inset-0 bg-black/40 flex items-center justify-center z-[60] px-4">
      <div class="bg-white w-full max-w-[360px] rounded-[12px] border border-[#00000018] shadow-xl p-5">
        <p class="text-lg font-semibold mb-2">Save changes?</p>
        <p class="text-sm text-black/60 mb-5">This will update the note.</p>

        <div class="flex justify-end gap-2">
          <button @click="showEditConfirm = false" class="px-4 py-2 rounded-[6px] hover:bg-black/10 text-sm">
            Cancel
          </button>

          <button @click="confirmSaveEdit" class="px-4 py-2 rounded-[6px] bg-black text-white text-sm hover:bg-black/80">
            Save
          </button>
        </div>
      </div>
    </div>

    <div v-if="showDeleteConfirm" class="fixed inset-0 bg-black/40 flex items-center justify-center z-[60] px-4">
      <div class="bg-white w-full max-w-[360px] rounded-[12px] border border-[#00000018] shadow-xl p-5">
        <p class="text-lg font-semibold mb-2">Delete note?</p>
        <p class="text-sm text-black/60 mb-5">This action cannot be undone.</p>

        <div class="flex justify-end gap-2">
          <button @click="showDeleteConfirm = false" class="px-4 py-2 rounded-[6px] hover:bg-black/10 text-sm">
            Cancel
          </button>

          <button @click="confirmDeleteNote" class="px-4 py-2 rounded-[6px] bg-red-500 text-white text-sm hover:bg-red-600">
            Delete
          </button>
        </div>
      </div>
    </div>

    <div v-if="showVersionsModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-[70] px-4">
      <div class="bg-white w-full max-w-[520px] rounded-[12px] border border-[#00000018] shadow-xl p-5">
        <div class="flex justify-between items-center mb-4">
          <div>
            <p class="text-lg font-semibold">Version History</p>
            <p class="text-sm text-black/50">Previous saved versions of this note.</p>
          </div>

          <button @click="showVersionsModal = false" class="text-sm px-3 py-1 rounded-[6px] hover:bg-black/10">
            Close
          </button>
        </div>

        <div v-if="versions.length === 0" class="text-sm text-black/60 py-8 text-center">
          No previous versions yet.
        </div>

        <div v-else class="space-y-3 max-h-[400px] overflow-y-auto pr-1">
          <div v-for="version in versions" :key="version.id" class="border border-black/10 rounded-[10px] p-4">
            <div class="mb-3">
              <p class="text-sm font-medium text-black">
                Modified by {{ version.edited_by || "Unknown" }}
              </p>

              <p class="text-xs text-black/50">
                {{ version.edited_at }}
              </p>
            </div>

            <p class="text-sm font-semibold text-black">{{ version.title }}</p>
            <p class="text-xs text-black/50 mb-2">{{ version.subject }}</p>

            <p class="text-sm text-black/80 break-words whitespace-pre-wrap max-h-[120px] overflow-y-auto mb-3">
              {{ version.description }}
            </p>

            <button @click="askRestoreVersion(version.id)" class="text-sm bg-black text-white px-4 py-2 rounded-[6px] hover:bg-black/80">
              Restore
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showRestoreConfirm" class="fixed inset-0 bg-black/40 flex items-center justify-center z-[80] px-4">
      <div class="bg-white w-full max-w-[360px] rounded-[12px] border border-[#00000018] shadow-xl p-5">
        <p class="text-lg font-semibold mb-2">Restore this version?</p>
        <p class="text-sm text-black/60 mb-5">Your current note will be replaced by this saved version.</p>

        <div class="flex justify-end gap-2">
          <button @click="cancelRestoreVersion" class="px-4 py-2 rounded-[6px] hover:bg-black/10 text-sm">
            Cancel
          </button>

          <button @click="confirmRestoreVersion" class="px-4 py-2 rounded-[6px] bg-black text-white text-sm hover:bg-black/80">
            Restore
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    id: { type: Number, required: true },
    fileLink: { type: String, required: true },
    links: { type: Array, default: () => [] },
    Title: { type: String, required: true },
    Subject: { type: String, required: true },
    Description: { type: String, required: true },
    Username: { type: String, required: true },
    Date: { type: String, required: true },
    userId: { type: Number, required: true },
    canEdit: { type: Boolean, default: false },
    editableByOthers: { type: Boolean, default: false }
  },

  data() {
    return {
      showModal: false,
      showEditConfirm: false,
      showDeleteConfirm: false,
      showVersionsModal: false,
      showRestoreConfirm: false,

      versions: [],
      selectedVersionId: null,
      currentUser: null,
      subjectColor: "",
      isEditing: false,

      localTitle: this.Title,
      localDescription: this.Description,
      localSubject: this.Subject,
      localFileLink: this.fileLink,
      localLinks: Array.isArray(this.links) ? [...this.links] : [],
      localEditableByOthers: this.editableByOthers,

      editTitle: this.Title,
      editDescription: this.Description,
      editSubject: this.Subject,
      editFileLink: this.fileLink,
      editLinks: Array.isArray(this.links) ? [...this.links] : [],
      editEditableByOthers: this.editableByOthers,
      editLinkInput: "",
      editLinkError: ""
    }
  },

  mounted() {
    const colors = [
      "bg-blue-100 text-blue-700",
      "bg-purple-100 text-purple-700",
      "bg-pink-100 text-pink-700",
      "bg-green-100 text-green-700",
      "bg-yellow-100 text-yellow-700",
      "bg-red-100 text-red-700",
      "bg-indigo-100 text-indigo-700"
    ]

    this.subjectColor = colors[Math.floor(Math.random() * colors.length)]

    const user = localStorage.getItem("user")

    if (user) {
      this.currentUser = JSON.parse(user)
    }
  },

  computed: {
    isOwner() {
      return this.currentUser && this.currentUser.id === this.userId
    },

    canEditNote() {
      return this.isOwner || this.canEdit
    },

    normalizedLinks() {
      return Array.isArray(this.localLinks) ? this.localLinks.filter(Boolean) : []
    }
  },

  methods: {
    closeModal() {
      this.showModal = false
      this.cancelEdit()
    },

    openFile() {
      if (!this.localFileLink) return
      window.open(this.localFileLink, "_blank")
    },

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

    addEditLink() {
      this.editLinkError = ""

      const normalizedLink = this.normalizeUrl(this.editLinkInput)

      if (!normalizedLink) {
        this.editLinkError = "Please enter a valid http or https URL."
        return
      }

      if (this.editLinks.includes(normalizedLink)) {
        this.editLinkError = "This link has already been added."
        return
      }

      this.editLinks.push(normalizedLink)
      this.editLinkInput = ""
    },

    removeEditLink(link) {
      this.editLinks = this.editLinks.filter(existingLink => existingLink !== link)
    },

    handleEditClick() {
      if (!this.canEditNote) return

      if (!this.isEditing) {
        this.startEdit()
        return
      }

      if (!this.editTitle || !this.editDescription || !this.editSubject || !this.editFileLink) {
        alert("Please fill in all fields")
        return
      }

      if (this.editLinkInput.trim()) {
        this.addEditLink()

        if (this.editLinkError) {
          return
        }
      }

      this.showEditConfirm = true
    },

    startEdit() {
      this.editTitle = this.localTitle
      this.editDescription = this.localDescription
      this.editSubject = this.localSubject
      this.editFileLink = this.localFileLink
      this.editLinks = [...this.localLinks]
      this.editEditableByOthers = this.localEditableByOthers
      this.editLinkInput = ""
      this.editLinkError = ""
      this.isEditing = true
    },

    cancelEdit() {
      this.isEditing = false
      this.showEditConfirm = false
      this.editLinkInput = ""
      this.editLinkError = ""
    },

    async confirmSaveEdit() {
      this.showEditConfirm = false
      await this.saveEdit()
    },

    async saveEdit() {
      const token = localStorage.getItem("token")

      const body = {
        title: this.editTitle,
        description: this.editDescription,
        subject: this.editSubject,
        fileLink: this.editFileLink,
        links: this.editLinks
      }

      if (this.isOwner) {
        body.editable_by_others = this.editEditableByOthers
      }

      const res = await fetch(`http://127.0.0.1:5000/api/notes/${this.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(body)
      })

      if (res.ok) {
        this.localTitle = this.editTitle
        this.localDescription = this.editDescription
        this.localSubject = this.editSubject
        this.localFileLink = this.editFileLink
        this.localLinks = [...this.editLinks]

        if (this.isOwner) {
          this.localEditableByOthers = this.editEditableByOthers
        }

        this.isEditing = false
        this.$emit("note-updated")
      } else {
        const error = await res.json()
        alert(error.message || "Update failed")
      }
    },

    async confirmDeleteNote() {
      this.showDeleteConfirm = false
      await this.deleteNote()
    },

    async deleteNote() {
      const token = localStorage.getItem("token")

      const res = await fetch(`http://127.0.0.1:5000/api/notes/${this.id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`
        }
      })

      if (res.ok) {
        this.showModal = false
        this.$emit("note-deleted", this.id)
      }
    },

    async openVersionHistory() {
      if (!this.canEditNote) return

      const token = localStorage.getItem("token")

      const res = await fetch(`http://127.0.0.1:5000/api/notes/${this.id}/versions`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })

      if (res.ok) {
        this.versions = await res.json()
        this.showVersionsModal = true
      } else {
        alert("Failed to load version history")
      }
    },

    askRestoreVersion(versionId) {
      this.selectedVersionId = versionId
      this.showRestoreConfirm = true
    },

    cancelRestoreVersion() {
      this.selectedVersionId = null
      this.showRestoreConfirm = false
    },

    async confirmRestoreVersion() {
      if (!this.selectedVersionId) return

      const versionId = this.selectedVersionId

      this.showRestoreConfirm = false
      this.selectedVersionId = null

      await this.restoreVersion(versionId)
    },

    async restoreVersion(versionId) {
      const token = localStorage.getItem("token")

      const res = await fetch(
        `http://127.0.0.1:5000/api/notes/${this.id}/versions/${versionId}/restore`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      if (res.ok) {
        const restoredVersion = this.versions.find(version => version.id === versionId)

        if (restoredVersion) {
          this.localTitle = restoredVersion.title
          this.localDescription = restoredVersion.description
          this.localSubject = restoredVersion.subject
          this.localFileLink = restoredVersion.fileLink
          this.localLinks = Array.isArray(restoredVersion.links) ? restoredVersion.links : []

          if (this.isOwner) {
            this.localEditableByOthers = restoredVersion.editable_by_others
          }
        }

        this.showVersionsModal = false
        this.showRestoreConfirm = false
        this.isEditing = false

        this.$emit("note-updated")
      } else {
        alert("Failed to restore version")
      }
    }
  }
}
</script>

<style scoped>
textarea {
  outline: none !important;
  box-shadow: none !important;
}
</style>