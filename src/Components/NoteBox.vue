  <template>
    <div>
      <!-- Card -->
      <div class="w-[320px] h-[200px] border border-[#00000018] rounded-[5px]">
        <div class="titleDiv p-6">
          <p class="inter-bold pb-1 text-lg">{{ Title }}</p>

          <p
            :class="[
              'text-xs inline-block mb-3 px-3 py-1 rounded-2xl font-medium',
              subjectColor
            ]"
          >
            {{ Subject }}
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

      <!-- Main Modal -->
      <div v-if="showModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 px-4">
        <div class="bg-white w-full max-w-[700px] rounded-[10px] border border-[#00000018] shadow-lg p-6 relative overflow-hidden">
          <button
            @click="showModal = false"
            class="absolute top-6 right-4 text-sm px-3 py-1 border rounded-[5px] border-[#00000030]"
          >
            Close
          </button>

          <div class="flex justify-between items-start gap-4 mb-4">
            <div class="w-full pr-24">
              <h2 class="text-3xl font-semibold mb-2">
                {{ Title }}
              </h2>

              <div class="flex gap-2 text-sm text-black/60">
                <p>By {{ Username }}</p>
                <p>·</p>
                <p>{{ Date }}</p>
              </div>
            </div>

            <p
              :class="[
                'text-xs inline-block px-3 py-1 rounded-2xl whitespace-nowrap mr-15',
                subjectColor
              ]"
            >
              {{ Subject }}
            </p>
          </div>

          <textarea
            v-if="isEditing"
            v-model="editDescription"
            rows="5"
            class="appearance-none w-full text-base leading-7 text-black/80 mb-6 px-0 py-2 outline-none border-0 focus:ring-0 resize-none bg-transparent break-words whitespace-pre-wrap"
          ></textarea>

          <p
            v-else
            class="text-base leading-7 text-black/80 mb-6 break-words whitespace-pre-wrap max-h-[180px] overflow-y-auto"
          >
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

          <div class="pt-5 flex gap-3">
            <button
              title="Open File"
              @click="openFile"
              class="w-10 h-10 rounded-[6px] flex items-center justify-center transition bg-black text-white shadow-sm hover:bg-black/80 hover:shadow-md"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path d="M3 7h6l2 2h10v10H3z" />
              </svg>
            </button>

            <button
              title="Edit"
              :disabled="!isOwner"
              @click="handleEditClick"
              :class="[
                'w-10 h-10 rounded-[6px] flex items-center justify-center transition',
                isOwner ? 'hover:bg-black/20 cursor-pointer' : 'opacity-30 cursor-not-allowed'
              ]"
            >
              <svg v-if="!isEditing" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path d="M12 20h9" />
                <path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z" />
              </svg>

              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path d="M5 13l4 4L19 7" />
              </svg>
            </button>

            <button
              title="Version History"
              :disabled="!isOwner"
              @click="openVersionHistory"
              :class="[
                'w-10 h-10 rounded-[6px] flex items-center justify-center transition',
                isOwner ? 'hover:bg-black/20 cursor-pointer' : 'opacity-30 cursor-not-allowed'
              ]"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path d="M12 8v5l3 2" />
                <path d="M3 12a9 9 0 1 0 3-6.7" />
                <path d="M3 3v5h5" />
              </svg>
            </button>

            <button
              title="Delete"
              :disabled="!isOwner"
              @click="showDeleteConfirm = true"
              :class="[
                'w-10 h-10 rounded-[6px] flex items-center justify-center text-red-500 transition',
                isOwner ? 'hover:bg-black/20 cursor-pointer' : 'opacity-30 cursor-not-allowed'
              ]"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path d="M3 6h18" />
                <path d="M8 6V4h8v2" />
                <path d="M6 6l1 14h10l1-14" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Confirm Edit Modal -->
      <div v-if="showEditConfirm" class="fixed inset-0 bg-black/40 flex items-center justify-center z-[60] px-4">
        <div class="bg-white w-full max-w-[360px] rounded-[12px] border border-[#00000018] shadow-xl p-5">
          <p class="text-lg font-semibold mb-2">Save changes?</p>
          <p class="text-sm text-black/60 mb-5">
            This will update the note description.
          </p>

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

      <!-- Confirm Delete Modal -->
      <div v-if="showDeleteConfirm" class="fixed inset-0 bg-black/40 flex items-center justify-center z-[60] px-4">
        <div class="bg-white w-full max-w-[360px] rounded-[12px] border border-[#00000018] shadow-xl p-5">
          <p class="text-lg font-semibold mb-2">Delete note?</p>
          <p class="text-sm text-black/60 mb-5">
            This action cannot be undone.
          </p>

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

      <!-- Version History Modal -->
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
            <div
              v-for="version in versions"
              :key="version.id"
              class="border border-black/10 rounded-[10px] p-4"
            >
              <div class="mb-3">
                <p class="text-sm font-medium text-black">
                  Modified by {{ version.edited_by || 'Unknown' }}
                </p>

                <p class="text-xs text-black/50">
                  {{ version.edited_at }}
                </p>
              </div>

              <p class="text-sm text-black/80 break-words whitespace-pre-wrap max-h-[120px] overflow-y-auto mb-3">
                {{ version.description }}
              </p>

              <button
                @click="askRestoreVersion(version.id)"
                class="text-sm bg-black text-white px-4 py-2 rounded-[6px] hover:bg-black/80"
              >
                Restore
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Confirm Restore Modal -->
      <div v-if="showRestoreConfirm" class="fixed inset-0 bg-black/40 flex items-center justify-center z-[80] px-4">
        <div class="bg-white w-full max-w-[360px] rounded-[12px] border border-[#00000018] shadow-xl p-5">
          <p class="text-lg font-semibold mb-2">Restore this version?</p>

          <p class="text-sm text-black/60 mb-5">
            Your current note will be replaced by this saved version.
          </p>

          <div class="flex justify-end gap-2">
            <button
              @click="cancelRestoreVersion"
              class="px-4 py-2 rounded-[6px] hover:bg-black/10 text-sm"
            >
              Cancel
            </button>

            <button
              @click="confirmRestoreVersion"
              class="px-4 py-2 rounded-[6px] bg-black text-white text-sm hover:bg-black/80"
            >
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
      userId: { type: Number, required: true }
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
        localDescription: this.Description,
        editDescription: this.Description
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
      normalizedLinks() {
        return Array.isArray(this.links) ? this.links.filter(Boolean) : []
      }
    },

    methods: {
      openFile() {
        if (!this.fileLink) return
        window.open(this.fileLink, "_blank")
      },

      handleEditClick() {
        if (!this.isOwner) return

        if (!this.isEditing) {
          this.isEditing = true
          return
        }

        this.showEditConfirm = true
      },

      async confirmSaveEdit() {
        this.showEditConfirm = false
        await this.saveEdit()
      },

      async saveEdit() {
        const token = localStorage.getItem("token")

        const res = await fetch(`http://localhost:5000/api/notes/${this.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({
            description: this.editDescription
          })
        })

        if (res.ok) {
          this.localDescription = this.editDescription
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

        const res = await fetch(`http://localhost:5000/api/notes/${this.id}`, {
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
        if (!this.isOwner) return

        const token = localStorage.getItem("token")

        const res = await fetch(`http://localhost:5000/api/notes/${this.id}/versions`, {
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
    `http://localhost:5000/api/notes/${this.id}/versions/${versionId}/restore`,
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
      this.localDescription = restoredVersion.description
      this.editDescription = restoredVersion.description
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
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
  }
  </style>
