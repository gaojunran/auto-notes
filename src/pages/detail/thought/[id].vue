<script setup lang="ts">
throw new Error("This page is not implemented yet.");
// import {useRoute} from "vue-router";
// import {onMounted, ref} from "vue";
// import {readCache, updateCache} from "../../../utils.ts";
// import {getThought, Question} from "../../../apis.ts";
// import Loading from "../../../components/Loading.vue";
//
// import Accordion from 'primevue/accordion';
// import AccordionPanel from 'primevue/accordionpanel';
// import AccordionHeader from 'primevue/accordionheader';
// import AccordionContent from 'primevue/accordioncontent';
//
//
// const id = Number(useRoute().params.id);
// const loading = ref(false);
// const thoughts = ref([] as Question[]);
// const current = ref(0);
// const activePanels = ref(['0']);
//
// onMounted(async () => {
//   const cache = await readCache(id);
//   if (!cache.notes) {
//     throw new Error("请先生成笔记，再来练习吧！")
//   } else if (cache.thoughts) { // use cache if exists
//     thoughts.value = cache.thoughts;
//   } else {   // request from server
//     loading.value = true;
//     const response = await getThought({
//       notes: cache.notes,
//       num: 5
//     });
//     thoughts.value = response.questions;
//     loading.value = false;
//     await updateCache(id, {thoughts: response.questions})
//   }
// });
</script>

<!--<template>-->
<!--  <Loading v-model="loading" title="正为您生成思考题..." subtitle="耗时将取决于您上传的录音时长，请耐心等待。"></Loading>-->
<!--  <Accordion :value="activePanels" multiple>-->
<!--    <AccordionPanel value="0">-->
<!--      <AccordionHeader>题 目</AccordionHeader>-->
<!--      <AccordionContent>-->
<!--        <p class="m-0">-->
<!--          {{ thoughts?.[current]?.question }}-->
<!--        </p>-->
<!--      </AccordionContent>-->
<!--    </AccordionPanel>-->
<!--    <AccordionPanel value="1">-->
<!--      <AccordionHeader>答 案</AccordionHeader>-->
<!--      <AccordionContent>-->
<!--        <p class="m-0">-->
<!--          {{ thoughts?.[current]?.answer }}-->
<!--        </p>-->
<!--      </AccordionContent>-->
<!--    </AccordionPanel>-->
<!--    <AccordionPanel value="2">-->
<!--      <AccordionHeader>解 析</AccordionHeader>-->
<!--      <AccordionContent>-->
<!--        <p class="m-0">-->
<!--          {{ thoughts?.[current]?.analysis }}-->
<!--        </p>-->
<!--      </AccordionContent>-->
<!--    </AccordionPanel>-->
<!--  </Accordion>-->
<!--  <div class="mt-4 flex justify-between items-center">-->
<!--    <Button class="flex-1 mr-20" :disabled="current === 0" @click="current&#45;&#45;; activePanels = ['0']">上一题</Button>-->
<!--    <div class="text-white/50">第 {{ current + 1 }} 题 / 共 {{ thoughts.length }} 题</div>-->
<!--    <Button class="flex-1 ml-20" :disabled="current === thoughts.length - 1" @click="current++; activePanels = ['0']">下一题</Button>-->
<!--  </div>-->

<!--</template>-->
<template>
  <div>

  </div>
</template>