<script setup lang="ts">

import {onMounted, ref} from "vue";
import Loading from "../../../../components/Loading.vue";
import {readCache, updateCache} from "../../../../utils.ts";
import {getNote} from "../../../../apis.ts";
import {Point} from "../../../../types.ts";
import {useRoute, useRouter} from "vue-router";

const loading = ref(false);
const points = ref([] as Point[])
const id = Number(useRoute().params.id);

const router = useRouter();

const navigateToPoint = async (name: string) => {
  await router.push({path: `/detail/note/${id}`, query: {point: name}})
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
});
</script>

<template>
  <Loading v-model="loading" title="正为您生成笔记..." subtitle="耗时将取决于您上传的录音时长，请耐心等待。"></Loading>
  <div class="font-bold text-lg">本课思维导图</div>
  <div class="">(TODO)</div>
  <div class="font-bold text-lg mt-8 mb-4">本课知识点</div>
  <Button v-for="point in points" :key="point.name" :label="point.name" severity="secondary"
          class="!text-sm" @click="navigateToPoint(point.name)"
  ></Button>

</template>

<style scoped>

</style>