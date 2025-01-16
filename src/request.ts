import axios, {AxiosError, AxiosResponse} from 'axios'
import store from '@/store'
import router from '@/router'


const instance = axios.create({
    baseURL: '/api',
    timeout: 10000  // 10 seconds
})

instance.interceptors.response.use((response: AxiosResponse) => {
    return response.data
}, (error: AxiosError) => {
    throw error
})

const request = (url: string, method?: string = 'GET', submitData: object = {}) => {
    const paramsOrData = method.toLowerCase() === 'get' ? 'params' : 'data';
    return instance({
        url,
        method,
        [paramsOrData]: submitData
    })
}

export default request