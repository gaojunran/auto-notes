<template>
  <div class="flex min-h-screen">
    <!-- Sidebar -->
    <aside class="w-64 bg-gray-800 text-white m-4 rounded-2xl flex flex-col overflow-hidden">
      <div class="p-6">
        <h1 class="text-2xl font-bold">学习中心</h1>
      </div>
      <nav class="mt-2 flex-1">
        <div
            v-for="item in menuItems"
            :key="item.name"
            @click="navigateTo(item.href)"
            class="flex items-center px-6 py-3 text-gray-300 hover:bg-gray-700 hover:text-white transition-colors duration-200"
            :class="{ 'bg-gray-700 text-white': item.current }"
        >
          <component :is="item.icon" class="h-5 w-5 mr-3"/>
          {{ item.name }}
        </div>
      </nav>
      <div class="p-4">
        <button
            class="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg transition-colors duration-200"
            @click="router.push('/')">
          返回主页
        </button>
      </div>
    </aside>

    <!-- Main content -->
    <main class="flex-1 p-6 overflow-auto bg-white/5 m-4 rounded-2xl">
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue';
import {PlayCircle, BookOpen, HelpCircle, PenTool} from 'lucide-vue-next';
import {useRouter} from "vue-router";
import {useRoute} from "vue-router";

const route = useRoute();

const id = route.fullPath.split('/')[3];
const type = route.fullPath.split('/')[2];

const menuItems = ref([
  {name: '课堂回放', icon: PlayCircle, href: `/detail/recognition/${id}`, current: false},
  {name: '课堂笔记', icon: BookOpen, href: `/detail/note/${id}`, current: false},
  {name: '思考题', icon: HelpCircle, href: `/detail/thought/${id}`, current: false},
  {name: '练习题', icon: PenTool, href: `/detail/exercise/${id}`, current: false},
]);

const router = useRouter();

const navigateTo = (href) => {
  router.push(href);
  menuItems.value.forEach(item => {
    item.current = false;
  });
  (menuItems.value.find(item => item.href === href)).current = true;
}

onMounted(() => {
  menuItems.value.find(item => type === item.href.split('/')[2]).current = true;
})
</script>