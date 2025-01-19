
import {useRouter} from "vue-router";

export function useJump() {
  const router = useRouter();

  const jumpToLevelOne = async (id: number, name: string) => {
    await router.push({path: `/detail/note/${id}`, query: {point: name}})
  }

  const jumpToRecognition = async (id: number, start: number) => {
    await router.push({path: `/detail/recognition/${id}`, hash: `time-${start}`})
  }

  return {jumpToLevelOne, jumpToRecognition}
}
