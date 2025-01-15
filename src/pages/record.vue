<template>
  <div class="min-h-screen flex items-center justify-center p-6">
    <div class="w-full max-w-md bg-white rounded-xl shadow-2xl p-8">
<!--      <h1 class="text-3xl font-bold text-center text-gray-800 mb-8">高级音频录制器</h1>-->

      <div v-if="!isRecording && !audioUrl" class="flex justify-center">
        <button @click="startRecording" class="bg-red-500 hover:bg-red-600 text-white font-bold py-4 px-8 rounded-full shadow-lg transition duration-300 ease-in-out flex items-center">
          <MicIcon class="w-6 h-6 mr-2" />
          开始录音
        </button>
      </div>
      <div class="text-black text-center my-8">此功能目前仅在浏览器中可用。</div>

      <div v-if="isRecording" class="flex justify-center space-x-4">
        <button @click="pauseRecording" class="bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-3 px-6 rounded-full shadow-lg transition duration-300 ease-in-out flex items-center">
          <PauseIcon v-if="!isPaused" class="w-5 h-5 mr-2" />
          <PlayIcon v-else class="w-5 h-5 mr-2" />
          {{ isPaused ? '继续' : '暂停' }}
        </button>
        <button @click="stopRecording" class="bg-red-500 hover:bg-red-600 text-white font-bold py-3 px-6 rounded-full shadow-lg transition duration-300 ease-in-out flex items-center">
          <SquareIcon class="w-5 h-5 mr-2" />
          停止
        </button>
      </div>

      <div v-if="audioUrl" class="mt-8 space-y-4">
        <audio :src="audioUrl" controls class="w-full"></audio>
        <div class="flex justify-center space-x-4">
          <button @click="uploadAudio" class="bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-6 rounded-full shadow-lg transition duration-300 ease-in-out flex items-center">
            <UploadIcon class="w-5 h-5 mr-2" />
            上传
          </button>
          <button @click="resetRecording" class="bg-gray-500 hover:bg-gray-600 text-white font-bold py-3 px-6 rounded-full shadow-lg transition duration-300 ease-in-out flex items-center">
            <RefreshCwIcon class="w-5 h-5 mr-2" />
            重新录制
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// TODO: 实现本地录音功能，可能需要与Rust进行交互

import { ref, onUnmounted } from 'vue'
import { MicIcon, PauseIcon, PlayIcon, SquareIcon, UploadIcon, RefreshCwIcon } from 'lucide-vue-next'

const isRecording = ref(false)
const isPaused = ref(false)
const audioUrl = ref(null)
let mediaRecorder = null
let audioChunks = []

const startRecording = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder = new MediaRecorder(stream)

    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data)
    }

    mediaRecorder.onstop = () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/wav' })
      audioUrl.value = URL.createObjectURL(audioBlob)
      isRecording.value = false
      isPaused.value = false
    }

    mediaRecorder.start()
    isRecording.value = true
  } catch (error) {
    console.error('Error accessing microphone:', error)
    alert('无法访问麦克风。请确保您已授予必要的权限。')
  }
}

const pauseRecording = () => {
  if (isPaused.value) {
    mediaRecorder.resume()
  } else {
    mediaRecorder.pause()
  }
  isPaused.value = !isPaused.value
}

const stopRecording = () => {
  mediaRecorder.stop()
  mediaRecorder.stream.getTracks().forEach(track => track.stop())
}

const uploadAudio = () => {
  // 这里添加上传逻辑
  console.log('上传音频文件')
}

const resetRecording = () => {
  audioUrl.value = null
  audioChunks = []
}

onUnmounted(() => {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop()
    mediaRecorder.stream.getTracks().forEach(track => track.stop())
  }
})
</script>