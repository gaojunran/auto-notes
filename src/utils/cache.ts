import {load, Store} from "@tauri-apps/plugin-store";
import {Cache, NodeLink} from "../types.ts";
import {EChartsOption} from "echarts";

const EXAMPLE_CACHE: Cache[] = [
    {
        id: 12345677,
        tags: ['离散结构', 'ICSI210'],
        duration: 3421,
        abstract: '这节课主要讲了关于布尔代数的知识。',
        topic: '布尔代数',
        raw_recognition: [
                {
                    "start": 0,
                    "end": 12,
                    "text": "什么是布尔值？"
                },
                {
                    "start": 13,
                    "end": 25,
                    "text": "布尔值有什么用？"
                },
                {
                    "start": 26,
                    "end": 30,
                    "text": "布尔值有哪两种？"
                },
                {
                    "start": 31,
                    "end": 40,
                    "text": "什么是命题真值？"
                },
                {
                    "start": 41,
                    "end": 50,
                    "text": "什么是真值表？"
                },
                {
                    "start": 51,
                    "end": 60,
                    "text": "真值表有什么用？"
                }
        ],
    }
];

const store: Store = await load('store.json', {autoSave: true});

export const readAllCache = async () => {
    let cache = await store.get<Cache[]>('cache');
    if (!cache || cache.length === 0) {
        cache = EXAMPLE_CACHE;
        await store.set('cache', cache);
    }
    return cache;
}
export const readCache = async (id: number) => {
    const cache = await readAllCache();
    const result = cache.find(c => c.id === id);
    if (!result) {
        throw new Error('Cache not found');
    }
    return result;
}
export const updateCache = async (id: number, kv: object) => {
    const cache = await readAllCache();
    const index = cache.findIndex(c => c.id === id);
    if (index === -1) {
        throw new Error('Cache not found');
    }
    cache[index] = {...cache[index], ...kv};
    await store.set('cache', cache);
    await setShouldUpdateChart(true); // Lazy update，每次仅在点击查看图表的时候才需要更新
}

export const updatePointCache = async (id: number, pointName: string, kv: object) => {
    console.log('updatePointCache', id, pointName, kv);
    const cache = await readCache(id);
    let point = cache?.points?.find(p => p.name === pointName);
    const pointIndex = cache?.points?.findIndex(p => p.name === pointName) ?? -1;
    if (!point || pointIndex === -1) {
        throw new Error('Point not found');
    }
    point = {...point, ...kv};
    cache.points!![pointIndex] = point;
    await updateCache(id, {points: cache.points});
}

export const addCache = async (cache: Cache) => {
    const allCache = await readAllCache();
    if (allCache.some(c => c.id === cache.id)) {
        throw new Error('Cache with the same id already exists');
    }
    allCache.push(cache);
    await store.set('cache', allCache);
}
export const deleteCache = async (id: number) => {
    const cache = await readAllCache();
    const index = cache.findIndex(c => c.id === id);
    if (index === -1) {
        throw new Error('Cache not found');
    }
    cache.splice(index, 1);
    await store.set('cache', cache);
}
export const clearCache = async () => {
    await store.set('cache', []);
    await store.set('chart', null);
    await store.set('shouldUpdateChart', true);
    await store.set('userLink', []);
}

export const getShouldUpdateChart = async () => {
    return await store.get<boolean>('shouldUpdateChart') ?? true;
}

export const setShouldUpdateChart = async (shouldUpdate: boolean = true) => {
    await store.set('shouldUpdateChart', shouldUpdate);
}

export const loadChartCache = async () => {
    const cache = await store.get<EChartsOption>('chart');
    if (!cache) {
        return null;
    }
    return cache;
}

export const updateChartCache = async (cache: EChartsOption) => {
    await store.set('chart', cache);
}

export const getUserLinkCache = async () => {
    const cache = await store.get<NodeLink[]>('userLink');
    if (!cache) {
        return [];
    }
    return cache;
}

export const updateUserLinkCache = async (links: NodeLink[]) => {
    await store.set('userLink', links);
}

export const getFakeService = async () => {
    return await store.get<boolean>('fakeService') ?? false;
}

export const setFakeService = async (fake: boolean) => {
    await store.set('fakeService', fake);
}