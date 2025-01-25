import {load} from "@tauri-apps/plugin-store";
import {Cache} from "../types.ts";
import {EChartsOption} from "echarts";

const EXAMPLE_CACHE: Cache[] = [
    {
        id: 1,
        tags: ['数据结构', 'ICSI213'],
        duration: 3421,
        abstract: '这节课主要讲了关于栈和队列的理论知识。',
        topic: '栈和队列',
        raw_recognition: [
            {start: 0, end: 12, text: '这节课主要讲了关于栈和队列的理论知识。'},
            {start: 13, end: 25, text: '栈和队列是两种基本的数据结构。'},
            {start: 26, end: 39, text: '栈是一种线性数据结构，它遵循后进先出（LIFO）的原则。'},
            {start: 40, end: 52, text: '队列是一种线性数据结构，它遵循先进先出（FIFO）的原则。'},
            {start: 53, end: 65, text: '栈和队列的操作主要包括入栈、出栈、查看栈顶元素、判断栈是否为空、判断队列是否为空。'},
            {
                start: 66,
                end: 78,
                text: '栈和队列的应用主要包括表达式求值、函数调用栈、浏览器前进后退、打印机打印任务队列等。'
            },
            {start: 79, end: 91, text: '栈和队列的实现主要基于数组和链表。'},
            {start: 92, end: 104, text: '栈和队列的分析主要基于时间复杂度、空间复杂度、稳定性、并发性等。'},
            {
                start: 105,
                end: 117,
                text: '栈和队列的应用举例主要包括进制转换、括号匹配、表达式求值、函数调用栈、浏览器前进后退、打印机打印任务队列等。'
            },
        ],
    }
];
const store = await load('store.json', {autoSave: true});
export const readAllCache = async () => {
    let cache = await store.get<Cache[]>('cache');
    if (!cache || cache.length === 0) {
        cache = EXAMPLE_CACHE;
        await store.set('cache', cache);
    }
    console.log('cache', cache)
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
}

export const getShouldUpdateChart = async () => {
    return await store.get<boolean>('shouldUpdateChart') || true;
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