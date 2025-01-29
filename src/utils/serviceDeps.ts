import {Ref} from "vue";
import {resolveResource} from "@tauri-apps/api/path";
import {Command} from "@tauri-apps/plugin-shell";
import {testConnection} from "../apis.ts";
import {platform} from "@tauri-apps/plugin-os";
import {success} from "./utils.ts";
import {load} from "@tauri-apps/plugin-store";
import {info} from "@tauri-apps/plugin-log"

const store = await load('store.json', {autoSave: true});

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
        info(rs1.stdout)
    }

    const rs2 = await Command.create(script[0], script.slice(1), {cwd: apiPath}).execute()
    if (rs2.code !== 0) {
        loading.value = false
        throw new Error(rs2.stderr)
    }
    console.log(rs2.stdout)
    info(rs2.stdout)
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

    command.on('close', (data) => {
        console.log(`command finished with code ${data.code} and signal ${data.signal}`)
    });

    command.on('error', (err) => {
        throw new Error(`command error: "${err}"`);
    });

    command.stdout.on('data', line => {
        console.log(`command stdout: "${line}"`);
        info(line);
    });
    
    command.stderr.on('data', line => {
        throw new Error(`command stderr: "${line}"`);
    });

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