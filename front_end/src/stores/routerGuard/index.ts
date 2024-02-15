// cSpell:ignore pinia
// 保存登录和注册之前的路由信息

import { reactive } from 'vue'
import { defineStore } from 'pinia'

export const useRouterGuardStore = defineStore('routerGuardStore', () => {
    let preRouterObj: any = reactive([{name: 'home'}]);
    // 末尾新增路由历史记录
    function changePreRouterObj(newRouterObj: object){
        preRouterObj.push(newRouterObj);
    }
    // 清空
    function clearPreRouterObj(){
        preRouterObj.splice(0, preRouterObj.length - 1);
    }

    return {
        preRouterObj,
        changePreRouterObj,
        clearPreRouterObj
    }
})
