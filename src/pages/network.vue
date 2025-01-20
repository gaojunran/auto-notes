<script setup lang="ts">
import { use } from 'echarts/core';
import { GraphChart } from 'echarts/charts';
import { TooltipComponent, LegendComponent } from 'echarts/components';
import { LabelLayout } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';
import type { ComposeOption } from 'echarts/core';
import type { GraphSeriesOption } from 'echarts/charts';
import type {
  TooltipComponentOption,
  LegendComponentOption
} from 'echarts/components';
import {readAllCache} from "../utils/cache.ts";
import {onMounted} from "vue";

use([
  TooltipComponent,
  LegendComponent,
  GraphChart,
  CanvasRenderer,
  LabelLayout
]);

type EChartsOption = ComposeOption<
    | TooltipComponentOption
    | LegendComponentOption
    | GraphSeriesOption
>;

const getAllNodes = async () => {
  const caches = await readAllCache()
  const requests = caches.filter(cache => cache.points && cache.points.length > 0)
      .map(cache => {
        return {
          id: cache.id,
          topic: cache.topic,
          points: cache.points.map(point => point.name)
        }
      });
  console.log(requests)
}

onMounted(async () => {
  await getAllNodes()
});

</script>

<template>

</template>

<style scoped>

</style>