<template>
  <div
      class="w-full bg-gray-900 shadow-lg rounded-lg overflow-hidden transition-all duration-300 ease-in-out transform hover:scale-102 hover:shadow-xl cursor-pointer relative"
      @click="$emit('cardClick')"
  >

    <div class="absolute top-6 right-6">
      <Button outlined icon="pi pi-trash" @click.stop="deleteCache(props.id); router.push('/quickjump')" severity="danger"
              :pt="{
        root: {
          class: '!border-red-500/30'
        }
              }"
      />
      <!-- click.stop 阻止事件冒泡 -->
    </div>

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
import {ClockIcon} from 'lucide-vue-next'
import Button from 'primevue/button'
import {formatTime} from "../utils/utils.ts";
import {useRouter} from "vue-router";
import {deleteCache} from "../utils/cache.ts"; // 导入 Button 组件

const router = useRouter()

const props = defineProps({
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



</script>