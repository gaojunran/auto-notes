<template>
  <div
      class="w-full bg-gray-900 shadow-lg rounded-lg overflow-hidden transition-all duration-300 ease-in-out transform hover:scale-102 hover:shadow-xl cursor-pointer"
      @click="$emit('cardClick')"
  >
    <div class="p-6">
      <h2 class="text-2xl font-bold text-gray-100 mb-2">{{ topic }}</h2>
      <p class="text-gray-300 mb-4">{{ abstract }}</p>
      <div class="flex items-center justify-between">
        <div class="flex items-center">
          <ClockIcon class="h-5 w-5 text-gray-400 mr-2" />
          <span class="text-sm text-gray-400">{{ formatTime(duration) }}</span>
        </div>
        <div class="flex flex-wrap gap-2">
          <span
              v-for="tag in tags"
              :key="tag"
              class="px-2 py-1 text-xs font-semibold text-indigo-300 bg-indigo-900 rounded-full"
          >
            {{ tag }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ClockIcon } from 'lucide-vue-next'

defineProps({
  id: {
    type: Number,
    required: true
  },
  topic: {
    type: String,
    required: true
  },
  abstract: {
    type: String,
    required: true
  },
  duration: {
    type: Number,
    required: true
  },
  tags: {
    type: Array,
    required: false
  },

})

defineEmits(['cardClick'])

const formatTime = (seconds) => {
  const hours = Math.floor(seconds / 3600);
  const remainingSeconds = seconds % 3600;
  const minutes = Math.floor(remainingSeconds / 60);
  const finalSeconds = remainingSeconds % 60;

  const paddedHours = String(hours).padStart(2, '0');
  const paddedMinutes = String(minutes).padStart(2, '0');
  const paddedSeconds = String(finalSeconds).padStart(2, '0');

  return `${paddedHours}:${paddedMinutes}:${paddedSeconds}`;
}
</script>