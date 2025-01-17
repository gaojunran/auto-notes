import axios, {AxiosError, AxiosResponse} from 'axios'


const instance = axios.create({
    baseURL: '/api',
    timeout: 10000  // 10 seconds
})

instance.interceptors.response.use((response: AxiosResponse) => {
    return response.data
}, (error: AxiosError) => {
    throw error
})

const request = (url: string, method?: string = 'GET', submitData?: any, headers?: object) => {
    const paramsOrData = method.toLowerCase() === 'get' ? 'params' : 'data';
    const config = {url, method, [paramsOrData]: submitData};
    headers && (config.headers = headers);
    return instance(config)
}

export default request