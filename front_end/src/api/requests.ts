// cSpell:ignore nprogress

import axios from 'axios'
import { v4 as uuidV4 } from 'uuid'
// 这里导入不了pinia的useGoodsList中的uuid，报错说pinia还未use

import nprogress from 'nprogress'
import 'nprogress/nprogress.css'


const requests = axios.create({
    baseURL:'/api',
    timeout:12000,
});

// uuid作为游客临时id
let uuid_token: any = localStorage.getItem('UUIDTOKEN')? localStorage.getItem('UUIDTOKEN') : uuidV4();
localStorage.setItem('UUIDTOKEN', uuid_token);

// 请求拦截器
requests.interceptors.request.use(config => {
    nprogress.start();
    // 临时其他字段
    config.headers.userTmpId = uuid_token;
    return config
})
// 响应拦截器
requests.interceptors.response.use(res => {
    nprogress.done();
    return res.data;
},error => {
    console.log(error)
    return Promise.reject(new Error('出错了!'))
})

export default requests