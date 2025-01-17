<script setup lang="ts">

</script>

<template>

  <Toast position="bottom-right"></Toast>


  <div class="bg-gradient-to-br from-gray-900 to-gray-800 min-h-screen">
    <RouterView v-slot="{ Component }">
      <transition name="fade">
        <component :is="Component"/>
      </transition>
    </RouterView>
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>