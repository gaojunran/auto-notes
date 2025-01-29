import {fetch} from "@tauri-apps/plugin-http"
import { info } from "@tauri-apps/plugin-log"

const BASE_URL = 'http://localhost:5100'

class HttpError extends Error {
    constructor(public message: string, public cause: Response) {
        super(message)
        this.cause = cause
    }
}

const request = async (url: string, method: string = 'GET', json?: object, body?: any, headers?: HeadersInit) => {
    info(JSON.stringify({url, method, json, body, headers}))
    try {
        let init = {
            method: method
        }
        init['headers'] = json ? {
            'Content-Type': 'application/json',
        } : headers;
        init['body'] = json ? JSON.stringify(json) : body

        const response = await fetch(BASE_URL + url, init)
        if (!response.ok) {
            throw new HttpError(`HTTP Error: status: ${response.status}, statusText: ${response.statusText}`, await response.json())
        } else {
            info(JSON.stringify(response))
            return await response.json()
        }
    } catch (error) {
        throw error
    }
}

export default request