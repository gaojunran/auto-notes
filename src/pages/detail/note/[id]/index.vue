<script setup lang="ts">
import {getNote} from "../../../../apis.ts";
import {onMounted, ref} from "vue";
//@ts-ignore
import MarkDown from "vue3-markdown-it";
import {useRoute, useRouter} from "vue-router";
import {formatDuration, info} from "../../../../utils/utils.ts";
import Loading from "../../../../components/Loading.vue";
import {Point, RawRecognition} from "../../../../types.ts";
import {Divider, Popover} from "primevue";
import {readCache, updateCache} from "../../../../utils/cache.ts";
import {useJump} from "../../../../utils/useJump.ts";
const id = Number(useRoute().params.id);
const loading = ref(false);

const points = ref([] as Point[])
const currentPoint = ref({} as Point);

const router = useRouter();
const route = useRoute();

const jump = useJump();

const popover = ref();

const togglePopover = (event: any) => {
  popover.value.toggle(event);
}

const navigateToOverview = async () => {
  await router.push(`/detail/note/${id}/overview`);
}

const getDuration = (recognitions: RawRecognition[]) => {
  let start = recognitions[0].start;
  let end = recognitions[recognitions.length - 1].end;
  return formatDuration(start, end, "-")
}

onMounted(async () => {
  const cache = await readCache(id)
  if (cache.points?.length > 0) { // use cache if exists
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
  currentPoint.value = points.value.find((point) => point.name === route.query.point);
});

</script>

<template>
  <Loading v-model="loading" title="正为您生成笔记..." subtitle="耗时将取决于您上传的录音时长，请耐心等待。"></Loading>
  <div class="flex flex-col h-full">
    <div id="main" class="flex-1">
      <div v-for="subtitle in currentPoint.subtitles" :key="subtitle.name">
        <div class="flex" >
          <div id="subtitle" class="flex-none w-1/4 text-right pr-6">
            <div>
              {{subtitle.subtitle}}
            </div>
            <Button :pt="{label: {class: '!text-xs'}}"
                size="small" :label="getDuration(subtitle.raw_recognition)" severity="secondary"
                    class="mt-2" @click="jump.jumpToRecognition(id, subtitle.raw_recognition[0].start)"
            ></Button>
          </div>
          <div id="md" class="flex-1">
            <MarkDown :source="currentPoint?.subtitles?.[0]?.md"></MarkDown>
          </div>
        </div>
        <Divider :pt="{root: {class: '!py-3 !my-0'}}" />
      </div>


    </div>

    <div id="importance" class="flex gap-2 mb-4 w-max-content rounded-md flex-0">
      <i class="pi pi-star-fill text-yellow-500" v-for="i in currentPoint.importance || 0" :key="i" />
      <i class="pi pi-star text-gray-400" v-for="i in 5 - currentPoint.importance || 0" :key="i" />
    </div>
    <div id="points" class="w-full rounded mb-2 flex justify-start items-center gap-4 flex-0">
      <Button @click="navigateToOverview" label="总览" icon="pi pi-book" size="small" severity="secondary"></Button>
      <Button label="相关链接" severity="secondary" size="small" icon="pi pi-link"
            @click="togglePopover"
        />
      <Popover ref="popover">
        <a v-for="link in currentPoint.links" :key="link.name" :href="link.href" target="_blank"
           class="p-1 hover:underline text-white/50 hover:text-white transition block"
        >
          {{link.name}}
        </a>
      </Popover>
      <Button v-for="point in points" :key="point.name" :label="point.name" :severity="currentPoint.name === point.name ? 'info' : 'secondary'"
              size="small" @click="currentPoint = point"
      ></Button>
    </div>

  </div>

</template>

<style>
#md h1 {
  margin-bottom: 16px;
  font-size: 24px;
  font-weight: bold;
  color: lightblue;
}

#md h2 {
  margin-top: 16px;
  margin-bottom: 8px;
  font-size: 20px;
  color: lightblue;
}

</style>