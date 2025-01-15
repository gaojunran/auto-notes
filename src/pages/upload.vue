<script setup lang="ts">

</script>

<template>
  <div class="w-full min-h-screen flex items-center justify-center">
    <div>
      <FileUpload
          choose-label="选择音频文件" upload-label="上传" cancel-label="取消"
          accept="audio/*"
          :pt="{
              fileThumbnail: {
                class: 'hidden'
              },
              file: {
                class: 'bg-white/10 rounded'
              }
          }"
          :multiple="false"
      />

    </div>

  </div>

</template>

<style scoped>

</style>