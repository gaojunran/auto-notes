<script setup lang="ts">
import {ref, watch} from "vue";

const props = defineProps<{
  pointName: string;
  subtitles: Subtitle[];
}>()

const id = Number((useRoute().params as { id: string }).id);

const show = defineModel('show', { type: Boolean, default: false })

import {Dialog, Textarea, SelectButton} from "primevue";
import {Subtitle} from "../types.ts";
import {updatePointCache} from "../utils/cache.ts";
import {useRoute} from "vue-router";

const options = props.subtitles?.map((subtitle) => subtitle.subtitle) ?? [];
const currentSelect = ref((options && options[0]) ?? '');
const currentMarkdown = ref(props.subtitles?.find((subtitle) => subtitle.subtitle === currentSelect.value)?.md ?? '');

watch(currentSelect, async (newVal, oldVal) => {
    await saveAndUpdate(oldVal, newVal)
  },
)

const saveAndUpdate = async (oldVal: string, newVal?: string) => {
  // 保存此前更改内容
  const subtitleIndex = props.subtitles?.findIndex((subtitle) => subtitle.subtitle === oldVal);
  if (subtitleIndex === -1) return;
  const subtitles = [...props.subtitles];
  subtitles[subtitleIndex].md = currentMarkdown.value; // 单个subtitle的引用和笔记页的subtitle引用相同，所以可以同步更新
  await updatePointCache(id, props.pointName, { subtitles: subtitles })

  // 更新文本框内容
  if (newVal) {
    currentMarkdown.value = props.subtitles?.find((subtitle) => subtitle.subtitle === newVal)?.md || '';
  }
}

const onClose = async () => {
  await saveAndUpdate(currentSelect.value);
  show.value = false;
}


</script>

<template>
  <Dialog v-model:visible="show" modal :style="{ width: '75%' }" header="编辑笔记" @hide="onClose"
          :pt="{header: '!pb-0'}"
  >
    <div class="flex justify-center items-center mb-6">
      <SelectButton :allow-empty="false" v-model="currentSelect" :options="options" />
    </div>

    <div class="flex justify-center items-center">
      <Textarea v-model="currentMarkdown" :rows="15" :cols="50" />
    </div>

  </Dialog>
</template>

<style scoped>

</style>