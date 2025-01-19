<script setup lang="ts">
import {useRoute} from "vue-router";
import {computed, onMounted, ref} from "vue";
import {formatDuration, readCache} from "../../../utils.ts";
import {RawRecognition} from "../../../types.ts";
import {Timeline} from "primevue";
const id = Number(useRoute().params.id);

const recognition = ref([] as RawRecognition[]);
const timeline = computed(() => {
  return recognition.value.map((item) => ({
    text: item.text,
    period: formatDuration(item.start, item.end, '\n'),
  }))
})

const getRecognition = async () => {
  const cache = await readCache(id);
  console.log(cache)
  recognition.value = cache?.raw_recognition;
}

onMounted(async () => {
  await getRecognition();
});
</script>

<template>
  <Timeline :value="timeline" :pt="{eventOpposite: { class: '!flex-0 !min-w-1/4'} }">
    <template #content="slotProps">
      {{ slotProps.item.text }}
    </template>
    <template #opposite="slotProps">
      <div class="text-white/50 font-mono">
        {{ slotProps.item.period }}
      </div>
    </template>
  </Timeline>
</template>

<style scoped>

</style>