
  <template>
    <div class="min-h-screen flex items-start justify-center p-6">
      <div class="w-full max-w-2xl">
        <div class="flex flex-col sm:flex-row gap-4">
          <button
              @click="navigateTo('/upload')"
              class="flex-1 bg-gradient-to-r from-green-500 to-teal-600 text-white font-semibold py-4 px-6 rounded-lg shadow-lg hover:from-green-600 hover:to-teal-700 transition duration-300 ease-in-out flex items-center justify-center"
          >
            <UploadIcon class="w-6 h-6 mr-2" />
            上传音频
          </button>
          <button
              @click="navigateTo('/network')"
              class="flex-1 bg-gradient-to-r from-purple-500 to-indigo-600 text-white font-semibold py-4 px-6 rounded-lg shadow-lg hover:from-purple-600 hover:to-indigo-700 transition duration-300 ease-in-out flex items-center justify-center"
          >
            <NetworkIcon class="w-6 h-6 mr-2" />
            知识点网络
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
            class="mb-2"
            :key="history.id"
            :id="history.id"
            :tags="history.tags"
            :duration="history.duration"
            :abstract="history.abstract"
            :topic="history.topic"
            @cardClick="navigateTo(`/detail/recognition/${history.id}`)"
        >
        </HistoryCard>
        <Button outlined icon="pi pi-cog" class="!fixed !bottom-0 !right-0 !mr-4 !mb-4" rounded
                @click="navigateTo('/settings')"
        ></Button>
      </div>
    </div>
  </template>

  <script setup lang="ts">
    import { MicIcon, UploadIcon, NetworkIcon } from 'lucide-vue-next'
    import {useRouter} from "vue-router";
    import {onMounted, ref} from "vue";
    import { load } from '@tauri-apps/plugin-store';
    import { Cache } from "../types.js";
    import HistoryCard from "../components/HistoryCard.vue";
    import {readAllCache, readCache} from "../utils/cache.ts";

    const router = useRouter()
    const histories = ref([] as Cache[])

    const navigateTo = (url: string) => {
      router.push(url);
    }

    onMounted(async () => {
      histories.value = await readAllCache();
    })
  </script>
