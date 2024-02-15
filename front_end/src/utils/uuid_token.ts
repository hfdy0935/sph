// 临时游客的token，不变
import { v4 as uuidV4 } from 'uuid'

export const useUUID = () => {
    //  先尝试从本地存储获取uuid
    let uuid_token: any = localStorage.getItem('UUIDTOKEN')? localStorage.getItem('UUIDTOKEN') : uuidV4();
    localStorage.setItem('UUIDTOKEN', uuid_token);
    return uuid_token
}