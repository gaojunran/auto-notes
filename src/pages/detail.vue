<template>
  <div class="flex min-h-screen dark:bg-black/30 bg-gray-50">
    <!-- Sidebar -->
    <aside class="w-48 dark:bg-gray-800 bg-gray-100 text-black dark:text-white m-4 rounded-2xl flex flex-col overflow-hidden">
      <div class="p-6">
        <h1 class="text-2xl font-bold">{{ i18n('Learning Center', '学习中心') }}</h1>
      </div>
      <nav class="mt-2 flex-1">
        <div
            v-for="item in menuItems"
            :key="item.name"
            @click="router.push(item.href)"
            class="text-sm flex items-center px-6 py-3 dark:text-gray-300 dark:hover:bg-gray-700
            hover:bg-gray-200 transition-colors duration-200 dark:hover:text-white"
            :class="{ 'dark:bg-gray-700 bg-gray-200 dark:text-white text-black': item.current }"
        >
          <component :is="item.icon" class="h-5 w-5 mr-3"/>
          {{ item.name }}
        </div>
      </nav>
      <div class="p-4">
        <Button severity="secondary" icon="pi pi-home" :label="i18n('Home', '返回主页')" class="w-full"
        :pt="{ root: 'dark:!bg-black/20 dark:hover:!bg-black/50 !bg-white hover:!bg-gray-100 !transition' }"
          @click="router.push('/')"
        ></Button>
      </div>
    </aside>

    <!-- Main content -->
    <main class="flex-1 px-6 pt-6 pb-2 overflow-auto dark:bg-white/2 bg-gray-100/30 m-4 rounded-2xl">
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
import {PlayCircle, BookOpen, LinkIcon} from 'lucide-vue-next';
import {useRouter} from "vue-router";
import {useRoute} from "vue-router";
import {useEnglish} from "../utils/useEnglish.ts";

const route = useRoute();

const { i18n } = useEnglish();

const id = route.params.id;
const type = computed(() => route.fullPath.split('/')[2]);

const menuItems = ref([]);

const router = useRouter();

onMounted(() => {
  menuItems.value = [
    {name: i18n("Lecture Replay", '课堂回放'), icon: PlayCircle, href: `/detail/recognition/${id}`},
    {name: i18n('Lecture Notes', '课堂笔记'), icon: BookOpen, href: `/detail/note/${id}/overview`},
    {name: i18n('Connections', '建立联系'), icon: LinkIcon, href: `/detail/connect`}
  ];
  menuItems.value.forEach(item => {
    item.current = computed(() => item.href.split('/')[2] === type.value)
  });
})
</script>