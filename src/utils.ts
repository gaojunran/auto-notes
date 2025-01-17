import {load} from "@tauri-apps/plugin-store";
import {Cache} from "./types.ts";

const EXAMPLE_CACHE: Cache[] = [
    {
        id: 1,
        tags: ['数据结构', 'ICSI213'],
        duration: 3421,
        abstract: '这节课主要讲了关于栈和队列的理论知识。',
        topic: '栈和队列',
        raw_recognition: '这里应该放识别结果。'
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