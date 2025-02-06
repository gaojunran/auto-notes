import { createApp } from "vue";
import App from "./App.vue";
import 'primeicons/primeicons.css'
import './index.css'
import { createRouter, createWebHistory } from 'vue-router'
import { routes } from 'vue-router/auto-routes'
import PrimeVue from 'primevue/config';
import {FileUpload, Button, Menu, Toast, ToastEventBus} from "primevue";
import Aura from '@primevue/themes/aura';
import {definePreset} from "@primevue/themes";
import ToastService from 'primevue/toastservice';
import MarkDown from 'vue3-markdown-it'
import {error} from '@tauri-apps/plugin-log'

const router = createRouter({
    history: createWebHistory(),
    scrollBehavior(to) {
        if (to.hash) {
            return {
                el: to.hash,
            }
        }
    },
    routes,
})

const MyPreset = definePreset(Aura, {
    semantic: {
        primary: {
            50: '{indigo.50}',
            100: '{indigo.100}',
            200: '{indigo.200}',
            300: '{indigo.300}',
            400: '{indigo.400}',
            500: '{indigo.500}',
            600: '{indigo.600}',
            700: '{indigo.700}',
            800: '{indigo.800}',
            900: '{indigo.900}',
            950: '{indigo.950}'
        }
    }
});

const app  = createApp(App);

app.use(router)
    .use(PrimeVue, {
        theme: {
            preset: MyPreset,
            options: {
                darkModeSelector: '.app-dark',
            }
        }
    })
    .use(ToastService)
    .use(MarkDown)
    .component("FileUpload", FileUpload)
    .component("Toast", Toast)
    .component("Button", Button)
    .component("Menu", Menu)


app.config.errorHandler = async (err, _, info) => {
    console.error(err, info);  // log to console
    error(JSON.stringify({err, info}));  // log to tauri console
    await ToastEventBus.emit('add', { severity: "error", summary: "发生错误", detail: (err as { message?: string })?.message || "未知错误，请联系管理员" }); // display toast
}

app.mount("#app");
