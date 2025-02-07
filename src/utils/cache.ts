import {load, Store} from "@tauri-apps/plugin-store";
import {Cache, NodeLink} from "../types.ts";
import {EChartsOption} from "echarts";

const EXAMPLE_CACHE: Cache[] = [
    {
        id: 1,
        tags: ['Discrete Structures', 'ICSI210'],
        duration: 3421,
        abstract: 'The lecture includes the language of propositions and its applications, and logical equivalents of propositions.',
        topic: 'Propositional Logic',
        raw_recognition: [
                {
                    "start": 132,
                    "end": 137,
                    "text": "Well, for this section, we will talk about logics and proofs, which is the core of the course."
                },
                {
                    "start": 137,
                    "end": 142,
                    "text": "When it comes to the first concept propositions, it is a declarative sentence that is either true or false. "
                },
                {
                    "start": 143,
                    "end": 150,
                    "text": "The truth value of a proposition is determined, it can be predicated from the facts or the rules of inference."
                },
                {
                    "start": 151,
                    "end": 158,
                    "text": "Here are some examples of propositions, we can learn deeper about the definition of propositions."
                },
                {
                    "start": 159,
                    "end": 166,
                    "text": "Washington, D.C., is the capital of the United States of America. This sentence follows the fact, and it's true, "
                },
                {
                    "start": 166,
                    "end": 172,
                    "text": "So we can say that it is a proposition."
                },
                {
                    "start": 173,
                    "end": 179,
                    "text": "Toronto is the capital of Canada. This sentence also follows the fact, and it's true."
                },
                {
                    "start": 180,
                    "end": 186,
                    "text": "1 + 0 = 1. This sentence is a mathematical proposition, and it's true."
                },
                {
                    "start": 187,
                    "end": 193,
                    "text": "0 + 0 = 2. This sentence is also a mathematical proposition, and it's false."
                }
        ],
        points: [
            {
                name: 'The language of propositions',
                importance: 3,
                links: [],
                summary: "",
                subtitles: [
                    {
                        subtitle: 'Propositions',
                        md: `
# _Definition_: 

A **proposition** is a declarative sentence that is either true or false. 

# _Examples of propositions_: 
- Washington, D.C., is the capital of the United States of America.
- Toronto is the capital of Canada.
- 1 + 0 = 1
- 0 + 0 = 2
# _Examples of non-propositions_: 
- Sit down!
- What time is it?
- $x + 1 = 2$
- $x + y = z$
`,
                        raw_recognition: [{start: 132}]
                    },
                    {
                        subtitle: "Propositional logic",
                        md: `
# _Propositional Variables_
- Represented by \`p, q, r, s, ...\`.

# _Constant Propositions_
- **T**: A proposition that is always true (tautology).
- **F**: A proposition that is always false (contradiction).

# _Compound Propositions_
Built using logical connectives and other propositions. Key connectives include:

1. **Negation**  
   Symbol: \`¬\`  
   Example: \`¬p\` (not p).

2. **Conjunction**  
   Symbol: \`∧\`  
   Example: \`p ∧ q\` (p and q).

3. **Disjunction**  
   Symbol: \`∨\`  
   Example: \`p ∨ q\` (p or q).

4. **Implication**  
   Symbol: \`→\`  
   Example: \`p → q\` (if p, then q).

5. **Biconditional**  
   Symbol: \`↔\`  
   Example: \`p ↔ q\` (p if and only if q).
                        `,
                        raw_recognition: [{start: 303}]
                    },
                    {
                        subtitle: "Truth Tables For Compound Propositions",
                        md: "...",
                        raw_recognition: [{start: 400}]
                    }
                ]
            },
            {
                name: "Applications of Propositional Logic",
                importance: 2,
                links: [],
                summary: "",
                subtitles: [
                    {
                        subtitle: "Translating English to Propositional Logic",
                        md: "...",
                        raw_recognition: [{start: 500}]
                    },
                    {
                        subtitle: "Boolean Searches",
                        md: "...",
                        raw_recognition: [{start: 600}]
                    },
                    {
                        subtitle: "Logic Circuits",
                        md: "...",
                        raw_recognition: [{start: 700}]
                    },
                ]
            }
        ]
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
    const pointIndex = cache?.points?.findIndex(p => p.name === pointName);
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