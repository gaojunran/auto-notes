<script setup lang="ts">

import {computed, onMounted, ref} from "vue";
import Loading from "../../../../components/Loading.vue";
import {getExport, getNote} from "../../../../apis.ts";
import {Point} from "../../../../types.ts";
import {useRoute} from "vue-router";
import {OrganizationChart} from "primevue";
import {Cache} from "../../../../types.ts";
import {readCache, updateCache} from "../../../../utils/cache.ts";
import {useJump} from "../../../../utils/useJump.ts";
import { load } from "@tauri-apps/plugin-store";
import { info } from "../../../../utils/utils.ts";
import {useEnglish} from "../../../../utils/useEnglish.ts";


const loading = ref(false);
const points = ref([] as Point[])
const id = Number((useRoute().params as {id: string}).id);

const cache = ref({} as Cache)

const jump = useJump();

const { i18n } = useEnglish();

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

const exportNote = async () => {
  loading.value = true;
  if (await getExport(
    {
      id: id,
      topic: cache.value.topic,
      abstract: cache.value.abstract,
      points: points.value,
    }
  )) {
    loading.value = false;
    await info("导出成功！");
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
    <div class="flex justify-between items-center mb-8">
      <div class="font-bold text-xl dark:text-white text-black">
        {{ i18n("MindMap", "思维导图") }}
      </div>
      <Button icon="pi pi-file-pdf" :label="i18n('Export PDF', '导出为PDF')" size="small"
        @click="exportNote()"
      ></Button>
    </div>
    
    <OrganizationChart :value="org" collapsible :pt="{node: '!p-0'}">
      <template #default="slotProps">
        <Button :label="slotProps.node.label"
                :pt="{root: '!max-w-30 !text-xs'}"
                severity="secondary" @click="jumpTo(slotProps.node.point, slotProps.node.subtitle)"/>
      </template>
    </OrganizationChart>
  </div>

</template>

<style scoped>

</style>