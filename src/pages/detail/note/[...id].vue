<script setup lang="ts">
import {getNote} from "../../../apis.ts";
import {onMounted, ref} from "vue";
//@ts-ignore
import MarkDown from "vue3-markdown-it";
import {useRoute} from "vue-router";
import {readCache, updateCache} from "../../../utils.ts";
import Loading from "../../../components/Loading.vue";

const note = ref("");
const id = Number(useRoute().params.id);
const loading = ref(false);

onMounted(async () => {
  const cache = await readCache(id)
  if (cache.notes) { // use cache if exists
    note.value = cache.notes;
  } else {   // request from server
    loading.value = true;
    const response = await getNote({
      topic: cache.topic,
      raw_recognition: cache!!.raw_recognition
    });
    note.value = response.notes;
    loading.value = false;
    await updateCache(id, {notes: response.notes})
  }
});

</script>

<template>
  <Loading v-model="loading" title="正为您生成笔记..." subtitle="耗时将取决于您上传的录音时长，请耐心等待。"></Loading>
  <div id="md">
    <MarkDown :source="note"></MarkDown>
  </div>
</template>

<style>
#md h1 {
  margin-bottom: 16px;
  font-size: 24px;
  font-weight: bold;
  color: lightblue;
}

#md h2 {
  margin-top: 16px;
  margin-bottom: 8px;
  font-size: 20px;
  color: lightblue;
}

</style>