<script setup lang="ts">
import {useRoute} from "vue-router";
import {computed, onMounted, ref} from "vue";
import {formatTime} from "../../../utils/utils.ts";
import {RawRecognition} from "../../../types.ts";
import {Timeline} from "primevue";
import {readCache, updateCache} from "../../../utils/cache.ts";
import {useJump} from "../../../utils/useJump.ts";

const id = Number((useRoute().params as { id: string }).id);
const recognition = ref([] as RawRecognition[]);

const jump = useJump();


const timeline = computed(() => {
  console.log(recognition.value)
  return recognition.value.map((item) => ({
    text: item.text,
    start: item.start,
    period: formatTime(item.start),
    mapping: item.mapping
  }))
})

const getMappings = async () => {
  const cache = await readCache(id);
  if (!cache.points || cache.points.length === 0 || recognition.value[0]?.mapping?.point) {
    return;
  }
  cache.points.forEach((point) => {
    point?.subtitles?.forEach((subtitle) => {
      subtitle.raw_recognition.forEach((period) => {
        const idx = recognition.value.findIndex((item) => item.start === period.start);
        if (idx !== -1) {
          recognition.value[idx].mapping = {
            point: point,
            subtitle: subtitle,
          }
        }
      })
    })
  })
  await updateCache(id, {raw_recognition: recognition.value})
}

const getRecognition = async () => {
  const cache = await readCache(id);
  console.log(cache)
  recognition.value = cache.raw_recognition;
}

onMounted(async () => {
  await getRecognition();
  await getMappings();
});
</script>

<template>
  <div>
    <Timeline :value="timeline" :pt="{eventOpposite: { class: '!flex-0 !min-w-2/5'} }">
      <template #content="slotProps" >
        <div>
          {{ slotProps.item.text }}
        </div>

      </template>
      <template #opposite="slotProps">
        <div class="dark:text-white/50 text-black/50 text-[14px]" :id="`time-${slotProps.item.start}`">
          {{ slotProps.item.period }}
        </div>
        <Button severity="secondary" size="small" class="mt-2"
                v-if="slotProps.item?.mapping?.point && slotProps.item?.mapping?.subtitle"
                @click="jump.jumpToNote(id, slotProps.item?.mapping?.point?.name)"
                :label="`${slotProps.item?.mapping?.point?.name} / ${slotProps.item?.mapping?.subtitle?.subtitle}`"></Button>
      </template>
    </Timeline>
  </div>

</template>

<style scoped>

</style>