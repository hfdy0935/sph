// 提交购物车后的数据
// cSpell:ignore pinia
import { reactive } from 'vue'
import { defineStore } from 'pinia'

export const useTradeStore = defineStore('tradeStore', () => {
    // 提交购物车的商品
    let shoppingCartSelected: any = reactive([]);
    function changeShoppingCartSelected(value: any){
        shoppingCartSelected.splice(0, shoppingCartSelected.length);
        value.forEach((item: number) => {
            shoppingCartSelected.push(item);
        }) 
    }
    // 提交购物车商品的索引
    let shoppingCartSelectedIndex: any = reactive([]);
    function changeShoppingCartSelectedIndex(value: any){
        shoppingCartSelectedIndex.splice(0, shoppingCartSelectedIndex.length);
        value.forEach((item: number) => {
            shoppingCartSelectedIndex.push(item);
        }) 
    }
    // 订单信息
    let orderInfo = reactive([]);
    function changeOrderInfo(value: object){
        orderInfo.splice(0, orderInfo.length);
        Object.assign(orderInfo, value);
    }

    return {
        shoppingCartSelected,
        changeShoppingCartSelected,
        shoppingCartSelectedIndex,
        changeShoppingCartSelectedIndex,
        orderInfo,
        changeOrderInfo
    }
})