import { createApp } from "vue";
import App from "./App.vue";
import 'primeicons/primeicons.css'
import './index.css'
import { createRouter, createWebHistory } from 'vue-router'
import { routes } from 'vue-router/auto-routes'
import PrimeVue from 'primevue/config';
import {FileUpload, Button, Menu, useToast, Toast} from "primevue";
import Aura from '@primevue/themes/aura';
import {definePreset} from "@primevue/themes";
import ToastService from 'primevue/toastservice';

const router = createRouter({
    history: createWebHistory(),
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
            preset: MyPreset
        }
    })
    .use(ToastService)
    .component("FileUpload", FileUpload)
    .component("Toast", Toast)
    .component("Button", Button)
    .component("Menu", Menu)


app.config.errorHandler = (err, vm, info) => {
    const toast = useToast();
    toast.add({severity: "error", summary: "发生错误", detail: err.message})
    console.log(err, vm, info)
}

app.mount("#app");
