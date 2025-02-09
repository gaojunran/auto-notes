import {onMounted, ref} from "vue";
import {getIsBeta, getIsEnglish} from "./cache.ts";

export const useBeta = () => {
    const isBeta = ref(true);

    const beta = (yes: string, no: string) => {
        return isBeta.value? yes : no;
    }

    onMounted(async () => {
        isBeta.value = await getIsBeta();
    })

    return { beta, isBeta }
}