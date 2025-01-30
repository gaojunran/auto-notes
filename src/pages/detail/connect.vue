<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { getShouldUpdateChart, getUserLinkCache, loadChartCache, readAllCache, setShouldUpdateChart, updateChartCache, updateUserLinkCache } from '../../utils/cache';
import { getNetwork, NetworkRequest, NetworkResponse } from '../../apis';
import { Lecture, NodeLink, Node } from '../../types';
import { EChartsOption } from 'echarts';
import { DataTable, Column } from 'primevue';

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


const data = ref<NetworkResponse>();

const chartOptions = ref<any>();

const nodes = computed(() => {
    return (chartOptions.value?.series?.[0]?.data || []) as Node[];
})

const existingLinks = computed(() => {
    return (chartOptions.value?.series?.[0]?.links as NodeLink[]) || [];
})  // 大模型生成的链接

const userLinks = ref<NodeLink[]>([
    {
        source: '真值表',
        target: '另一个topic',
        weight: 3,
        isUserGenerated: true,
    }
]); // 用户自定义的链接

const allLinks = computed(() => {
    return [...existingLinks.value, ...userLinks.value];
})

const loading = ref(false);

const saveNewLink = async (source: string, target: string, weight: number) => {
    if (existingLinks.value.some(link => (link.source === source && link.target === target) || (link.source === target && link.target === source))) {
        throw new Error('知识点链接已存在！');
    }

    if (userLinks.value.some(link => (link.source === source && link.target === target) || (link.source === target && link.target === source))) {
        throw new Error('知识点链接已存在！');
    }

    if (source === target) {
        throw new Error('源节点和目标节点不能相同');
    }
    const link = {source, target, weight, isUserGenerated: true} as NodeLink;

    // 更新userLink ref及缓存
    userLinks.value.push(link);
    await updateUserLinkCache(userLinks.value);

}

onMounted(async () => {
  if (!await getShouldUpdateChart()) {
    chartOptions.value = await loadChartCache();
    return;
  }
  loading.value = true;
  data.value = await getResponse()
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
  
  await updateChartCache(chartOptions.value);
  await setShouldUpdateChart(false);

  userLinks.value = await getUserLinkCache();

  loading.value = false;
});

const columns = [
  { field: 'source', header: '源节点' },
  { field: 'target', header: '目标节点' },
  { field: 'weight', header: '权重' },
  { field: 'isUserGenerated', header: '※' }
]
</script>

<template>
    <div>
      <div class="flex justify-between items-center mb-6 gap-4">
        <div class="font-bold text-lg">所有知识点链接</div>
        <Button label="添加链接" icon="pi pi-plus" size="small"></Button>
      </div>
        
        <DataTable :value="allLinks" removableSort :pt="{
          tableContainer: '!rounded-lg !border !border-white/10 hover:!border-white/40  !border-2 !transition', 
          bodyRow: '!bg-black/10 hover:!bg-black/30'
        }">
            <Column v-for="col in columns" :field="col.field" :header="col.header" sortable
              :pt="{ headerCell: '!bg-black/10 hover:!bg-black/50' }"
            />
        </DataTable>
    </div>
    
</template>
