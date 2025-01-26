<script setup lang="ts">

import {computed, onMounted, ref} from "vue";
import Loading from "../../../../components/Loading.vue";
import {getNote} from "../../../../apis.ts";
import {Point} from "../../../../types.ts";
import {useRoute, useRouter} from "vue-router";
import {OrganizationChart} from "primevue";
import {Cache} from "../../../../types.ts";
import {readCache, setShouldUpdateChart, updateCache} from "../../../../utils/cache.ts";
import {useJump} from "../../../../utils/useJump.ts";

const loading = ref(false);
const points = ref([] as Point[])
const id = Number(useRoute().params.id);

const router = useRouter();
const cache = ref({} as Cache)

const jump = useJump();

const org = computed(() => {
  return {
    label: cache.value.topic,
    level: 0,
    children: points.value.map(point => {
      return {
        label: point.name,
        level: 1,
        children: point.subtitles.map(subtitle => {
          return {
            label: subtitle.subtitle,
            parent: point.name,
            level: 2,
          }
        })
      }
    })
  }
})

const jumpTo = (name: string, level: number) => {
  if (level === 0) {
    return;
  } else if (level === 1) {  // query
    jump.jumpToNote(id, name)
  } else if (level === 2) {  // hash
    jump.jumpToNote(id, name)
    // TODO: 跳转二级知识点
  }
}

onMounted(async () => {
  cache.value = await readCache(id)
  if (cache.value.points?.length > 0) { // use cache if exists
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
        <Button :label="slotProps.node.label" severity="secondary" @click="jumpTo(slotProps.node.level === 2 ? slotProps.node.parent : slotProps.node.label, slotProps.node.level)"/>
      </template>
    </OrganizationChart>
  </div>

</template>

<style scoped>

</style>