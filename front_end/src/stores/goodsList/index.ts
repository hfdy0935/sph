import { reactive,ref } from 'vue'
import { defineStore } from 'pinia'
import { useUUID } from '@/utils/uuid_token'

export const useGoodsListStore = defineStore('goodsListStore',()=>{
    // 总商品列表
    let goodsList:any = reactive({});
    // 点了某个商品后的要跳转的商品信息
    let currentGoods:any = reactive({});
    // 临时token
    let uuid_token = ref(useUUID());

    function changeGoodsList(value:object){
        Object.assign(goodsList,value);
    }

    // 从商品列表页面选择一个商品进入详情页面时触发
    function changeCurrentGoods(index:number){
        Object.assign(currentGoods, goodsList[Object.keys(goodsList)[index - 1]]);
    }

    // 详情页面选择的属性
    function changeCurrentGoodsFromDetail(obj:object){
        Object.assign(currentGoods, obj);
    }

    return {
        goodsList,
        changeGoodsList,
        currentGoods,
        changeCurrentGoods,
        uuid_token,
        changeCurrentGoodsFromDetail
    }
})