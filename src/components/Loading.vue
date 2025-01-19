<script setup lang="ts">
import {Dialog, ProgressSpinner} from "primevue";

const loading = defineModel();

const props = defineProps({
  title: String,
  subtitle: String,
})
</script>

<template>
<Dialog v-model:visible="loading" modal class="w-1/2 pt-8 pb-4"
  :pt="{
    header: {
      class: '!hidden'
    },
  }">
  <div class="flex items-center justify-center h-full">
    <div class="flex flex-col items-center">
      <ProgressSpinner class="!h-12 !w-12 !m-4" />
      <div class="text-center mb-2 text-white">{{title}}</div>
      <div class="text-center text-sm text-white/40">{{subtitle}}</div>
    </div>
  </div>

</Dialog>
</template>

<style scoped>

</style>