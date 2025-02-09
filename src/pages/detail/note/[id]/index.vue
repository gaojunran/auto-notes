<script setup lang="ts">
import {getNote} from "../../../../apis.ts";
import {onMounted, ref} from "vue";
//@ts-ignore
import MarkDown from "vue3-markdown-it";
import {useRoute, useRouter} from "vue-router";
import {formatTime} from "../../../../utils/utils.ts";
import Loading from "../../../../components/Loading.vue";
import {Point, RawRecognition} from "../../../../types.ts";
import {Divider, Popover} from "primevue";
import {readCache, updateCache} from "../../../../utils/cache.ts";
import {useJump} from "../../../../utils/useJump.ts";
import KateX from "@vscode/markdown-it-katex"
import EditNotes from "../../../../components/EditNotes.vue";
import {useEnglish} from "../../../../utils/useEnglish.ts";
import {useBeta} from "../../../../utils/useBeta.ts";

const id = Number((useRoute().params as { id: string }).id);
const loading = ref(false);

const points = ref([] as Point[])
const currentPoint = ref({} as Point);

const router = useRouter();
const route = useRoute();

const jump = useJump();

const popover = ref();
const showEditNotes = ref(false);

const { i18n } = useEnglish();
const { isBeta } = useBeta();

const togglePopover = (event: any) => {
  popover.value.toggle(event);
}

const navigateToOverview = async () => {
  await router.push(`/detail/note/${id}/overview`);
}

const getStartTime = (recognitions: RawRecognition[]) => {
  let start = recognitions[0].start;
  // let end = recognitions[recognitions.length - 1].end;
  return formatTime(start);
}

onMounted(async () => {
  const cache = await readCache(id)
  if (cache?.points?.length) { // use cache if exists
    points.value = cache.points;
  } else {   // request from server
    loading.value = true;
    const response = await getNote({
      abstract: cache.abstract,
      topic: cache.topic,
      raw_recognition: cache.raw_recognition
    });
    points.value = response.points;
    loading.value = false;
    await updateCache(id, {points: points.value})
  }
  currentPoint.value = points.value.find((point) => point.name === route.query.point) ?? points.value[0];
});

</script>

<template>
  <div class="h-full">
    <Loading v-model="loading" title="正为您生成笔记..." subtitle="耗时将取决于您上传的录音时长，请耐心等待。"></Loading>
    <EditNotes v-if="currentPoint.name && currentPoint.subtitles" :point-name="currentPoint.name" :subtitles="currentPoint.subtitles" v-model:show="showEditNotes" ></EditNotes>
    <div class="flex flex-col justify-between h-full">
      <div class="flex gap-4 mb-4 items-center">
<!--        <div class="font-bold text-xl">-->
<!--          {{ currentPoint.name }}-->
<!--        </div>-->
        <Button v-for="point in points" :key="point.name" :label="point.name" :severity="currentPoint.name === point.name ? 'info' :'secondary'"
                size="small" @click="currentPoint = point"
        ></Button>
        <Button v-show="isBeta" label="Logic & Bit Operations" severity="secondary" size="small"></Button>
        <Button v-show="isBeta" label="Equivalent Propositions" severity="secondary" size="small"></Button>
      </div>

      <div id="main" class="flex-1 max-h-[70vh] overflow-y-auto">
        <div v-for="subtitle in currentPoint.subtitles" :key="subtitle.name" :id="subtitle.name">
          <div class="flex">
            <div id="subtitle" class="flex-none w-1/4 text-right pr-6">
              <div class="font-bold text-lg">
                {{ subtitle.subtitle }}
              </div>
              <Button :pt="{label: {class: '!text-xs'}}"
                      size="small" :label="getStartTime(subtitle.raw_recognition)" severity="secondary"
                      class="mt-2" @click="jump.jumpToRecognition(id, subtitle.raw_recognition[0].start)"
              ></Button>
            </div>
            <div id="md" class="flex-1 -mt-1">
              <MarkDown :source="subtitle.md" :plugins="[{ plugin: KateX }]"></MarkDown>
            </div>
          </div>
          <Divider :pt="{root: {class: '!py-3 !my-0'}}" />
        </div>
      </div>

      <div id="importance" class="flex gap-2 mt-0 mb-0 w-max-content rounded-md flex-0">
        <i class="pi pi-star-fill text-yellow-500" v-for="i in currentPoint.importance || 0" :key="i" />
        <i class="pi pi-star text-gray-400" v-for="i in 5 - currentPoint.importance || 0" :key="i" />
      </div>
      <div id="points" class="w-full rounded mb-2 flex flex-wrap justify-start items-center gap-4 flex-0">
        <Button @click="navigateToOverview" :label="i18n('Overview', '总览')" icon="pi pi-book" size="small" severity="secondary"></Button>
        <Button @click="showEditNotes = true" :label="i18n('Edit Notes', '编辑笔记')" icon="pi pi-pencil" size="small" severity="secondary"></Button>
        <Button :label="i18n('Related Links', '相关链接')" severity="secondary" size="small" icon="pi pi-link"
                @click="togglePopover"
        />
        <Popover ref="popover">
          <a v-for="link in currentPoint.links" :key="link.name" :href="link.href" target="_blank"
             class="p-1 hover:underline dark:text-white/50 text-black/50 dark:hover:text-white hover:text-black transition block"
          >
            {{link.name}}
          </a>
          <a v-if="currentPoint.links.length === 0">
            暂无相关链接
          </a>
        </Popover>

      </div>
    </div>
  </div>


</template>

<style>
#md h1 {
  font-weight: bold;
  margin-top: 4px;
  margin-bottom: 4px;
  font-size: 18px;
  color: indigo;
}

.app-dark #md h1 {
  color: lightblue;
}

#md strong {
  color: indigo;
}

.app-dark #md strong {
  color: lightblue;
}

#md ul {
  list-style-type: disc;
  list-style-position: inside;
}

#md ol {
  list-style-type: decimal;
  list-style-position: inside;
}

</style>