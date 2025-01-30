<script setup lang="ts">
import {success} from "../utils/utils.ts";
import {onMounted, ref, watch} from "vue";
import Loading from "../components/Loading.vue";
import {bootService, installUv} from "../utils/serviceDeps.ts";
import {clearCache, getFakeService, setFakeService} from "../utils/cache.ts";
import {useRouter} from "vue-router";
import ToggleSwitch from 'primevue/toggleswitch';
import { info } from "../utils/utils.ts"

const loading = ref(false)
const router = useRouter()

const isFakeService = ref(false);

watch(isFakeService, async (newValue, _) => {
    await setFakeService(newValue);
    await info("伪造服务端模式已" + (newValue? "开启" : "关闭") + "！")
})

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

onMounted(async () => {
  isFakeService.value = await getFakeService();
})
</script>

<template>
  <div>
    <Loading v-model="loading" title="操作中，请稍后..."></Loading>
    <div class="rounded flex items-center justify-center min-h-screen">
      <div class="p-8 bg-black/20 rounded-lg flex flex-col">
        <div class="text-center mb-4 font-bold">
          以下设置请在指引下、慎重考虑后进行操作
        </div>
        <div class="flex items-center mb-4">
          <div class="text-white">首次进入软件时，如果依赖安装失败，可尝试：</div>
          <Button severity="success" icon="pi pi-wrench" label="重新安装uv" size="small" @click="reinstallUv" />
        </div>
        <div class="flex items-center mb-4">
          <div class="text-white">进入软件时，如果服务端启动失败，可尝试：</div>
          <Button severity="success" icon="pi pi-undo" label="重新启动服务端" size="small" @click="rebootService" />
        </div>
        <div class="flex items-center mb-4">
          <div class="text-white">若进行了某些错误操作，可尝试：</div>
          <Button severity="warn" icon="pi pi-trash" label="清空缓存" size="small" @click="clearAllCache" />
        </div>
        <div class="flex items-center mb-4">
          <div class="text-white mr-4">伪造服务端模式</div>
          <ToggleSwitch v-model="isFakeService"></ToggleSwitch>
        </div>
        <div class="flex justify-center items-center mt-2">
          <Button severity="secondary" icon="pi pi-home" label="返回主页" size="small" @click="router.push('/')" />
        </div>

      </div>
    </div>
  </div>

</template>

<style scoped>

</style>