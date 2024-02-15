import { ref,reactive } from 'vue'
import { defineStore } from 'pinia'
import { reqCategoryList,reqBannerList,reqFloorList } from '@/api'

export const useHomeStore = defineStore('homeStore',() => {
    async function getCategoryList(){
        let { data } = await reqCategoryList();
        return await data
    }
    async function getBannerList(){
        let { data } = await reqBannerList();
        return await data
    }
    async function getFloorList(){
        let { data } = await reqFloorList();
        return await data
    }
    return {
        getCategoryList,
        getBannerList,
        getFloorList
    }
})
