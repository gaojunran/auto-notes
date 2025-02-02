import { fetch } from "@tauri-apps/plugin-http"
import { info } from "@tauri-apps/plugin-log"
import { getFakeService } from "./utils/cache"

const BASE_URL = 'http://localhost:5100'

class HttpError extends Error {
    constructor(public message: string, public cause: string) {
        super(message)
        this.cause = cause
    }
}

const request = async (url: string, method: string = 'GET', json?: object, body?: any, headers?: HeadersInit) => {
    info(JSON.stringify({url, method, json, body, headers}))

    const isFakeService = await getFakeService();

    const fullUrl = BASE_URL + url + (isFakeService ? '?fake=true' : '')

    try {
        let init = {
            method: method
        }
        init['headers'] = json ? {
            'Content-Type': 'application/json',
        } : headers;
        init['body'] = json ? JSON.stringify(json) : body

        const response = await fetch(fullUrl, init)
        if (!response.ok) {
            throw new HttpError(`HTTP Error: status: ${response.status}, statusText: ${response.statusText}`, await response.text())
        } else {
            info(JSON.stringify(response))
            return await response.json()
        }
    } catch (error) {
        throw error
    }
}

export default request