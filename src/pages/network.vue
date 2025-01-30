<script setup lang="ts">
import {use} from 'echarts/core';
import {GraphChart} from 'echarts/charts';
import {TooltipComponent, LegendComponent} from 'echarts/components';
import {LabelLayout} from 'echarts/features';
import {CanvasRenderer} from 'echarts/renderers';
import type {ComposeOption,} from 'echarts/core';
import type {GraphSeriesOption,} from 'echarts/charts';
import type {
  TooltipComponentOption,
  LegendComponentOption
} from 'echarts/components';
import {
  getShouldUpdateChart,
  getUserLinkCache,
  loadChartCache,
  readAllCache,
  setShouldUpdateChart,
  updateChartCache
} from "../utils/cache.ts";
import {onMounted, provide, ref} from "vue";
import VChart, {THEME_KEY} from 'vue-echarts';
import {getNetwork, NetworkRequest, NetworkResponse} from "../apis.ts";
import {Lecture, NodeLink} from "../types.ts";
import {useRouter} from "vue-router";
import Loading from "../components/Loading.vue";
import { useJump } from '../utils/useJump.ts';

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

const data = ref<NetworkResponse>();
const chartOptions = ref<any>(null);
const chart = ref<any>();

const loading = ref(false);

const router = useRouter();

const jump = useJump();

const getResponse = async () => {
  const caches = await readAllCache()
  const requests = caches.filter(cache => cache.points && cache.points.length > 0)
    .map(cache => {
      return {
        id: cache.id,
        topic: cache.topic,
        points: cache.points!!.map(point => {
          return {name: point.name, importance: point.importance}
        })
      } as Lecture;
    });
  return await getNetwork({lectures: requests} as NetworkRequest);
}

const handleClick = async (params: any) => {
  if (params?.data?.route) {
    if (params?.data?.route.point) {
      await jump.jumpToNote(params.data.route.id, params.data.route.point);
    } else {
      await jump.jumpToNote(params.data.route.id);
    }
  }
}

onMounted(async () => {
  const userLinks = await getUserLinkCache();
  if (!await getShouldUpdateChart()) {
    chartOptions.value = await loadChartCache();
    (chartOptions.value.series?.[0]?.links as NodeLink[]).push(...userLinks)
    chart.value.setOption(chartOptions.value);
    return;
  }
  loading.value = true;
  data.value = await getResponse();
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
          // id: node.idx,
          name: node.name,
          symbolSize: node.size * 10,
          category: node.category,
          value: node.size,
          route: node.route,
        }
      }),
      links: data.value.links?.map(link => {
        return {
          source: link.source,
          target: link.target,
          weight: link.weight, // extra
          isUserGenerated: false,  // extra
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
  } as EChartsOption;

  // 先更新缓存，再加入用户定义的链接
  await updateChartCache(chartOptions.value);
  (chartOptions.value.series?.[0]?.links as NodeLink[]).push(...userLinks);

  chart.value.setOption(chartOptions.value);
  loading.value = false;
  await setShouldUpdateChart(false);
});


</script>

<template>
  <div>
    <Loading v-model="loading" title="正为您生成知识网络……" subtitle="耗时将取决于您的历史课程数量，请耐心等待。"></Loading>
    <div class="w-full h-screen">
      <v-chart id="chart" ref="chart" @click="handleClick" :options="chartOptions" auto-resize/>
    </div>
    <Button class="!fixed !top-4 !left-4" severity="secondary" icon="pi pi-home" rounded @click="router.push('/')"></Button>
  </div>
  
  

</template>

<style scoped>
#chart {
  height: 100vh;
  width: 100%;
  position: relative;
}
</style>