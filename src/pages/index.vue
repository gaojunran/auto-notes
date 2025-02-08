
  <template>
    <div class="min-h-screen flex items-start justify-center p-6">
      <div class="w-full max-w-2xl">
        <div class="flex flex-col sm:flex-row gap-4">
          <button
              @click="navigateTo('/upload')"
              class="flex-1 bg-gradient-to-r dark:from-green-500 dark:to-teal-600 
              dark:text-white text-black from-green-200 to-teal-300
               font-semibold py-4 px-6 rounded-lg shadow-lg dark:hover:from-green-600 dark:hover:to-teal-700 transition duration-300 ease-in-out flex items-center justify-center
               cursor-pointer"
          >
            <UploadIcon class="w-6 h-6 mr-2" />
            {{ i18n("Upload Audio", "上传音频") }}
          </button>
          <button
              @click="navigateTo('/network')"
              class="flex-1 bg-gradient-to-r dark:from-purple-500 dark:to-indigo-600 
              dark:text-white text-black from-purple-200 to-indigo-300
              font-semibold py-4 px-6 rounded-lg shadow-lg dark:hover:from-purple-600 dark:hover:to-indigo-700 transition duration-300 ease-in-out flex items-center justify-center
              cursor-pointer"
          >
            <NetworkIcon class="w-6 h-6 mr-2" />
            {{ i18n("Knowledge Graph", "知识图谱") }}
          </button>

        </div>
        <div class="text-lg text-black dark:text-white mt-10 mb-4 font-bold">
          {{ i18n("Previous Lectures", "历史课程") }}
        </div>
        <div class="text-center text-white/50 mt-4 "
          v-if="histories.length === 0"
        >
          {{ i18n("No Previous Lectures", "还没有历史课程，快去上传吧") }}
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
        <Button icon="pi pi-cog" class="!fixed !bottom-0 !right-0 !mr-4 !mb-4" rounded severity="secondary"
                @click="navigateTo('/settings')"
        ></Button>
      </div>
    </div>
  </template>

  <script setup lang="ts">
    import { UploadIcon, NetworkIcon } from 'lucide-vue-next'
    import {useRouter} from "vue-router";
    import {onMounted, ref} from "vue";
    import { Cache } from "../types.js";
    import HistoryCard from "../components/HistoryCard.vue";
    import { readAllCache } from "../utils/cache.ts";
    import {useEnglish} from "../utils/useEnglish.ts";

    const isEnglish = ref(false);

    const { i18n } = useEnglish();

    const router = useRouter()
    const histories = ref([] as Cache[])

    const navigateTo = (url: string) => {
      router.push(url);
    }

    onMounted(async () => {
      histories.value = await readAllCache();
    })
  </script>
