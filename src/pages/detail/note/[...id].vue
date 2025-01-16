<script setup lang="ts">
import {getNote, NoteRequest} from "../../../apis.ts";
import {defineComponent, onMounted, ref} from "vue";
//@ts-ignore
import MarkDown from "vue3-markdown-it";

const note = ref("");

onMounted(async () => {
  const response = await getNote({
    topic: "人工智能",
    raw_recognition: "..."
  });
  note.value = response.notes;
});

</script>

<template>
  <div>笔记页</div>
  <div id="md">
    <MarkDown :source="note"></MarkDown>
  </div>
</template>

<style>
#md h1 {
  margin-top: 16px;
  margin-bottom: 16px;
  font-size: 24px;
  color: lightblue;
}

#md h2 {
  margin-top: 16px;
  margin-bottom: 8px;
  font-size: 20px;
  color: lightblue;
}

</style>