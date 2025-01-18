<script setup lang="ts">
import {bootService, clearCache, installUv, success} from "../utils.ts";
import {ref} from "vue";
import Loading from "../components/Loading.vue";

const loading = ref(false)

const reinstallUv = async () => {
  await installUv(loading);
}

const rebootService = async () => {
  await bootService(loading);
}

const clearAllCache = async () => {
  await clearCache();
  await success("缓存清除成功!")
}
</script>

<template>
  <Loading v-model="loading" title="操作中，请稍后..."></Loading>
  <div class="rounded flex items-center justify-center min-h-screen">
    <div class="p-8 bg-black/20 rounded-lg flex flex-col">
      <div class="text-center mb-4 font-bold">
        以下设置请在指引下、慎重考虑后进行操作
      </div>
      <div class="flex items-center mb-4">
        <div>首次进入软件时，如果依赖安装失败，可尝试：</div>
        <Button severity="success" icon="pi pi-wrench" label="重新安装uv" size="small" @click="reinstallUv" />
      </div>
      <div class="flex items-center mb-4">
        <div>进入软件时，如果服务端启动失败，可尝试：</div>
        <Button severity="success" icon="pi pi-undo" label="重新启动服务端" size="small" @click="rebootService" />
      </div>
      <div class="flex items-center mb-4">
        <div>若进行了某些错误操作，可尝试：</div>
        <Button severity="warn" icon="pi pi-trash" label="清空缓存" size="small" @click="clearAllCache" />
      </div>
    </div>

  </div>
</template>

<style scoped>

</style>