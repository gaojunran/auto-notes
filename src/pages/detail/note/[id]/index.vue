<script setup lang="ts">
import {getNote} from "../../../../apis.ts";
import {onMounted, ref} from "vue";
//@ts-ignore
import MarkDown from "vue3-markdown-it";
import {useRoute, useRouter} from "vue-router";
import {info, readCache, updateCache} from "../../../../utils.ts";
import Loading from "../../../../components/Loading.vue";
import {Point} from "../../../../types.ts";

const id = Number(useRoute().params.id);
const loading = ref(false);

const points = ref([] as Point[])
const currentPoint = ref({} as Point);

const router = useRouter();
const route = useRoute();

const navigateToOverview = async () => {
  await router.push(`/detail/note/${id}/overview`);
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
    <div id="md" class="flex-1">
      <MarkDown :source="currentPoint?.subtitles?.[0]?.md"></MarkDown>
    </div>
    <div id="importance" class="flex gap-2 mb-4 w-max-content rounded-md flex-0">
      <i class="pi pi-star-fill text-yellow-500" v-for="i in currentPoint.importance || 0" :key="i" />
      <i class="pi pi-star text-gray-400" v-for="i in 5 - currentPoint.importance || 0" :key="i" />
    </div>
    <div id="points" class="w-full rounded mb-2 flex justify-start items-center gap-4 flex-0">
      <Button @click="navigateToOverview" label="总览" icon="pi pi-book" class="!text-sm" severity="secondary"></Button>
      <Button v-for="point in points" :key="point.name" :label="point.name" :severity="currentPoint.name === point.name ? 'info' : 'secondary'"
              class="!text-sm" @click="currentPoint = point"
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