<script setup lang="ts">
import {FileUploadUploaderEvent} from "primevue";
import {postRecord} from "../apis.ts";
import {ref} from "vue";
import Loading from "../components/Loading.vue";
import {useRouter} from "vue-router";
import {Cache} from "../types.ts";
import {addCache, setShouldUpdateChart} from "../utils/cache.ts";

const router = useRouter();
const loading = ref(false);

const handleUpload = async (event: FileUploadUploaderEvent) => {
  const file = (event.files as File[])[0];
  loading.value = true;
  const formData = new FormData();
  formData.append("file", file);
  const data = await postRecord(formData);
  console.log(data)
  loading.value = false;
  await addCache(data as Cache);
  await setShouldUpdateChart();
  await router.push(`/detail/recognition/${data.id}`)
}

</script>

<template>
  <div class="w-full min-h-screen flex items-center justify-center">
    <Button class="!fixed !top-4 !left-4" severity="secondary" icon="pi pi-home" rounded @click="router.push('/')"></Button>
    <div class="w-2/3">
      <FileUpload
          choose-label="选择音频文件" upload-label="上传" cancel-label="取消"
          accept=""
          custom-upload
          @uploader="handleUpload"
          :pt="{
              header: {
                class: 'flex items-center justify-between'
              },
              fileThumbnail: {
                class: 'hidden'
              },
              file: {
                class: 'bg-white/5 rounded'
              },
              pcUploadButton: {
                root: '!flex-1'
              },
              pcCancelButton: {
                root: '!flex-1'
              }, 
              pcChooseButton: {
                root: '!flex-1'
              }
          }"
          :multiple="false"
      >
        <template #empty>
          <div class="bg-white/5 w-full p-4 h-48 rounded flex justify-center items-center">
            <div>
              还没有选择文件，快来上传吧！
            </div>
          </div>
        </template>
      </FileUpload>
      <Loading v-model="loading" title="文件上传中，请稍等..." subtitle="耗时将取决于您上传的录音时长，请耐心等待。"></Loading>
    </div>
  </div>
</template>
