<script setup lang="ts">
  throw new Error("The page is not implemented yet.");
// import {useRoute} from "vue-router";
// import {onMounted, ref} from "vue";
// import {readCache, updateCache} from "../../../utils.ts";
// import {getExercise, Question} from "../../../apis.ts";
// import Loading from "../../../components/Loading.vue";
//
// const id = Number(useRoute().params.id);
// const loading = ref(false);
// const exercises = ref([] as Question[])
//
// onMounted(async () => {
//   const cache = await readCache(id);
//   if (!cache.notes) {
//     throw new Error("请先生成笔记，再来练习吧！")
//   } else if (cache.exercises) { // use cache if exists
//     exercises.value = cache.exercises;
//   } else {   // request from server
//     loading.value = true;
//     const response = await getExercise({
//       notes: cache.notes,
//       num: 5
//     });
//     exercises.value = response.questions;
//     loading.value = false;
//     await updateCache(id, {exercises: response.questions})
//   }
// });
  </script>

  <!--<template>-->
  <!--  <Loading v-model="loading" title="正为您生成练习题..." subtitle="耗时将取决于您上传的录音时长，请耐心等待。"></Loading>-->
  <!--</template>-->
<template>
  <div>

  </div>
</template>