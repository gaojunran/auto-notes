<script setup lang="ts">
import {onMounted, ref} from "vue";
import Loading from "./components/Loading.vue";
import {bootService, checkUvInstalled, installUv} from "./utils/serviceDeps.ts";
const loading = ref(false)
let tried = false;

onMounted(async () => {
  if (!await checkUvInstalled()) {
    console.log("Installing uv...")
    await installUv(loading);
  }
  if (tried) {
    return
  }
  await bootService(loading);
  tried = true;
})


</script>

<template>

  <Toast position="bottom-right" ></Toast>
  <Loading v-model="loading" title="正在启动大模型服务..." subtitle="首次启动时可能需要安装依赖，请耐心等待..."></Loading>
  <div class="dark:bg-gradient-to-br dark:from-gray-900 dark:to-gray-800 bg-white min-h-screen">
    <RouterView v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component"/>
      </transition>
    </RouterView>
  </div>

</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>