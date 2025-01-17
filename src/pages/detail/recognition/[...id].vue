<script setup lang="ts">
import {useRoute} from "vue-router";
import {onMounted, ref} from "vue";
import {readCache} from "../../../utils.ts";

const id = Number(useRoute().params.id);

const recognition = ref(null);

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
<div class="text-white">
  {{ recognition }}
</div>
</template>

<style scoped>

</style>