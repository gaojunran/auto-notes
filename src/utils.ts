import {load} from "@tauri-apps/plugin-store";
import {Cache} from "./types.ts";
import {ToastEventBus} from "primevue";
import {resolveResource} from "@tauri-apps/api/path";
import {Command} from "@tauri-apps/plugin-shell";
import {testConnection} from "./apis.ts";
import {Ref} from "vue";
import {platform} from "@tauri-apps/plugin-os";

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

export const checkUvInstalled = async () => {
    if (!await store.get<Boolean>('uv')) {
        await store.set('uv', true);
        return false;
    } else {
        return true;
    }
}

export const removeUvInstalled = async () => {
    await store.set('uv', false);
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
}

export const info = async (msg: string) => {
    await ToastEventBus.emit('add', { severity: "info", summary: "日志", detail: msg, life: 3000 });
}

export const success = async (msg: string) => {
    await ToastEventBus.emit('add', { severity: "success", summary: "任务成功执行", detail: msg, life: 3000 });
}

export const installUv = async (loading: Ref<boolean>) => {
    const apiPath = await resolveResource('../api/')
    const currentPlatform = platform();
    loading.value = true
    const command = {
        windows: {
            beforeExec: '',  // Fuck you Windows
            script: 'winget install --id=astral-sh.uv -e'
        },
        macos: {
            beforeExec: 'chmod +x uv_macos.sh',
            script: './uv_macos.sh'
        },
        linux: {
            beforeExec: 'chmod +x uv_linux.sh',
            script: './uv_linux.sh'
        }
    }
    if (!command[currentPlatform]) {
        throw new Error('不支持当前平台，请手动安装`uv`!')
    }
    const script = command[currentPlatform].script.split(' ')
    const beforeExec = command[currentPlatform].beforeExec.split(' ')
    if (beforeExec[0] !== '') {
        const rs1 = await Command.create(beforeExec[0], beforeExec.slice(1), {cwd: apiPath}).execute()
        if (rs1.code !== 0) {
            loading.value = false
            throw new Error(rs1.stderr)
        }
        console.log(rs1.stdout)
    }

    const rs2 = await Command.create(script[0], script.slice(1), {cwd: apiPath}).execute()
    if (rs2.code !== 0) {
        loading.value = false
        throw new Error(rs2.stderr)
    }
    console.log(rs2.stdout)
    loading.value = false
    await success("依赖安装成功！")
}

export const bootService = async (loading: Ref<boolean>) => {
    let count = 0;
    const apiPath = await resolveResource('../api/')
    loading.value = true
    const command = await Command.create('uv', ['run', 'fastapi', 'run', 'main.py', '--port', '5100'], {
        cwd: apiPath, encoding: 'utf8', env: {
            "PYTHONIOENCODING": "utf-8",
            "PYTHONLEGACYWINDOWSSTDIO": "utf-8"
        }
    });

    command.on('close', data => {
        console.log(`command finished with code ${data.code} and signal ${data.signal}`)
    });
    command.on('error', error => console.error(`command error: "${error}"`));
    command.stdout.on('data', line => console.log(`command stdout: "${line}"`));
    command.stderr.on('data', line => console.log(`command stderr: "${line}"`));

    await command.spawn();

    const interval = setInterval(async () => {
        const isConnected = await testConnection()
        if (isConnected) {
            clearInterval(interval)
            loading.value = false
            await success("服务启动成功！")
        } else {
            count += 1
            if (count > 20) {
                clearInterval(interval)
                loading.value = false
                throw new Error("服务启动失败！")
            }
        }
    }, 2000)

}

export const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const remainingSeconds = seconds % 3600;
    const minutes = Math.floor(remainingSeconds / 60);
    const finalSeconds = remainingSeconds % 60;

    const paddedHours = String(hours).padStart(2, '0');
    const paddedMinutes = String(minutes).padStart(2, '0');
    const paddedSeconds = String(finalSeconds).padStart(2, '0');

    return `${paddedHours}:${paddedMinutes}:${paddedSeconds}`;
}

export const formatDuration = (start: number, end: number, sep = ' - ') => {
    return formatTime(start) + sep + formatTime(end);
}