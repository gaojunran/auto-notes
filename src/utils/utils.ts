import {ToastEventBus} from "primevue";

export const info = async (msg: string) => {
    await ToastEventBus.emit('add', { severity: "info", summary: "日志", detail: msg, life: 3000 });
}

export const success = async (msg: string) => {
    await ToastEventBus.emit('add', { severity: "success", summary: "任务成功执行", detail: msg, life: 3000 });
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