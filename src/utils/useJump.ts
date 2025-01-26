
import {useRouter} from "vue-router";

export function useJump() {
  const router = useRouter();

  const jumpToNote = async (id: number, point?: string, subtitle?: string) => {
    if (point && subtitle) {
      await router.push({path: `/detail/note/${id}`, query: {point}, hash: `#${subtitle}`})
    } else if (point) {
      await router.push({path: `/detail/note/${id}`, query: {point}})
    } else {
      await router.push({path: `/detail/note/${id}/overview`})
    }
  }
  
  const jumpToRecognition = async (id: number, start: number) => {
    await router.push({path: `/detail/recognition/${id}`, hash: `time-${start}`})
  }

  return {jumpToNote, jumpToRecognition}
}
