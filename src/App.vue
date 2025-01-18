<script setup lang="ts">
import {onMounted, ref} from "vue";
import {Command} from "@tauri-apps/plugin-shell";
import { resolveResource } from '@tauri-apps/api/path';
import Loading from "./components/Loading.vue";
import {testConnection} from "./apis.ts";
import {bootService, info, installUv, success} from "./utils.ts";
import {checkUvInstalled} from "./utils.ts";
const loading = ref(false)
const result = ref("")
let tried = false;

onMounted(async () => {
  if (!await checkUvInstalled()) {
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
  <div class="bg-gradient-to-br from-gray-900 to-gray-800 min-h-screen">
    <RouterView v-slot="{ Component }">
      <transition name="fade">
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