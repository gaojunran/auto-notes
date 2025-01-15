
  <template>
    <div class="min-h-screen flex items-start justify-center p-6">
      <div class="w-full max-w-2xl">
        <div class="flex flex-col sm:flex-row gap-4">
          <button
              @click="navigateTo('/record')"
              class="flex-1 bg-gradient-to-r from-purple-500 to-indigo-600 text-white font-semibold py-4 px-6 rounded-lg shadow-lg hover:from-purple-600 hover:to-indigo-700 transition duration-300 ease-in-out flex items-center justify-center"
          >
            <MicIcon class="w-6 h-6 mr-2" />
            开始录音
          </button>
          <button
              @click="navigateTo('/upload')"
              class="flex-1 bg-gradient-to-r from-green-500 to-teal-600 text-white font-semibold py-4 px-6 rounded-lg shadow-lg hover:from-green-600 hover:to-teal-700 transition duration-300 ease-in-out flex items-center justify-center"
          >
            <UploadIcon class="w-6 h-6 mr-2" />
            上传音频
          </button>
        </div>
        <div class="text-lg text-white mt-10 mb-4 font-bold">
          历史课程
        </div>
        <div class="text-center text-white/50 mt-4 "
          v-if="histories.length === 0"
        >
          暂无课程，快去录制或上传吧！
        </div>
        <HistoryCard
            v-for="history in histories"
            :key="history.id"
            :id="history.id"
            :tags="history.tags"
            :duration="history.duration"
            :abstract="history.abstract"
            :topic="history.topic"
            @cardClick="navigateTo(`/detail/recognition/${history.id}`)"
        >
        </HistoryCard>
      </div>
    </div>
  </template>

  <script setup lang="ts">
    import { MicIcon, UploadIcon } from 'lucide-vue-next'
    import {useRouter} from "vue-router";
    import {onMounted, ref} from "vue";
    import { load } from '@tauri-apps/plugin-store';
    import { CourseProps } from "../types.js";
    import HistoryCard from "./HistoryCard.vue";

    const router = useRouter()
    const histories = ref([] as CourseProps[])

    const navigateTo = (url: string) => {
      router.push(url);
    }

    const loadHistories = async () => {
      const store = await load('store.json', {autoSave: true});
      return await store.get<CourseProps[]>('cache') || [
        {id: 1, tags: ['数据结构', 'ICSI213'], duration: 3421, abstract: '这节课主要讲了关于栈和队列的理论知识。', topic: '栈和队列'}
      ];
    }

    onMounted(async () => {
      histories.value = await loadHistories()
    })
  </script>
