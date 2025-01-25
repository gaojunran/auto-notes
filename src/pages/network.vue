<script setup lang="ts">
import {use} from 'echarts/core';
import {GraphChart} from 'echarts/charts';
import {TooltipComponent, LegendComponent} from 'echarts/components';
import {LabelLayout} from 'echarts/features';
import {CanvasRenderer} from 'echarts/renderers';
import type {ComposeOption} from 'echarts/core';
import type {GraphSeriesOption} from 'echarts/charts';

import type {
  TooltipComponentOption,
  LegendComponentOption
} from 'echarts/components';
import {readAllCache} from "../utils/cache.ts";
import {computed, onMounted, provide, ref} from "vue";
import VChart, {THEME_KEY} from 'vue-echarts';
import {getNetwork, NetworkRequest, NetworkResponse} from "../apis.ts";
import request from "../request.ts";
import {Lecture} from "../types.ts";

use([
  TooltipComponent,
  LegendComponent,
  GraphChart,
  CanvasRenderer,
  LabelLayout
]);

provide(THEME_KEY, 'dark');

type EChartsOption = ComposeOption<
    | TooltipComponentOption
    | LegendComponentOption
    | GraphSeriesOption
>;

const data = ref<NetworkResponse>({});
const chartOptions = ref<EChartsOption>();
const chart = ref<any>();

const getResponse = async () => {
  const caches = await readAllCache()
  const requests = caches.filter(cache => cache.points && cache.points.length > 0)
      .map(cache => {
        return {
          id: cache.id,
          topic: cache.topic,
          points: cache.points.map(point => {
            return {name: point.name, importance: point.importance}
          })
        } as Lecture;
      });
  return await getNetwork({lectures: requests} as NetworkRequest);
}


onMounted(async () => {
  data.value = await getResponse();
  console.log(data.value)
  chartOptions.value = {

        tooltip: {},
        legend: [
          {
            data: data.value.categories?.map(category => category.name)
          }
        ],
        series: [{
          name: '节点',
          type: 'graph',
          layout: 'force',
          roam: true,
          draggable: true,
          label: {
            show: true,
            position: 'right'
          },
          data: data.value.nodes?.map(node => {
            return {
              id: node.idx,
              name: node.name,
              symbolSize: node.size * 10,
              category: node.category,
              value: node.importance,
            }
          }),
          links: data.value.links?.map(link => {
            return {
              source: link.source,
              target: link.target,
              lineStyle: {
                width: link.weight * 2,
              }
            }
          }),
          categories: data.value.categories?.map(category => {
            return {
              name: category.name,
            }
          }),
          force: {
            initLayout: 'circular',
            repulsion: 500
          }
        }]
      }
  console.log(chartOptions.value)
    chart.value.setOption(chartOptions.value);
  }
);


</script>

<template>
  <div id="container">
    <v-chart id="chart" ref="chart" :options="chartOptions" auto-resize/>
  </div>

</template>

<style scoped>
#chart {
  height: 100vh;
  width: 100%;
  position: relative;
  z-index: 1;
}

#container {
  height: 100vh;
  width: 100%;
}
</style>