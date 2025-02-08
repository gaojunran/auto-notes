<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { getShouldUpdateChart, getUserLinkCache, loadChartCache, readAllCache, setShouldUpdateChart, updateChartCache, updateUserLinkCache } from '../../utils/cache';
import { getNetwork, NetworkRequest, NetworkResponse } from '../../apis';
import { Lecture, NodeLink, Node } from '../../types';
import { EChartsOption } from 'echarts';
import { DataTable, Column, Dialog, Select, Rating } from 'primevue';
import Loading from '../../components/Loading.vue';
import { info } from '../../utils/utils';
import {useEnglish} from "../../utils/useEnglish.ts";

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

const { i18n } = useEnglish();

const data = ref<NetworkResponse>();

const chartOptions = ref<any>();

const nodes = computed(() => {
    return (chartOptions.value?.series?.[0]?.data?.map(node => node.name) || []) as Node[];
})

const existingLinks = computed({
  get() {
    return (chartOptions.value?.series?.[0]?.links as NodeLink[]) || [];
  },
  set(val) {
    chartOptions.value.series[0].links = val;
  }
    
})  // 大模型生成的链接

const userLinks = ref<NodeLink[]>([]); // 用户自定义的链接

const allLinks = computed(() => {
    return [...existingLinks.value, ...userLinks.value];
})

const loading = ref(false);

const isNewLinkShow = ref(false);

const sourceSelect = ref('');
const targetSelect = ref('');
const weightInput = ref(1);

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
    const link = {source, target, weight, 
      isUserGenerated: true, 
      lineStyle: { width: weight * 2, color: 'yellow' }
    } as NodeLink;

    // 更新userLink ref及缓存
    userLinks.value.push(link);
    await updateUserLinkCache(userLinks.value);

    isNewLinkShow.value = false;

}

const removeLink = async (source: string, target: string, isUserGenerated: boolean) => {
  if (isUserGenerated) {
    userLinks.value = userLinks.value.filter(link => link.source !== source || link.target !== target);
    await updateUserLinkCache(userLinks.value);
  } else {
    await info("提醒：删除由大模型生成的链接的操作可能会被覆盖！")
    existingLinks.value = existingLinks.value.filter(link => link.source !== source || link.target !== target);
    await updateChartCache(chartOptions.value);
  }
  
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
  { field: 'source', header: 'Source' },
  { field: 'target', header: 'Target' },
  { field: 'weight', header: 'Weight' },
  // { field: 'isUserGenerated', header: '※' }
]
</script>

<template>
    <div>
      <Dialog v-model:visible="isNewLinkShow" modal :style="{ width: '75%' }" header="Add a New Link...">
        <div class="flex justify-between items-center mb-4 gap-4">
          <div class="flex justify-start items-center mb-4 gap-8">
            <div>Source Node</div>
            <Select v-model="sourceSelect" :options="nodes" placeholder="Select one..."></Select>
          </div>
          <div class="flex justify-start items-center mb-4 gap-6 mr-12">
            <div>Target Node</div>
            <Select v-model="targetSelect" :options="nodes" placeholder="Select one..."></Select>
          </div>
        </div>
        <div class="flex justify-start items-center mb-4 gap-4">
          <div>Relationship Weight</div>
          <Rating v-model="weightInput"></Rating>
        </div>
        <template #footer>
          <Button icon="pi pi-save" :label="i18n('Save', '保存')" @click="saveNewLink(sourceSelect, targetSelect, weightInput)"></Button>
        </template>
        
      </Dialog>
      <Loading v-model="loading" title="正为您生成知识网络……" subtitle="耗时将取决于您的历史课程数量，请耐心等待。"></Loading>
      <div class="flex justify-between items-center mb-6 gap-4">
        <div class="font-bold text-xl dark:text-white text-black">
          {{ i18n("All Knowledge Links", "所有知识链接") }}
        </div>
        <Button :label="i18n('Add New Link', '添加新链接')" @click="isNewLinkShow = true" icon="pi pi-plus" size="small"></Button>
      </div>
        
        <DataTable :value="allLinks" removableSort :pt="{
          tableContainer: '!rounded-lg !border !border-white/10 hover:!border-white/40  !border-2 !transition', 
          bodyRow: 'dark:!bg-black/10 dark:hover:!bg-black/30 !bg-white hover:!bg-black/5'
        }">
          <Column field="source" :header="i18n('Source', '源节点')" sortable
              :pt="{ headerCell: 'dark:!bg-black/10 dark:hover:!bg-black/50 !bg-black/5 hover:!bg-black/20' }"
            />
            <Column field="target" :header="i18n('Target', '目标节点')" sortable
                    :pt="{ headerCell: 'dark:!bg-black/10 dark:hover:!bg-black/50 !bg-black/5 hover:!bg-black/20' }"
          />
            <Column field="weight" :header="i18n('Weight', '权重')" sortable
                  :pt="{ headerCell: 'dark:!bg-black/10 dark:hover:!bg-black/50 !bg-black/5 hover:!bg-black/20' }"
            >
              <template #body="slotProps">
                <Rating v-model="slotProps.data.weight" readonly></Rating>
              </template>
            </Column>
            <Column header="" :pt="{ headerCell: 'dark:!bg-black/10 dark:hover:!bg-black/50 !bg-black/5 hover:!bg-black/20' }" >
              <template #body="slotProps">
                <Button icon="pi pi-trash" outlined severity="danger"
                  @click="removeLink(slotProps.data.source, slotProps.data.target, slotProps.data.isUserGenerated)"
                  :pt="{ root: '!border-0 !text-red-500/50 hover:!text-red-500/100 !transition'
                  }"
                ></Button>
              </template>
            </Column>

            
        </DataTable>
    </div>
    
</template>
