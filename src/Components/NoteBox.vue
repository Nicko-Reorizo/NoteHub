<template>
  <div>
    <!-- Card -->
    <div class="w-[320px] h-[200px] border border-[#00000018] rounded-[5px]">
      <div class="titleDiv p-6">
        <p class="inter-bold pb-1 text-lg">{{ Title }}</p>

        <p
          class="text-xs mb-3 bg-blue-100 text-[#00007c] inline-block p-1 px-2.5 rounded-2xl"
        >
          {{ Subject }}
        </p>

        <div class="description pb-3">
          <p class="text-sm opacity-75 line-clamp-2 min-h-[2.5rem]">
            {{ Description }}
          </p>
        </div>

        <div class="details flex justify-between items-center">
          <div class="namedate flex gap-2">
            <p class="text-xs opacity-55">{{ Username }}</p>
            <p class="text-xs opacity-55">{{ Date }}</p>
          </div>

          <button
            @click="showModal = true"
            class="text-sm px-3 p-2 font-medium border opacity-50 rounded-[5px] border-[#0000004b]"
          >
            View Details
          </button>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 px-4"
    >
      <div
        class="bg-white w-full max-w-[700px] rounded-[10px] border border-[#00000018] shadow-lg p-6 relative"
      >
        <button
          @click="showModal = false"
          class="absolute top-6 right-4 text-sm px-3 py-1 border rounded-[5px] border-[#00000030]"
        >
          Close
        </button>

        <div class="flex justify-between items-start gap-4 mb-4">
          <div>
            <h2 class="text-3xl font-semibold mb-2">{{ Title }}</h2>
            <div class="flex gap-2 text-sm text-black/60">
              <p>By {{ Username }}</p>
              <p>·</p>
              <p>{{ Date }}</p>
            </div>
          </div>

          <p
            class="text-xs bg-blue-100 text-[#00007c] inline-block px-3 py-1 rounded-2xl whitespace-nowrap mr-15"
          >
            {{ Subject }}
          </p>
        </div>

        <p class="text-base leading-7 text-black/80 mb-6">
          {{ Description }}
        </p>

        <div class="border-t pt-5 flex gap-3">
          <button
            class="bg-[#0f172a] text-white px-5 py-3 rounded-[6px] font-medium"
          >
            Open File
          </button>

          <button
            v-if="isOwner"
            class="border px-5 py-3 rounded-[6px] font-medium"
          >
            Edit
          </button>

          <button
            v-if="isOwner"
            class="bg-red-500 text-white px-5 py-3 rounded-[6px] font-medium"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
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
      currentUser: null
    }
  },
  computed: {
    isOwner() {
      return this.currentUser && this.currentUser.id === this.userId
    }
  },
  mounted() {
    const user = localStorage.getItem("user")
    if (user) {
      this.currentUser = JSON.parse(user)
    }
  }
}
</script>