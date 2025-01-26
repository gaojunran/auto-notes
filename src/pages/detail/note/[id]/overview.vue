<script setup lang="ts">

import {computed, onMounted, ref} from "vue";
import Loading from "../../../../components/Loading.vue";
import {getNote} from "../../../../apis.ts";
import {Point} from "../../../../types.ts";
import {useRoute} from "vue-router";
import {OrganizationChart} from "primevue";
import {Cache} from "../../../../types.ts";
import {readCache, updateCache} from "../../../../utils/cache.ts";
import {useJump} from "../../../../utils/useJump.ts";

const loading = ref(false);
const points = ref([] as Point[])
const id = Number((useRoute().params as {id: string}).id);

const cache = ref({} as Cache)

const jump = useJump();

const org = computed(() => {
  return {
    key: "root",
    label: cache.value.topic,
    level: 0,
    children: points.value.map(point => {
      return {
        key: point.name,
        point: point.name,
        label: point.name,
        level: 1,
        children: point?.subtitles?.map(subtitle => {
          return {
            key: subtitle.subtitle,
            point: point.name,
            subtitle: subtitle.subtitle,
            label: subtitle.subtitle,
            level: 2,
          }
        })
      }
    })
  }
})

const jumpTo = (point?: string, subtitle?: string) => {
  if (!point && !subtitle) {
    return;
  } else if (point && !subtitle) {  // level == 1
    jump.jumpToNote(id, point)
  } else {  // level == 2
    jump.jumpToNote(id, point, subtitle)
  }
}

onMounted(async () => {
  cache.value = await readCache(id)
  if (cache.value?.points?.length) { // use cache if exists
    points.value = cache.value.points;
  } else {   // request from server
    loading.value = true;
    const response = await getNote({
      abstract: cache.value.abstract,
      topic: cache.value.topic,
      raw_recognition: cache.value.raw_recognition
    });
    points.value = response.points;
    loading.value = false;
    await updateCache(id, {points: points.value})
  }
});
</script>

<template>
  <div>
    <Loading v-model="loading" title="正为您生成笔记..." subtitle="耗时将取决于您上传的录音时长，请耐心等待。"></Loading>
    <div class="font-bold text-lg">本课思维导图</div>
    <OrganizationChart :value="org">
      <template #default="slotProps">
        <Button :label="slotProps.node.label" severity="secondary" @click="jumpTo(slotProps.node.point, slotProps.node.subtitle)"/>
      </template>
    </OrganizationChart>
  </div>

</template>

<style scoped>

</style>