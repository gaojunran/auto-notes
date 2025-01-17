<script setup lang="ts">
import {useRoute} from "vue-router";
import {onMounted, ref} from "vue";
import {readCache} from "../../../utils.ts";
import {getExercise, Question} from "../../../apis.ts";

const id = Number(useRoute().params.id);
const loading = ref(false);
const exercises = ref([] as Question[])

onMounted(async () => {
  loading.value = true;
  const cache = await readCache(id);
  if (!cache.notes) {
    throw new Error("请先生成笔记，再来练习吧！")
  } else if (cache.exercises) { // use cache if exists
    exercises.value = cache.exercises;
  } else {   // request from server
    const response = await getExercise({
      notes: cache.notes,
      num: 5
    });
    exercises.value = response.exercises;
  }
  loading.value = false;
});
</script>

<template>
  <!--<div>思考题页</div>-->
</template>
