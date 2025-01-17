<script setup lang="ts">
import {useRoute} from "vue-router";
import {onMounted, ref} from "vue";
import {readCache} from "../../../utils.ts";
import {getThought, Question} from "../../../apis.ts";

const id = Number(useRoute().params.id);
const loading = ref(false);
const thoughts = ref([] as Question[])

onMounted(async () => {
  loading.value = true;
  const cache = await readCache(id);
  if (!cache.notes) {
    throw new Error("请先生成笔记，再来练习吧！")
  } else if (cache.thoughts) { // use cache if exists
    thoughts.value = cache.thoughts;
  } else {   // request from server
    const response = await getThought({
      notes: cache.notes,
      num: 5
    });
    thoughts.value = response.questions;
  }
  loading.value = false;
});
</script>

<template>
<!--<div>思考题页</div>-->
</template>
