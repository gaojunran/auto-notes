<template>
  <div class="flex min-h-screen bg-black/30">
    <!-- Sidebar -->
    <aside class="w-40 bg-gray-800 text-white m-4 rounded-2xl flex flex-col overflow-hidden">
      <div class="p-6">
        <h1 class="text-2xl font-bold">学习中心</h1>
      </div>
      <nav class="mt-2 flex-1">
        <div
            v-for="item in menuItems"
            :key="item.name"
            @click="router.push(item.href)"
            class="flex items-center px-6 py-3 text-gray-300 hover:bg-gray-700 hover:text-white transition-colors duration-200"
            :class="{ 'bg-gray-700 text-white': item.current }"
        >
          <component :is="item.icon" class="h-5 w-5 mr-3"/>
          {{ item.name }}
        </div>
      </nav>
      <div class="p-4">
        <button
            class="w-full bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded-lg transition-colors duration-200"
            @click="router.push('/')">
          返回主页
        </button>
      </div>
    </aside>

    <!-- Main content -->
    <main class="flex-1 px-6 pt-6 pb-2 overflow-auto bg-white/2 m-4 rounded-2xl">
      <RouterView v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component"/>
        </transition>
      </RouterView>
    </main>
  </div>
</template>

<script setup>
import {computed, onMounted, ref} from 'vue';
import {PlayCircle, BookOpen, HelpCircle, PenTool, LinkIcon} from 'lucide-vue-next';
import {useRouter} from "vue-router";
import {useRoute} from "vue-router";

const route = useRoute();

const id = route.params.id;
const type = computed(() => route.fullPath.split('/')[2]);

const menuItems = ref([
  {name: '课堂回放', icon: PlayCircle, href: `/detail/recognition/${id}`},
  {name: '课堂笔记', icon: BookOpen, href: `/detail/note/${id}/overview`},
  {name: '建立关系', icon: LinkIcon, href: `/detail/connect`},
  // {name: '练习题', icon: PenTool, href: `/detail/exercise/${id}`},
]);

menuItems.value.forEach(item => {
  item.current = computed(() => item.href.split('/')[2] === type.value)
});


const router = useRouter();
</script>