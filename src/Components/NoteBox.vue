<template>
    <div class="w-[320px] h-[200px] border border-[#00000018] rounded-[5px]">
      <div class="titleDiv p-6">
        <p class="inter-bold pb-1">{{ Title }}</p>
        <p class="text-xs mb-3 bg-blue-100 text-[#00007c] inline-block p-1 px-2.5 rounded-2xl">{{ Subject }}</p>
        <div class="description pb-3">
            <p class="text-sm opacity-75 line-clamp-2">{{ Description }}</p>
        </div>
        <div class="details flex justify-between items-center">
            <div class="namedate flex gap-2">
                <p class="text-xs opacity-55">{{ Username }}</p>
                <p class="text-xs opacity-55">{{ Date }}</p>
            </div>
            
            <button class="text-sm px-3 p-2 font-medium border opacity-50 rounded-[5px] border-[#0000004b]">View Details</button>
        </div>
      </div>
    </div>
</template>
<script>
export default{
    props: {
    Title: { type: String, required: true },
    Subject: { type: String, required: true },
    Description: { type: String, required: true },
    Username: { type: String, required: true },
    Date: { type: String, required: true }
  }
}
</script>