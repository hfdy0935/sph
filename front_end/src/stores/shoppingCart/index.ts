import { changeShoppingCart } from '../../api/index';
// 购物车数据保存在后端了，这个用不到了
import { reactive } from 'vue'
import { defineStore } from 'pinia'
import { useUUID } from '@/utils/uuid_token'

export const useShoppingCartStore = defineStore('shoppingCartStore',()=>{
    let shoppingCart: any = reactive([]);
    let uuid_token = useUUID();
    
    
    // 添加到购物车
    function addGoodsToShoppingCart(goods: any){
        // 首次添加
        if (shoppingCart.length === 0) {
            console.log(uuid_token);
            console.log('首次添加')
            shoppingCart.push(Object.assign(goods,{uuid_token}));
        } else {
            // 相同商品
            for (let item of shoppingCart) {
                if (JSON.stringify(item.goodsInfo) === JSON.stringify(goods.goodsInfo)) {
                    item.submitInfo.buyNum += item.submitInfo.buyNum;
                    item.submitInfo.totalPrice += item.goodsInfo.price;
                    item.submitInfo.submitTime = item.submitInfo.submitTime.concat(goods.submitInfo.submitTime);
                    return
                } 
            }
            // 不同商品、同一商品不同售卖属性
            shoppingCart.push(Object.assign(goods,{uuid_token}));
        }
    }
    // 清空购物车
    function clearShoppingCart(){
        shoppingCart.forEach((_:any,index:number)=>{
            delete shoppingCart[index]
        })
    }
    

    return {
        shoppingCart,
        addGoodsToShoppingCart,
        clearShoppingCart
    }
})