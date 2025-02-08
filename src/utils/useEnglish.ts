import {onMounted, ref} from "vue";
import {getIsEnglish} from "./cache.ts";

export const useEnglish = () => {
    const isEnglish = ref(true);

    const i18n = (en: string, zh: string) => {
        return isEnglish.value ? en : zh;
    }

    onMounted(async () => {
        isEnglish.value = await getIsEnglish();
    })

    return { i18n }
}