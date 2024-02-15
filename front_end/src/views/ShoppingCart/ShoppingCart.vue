<template>
  <div class="cart">
    <h4>全部商品</h4>
    <div class="cart-main">
      <div class="cart-th">
        <div class="cart-th1">全部</div>
        <div class="cart-th2">商品</div>
        <div class="cart-th3">配置</div>
        <div class="cart-th4">单价（元）</div>
        <div class="cart-th5">数量</div>
        <div class="cart-th6">小计（元）</div>
        <div class="cart-th7">操作</div>
      </div>
      <div v-show="!shoppingCartInfo.length" class="shoppingCartEmpty">购物车空空如也，快去选购吧~</div>
      <div class="cart-body">
        <ul class="cart-list" v-for="(goods,index) of shoppingCartInfo" :key="index">
          <li class="cart-list-con1">
            <input type="checkbox" name="chk_list" :checked="isChecked[index]" @change="checkedEvent(index)">
          </li>
          <li class="cart-list-con2">
            <img :src="goods.goodsInfo.defaultImg">
            <div class="item-msg">{{ goods.goodsInfo.title }}</div>
          </li>
          <li class="cart-list-con3">
            <div class="item-txt">{{ goods.goodsInfo.color }}</div>
            <div class="item-txt">{{ goods.goodsInfo.memory }}</div>
            <div class="item-txt">{{ goods.goodsInfo.version }}</div>
            <div class="item-txt">{{ goods.goodsInfo.way }}</div>
          </li>
          <li class="cart-list-con4">
            <span class="price">{{ goods.submitInfo.price }}</span>
          </li>
          <li class="cart-list-con5">
            <a @click="reduceOneGoods(index)" class="minus">-</a>
            <input 
            autocomplete="off" 
            type="text" 
            class="itxt" 
            v-model="goods.submitInfo.buyNum"
            @input="inputOneGoods(index)"
            >
            <a @click="addOneGoods(index)" class="plus">+</a>
          </li>
          <li class="cart-list-con6">
            <span class="sum">{{ goods.submitInfo.price * goods.submitInfo.buyNum }}</span>
          </li>
          <li class="cart-list-con7">
            <a @click="deleteOneGoods(index)" class="sindelet">删除</a>
            <br>
            <a href="#none" class="sindelet">收藏</a>
          </li>
        </ul>
      </div>
    </div>
    <div class="cart-tool" v-show="shoppingCartInfo.length">
      <div class="select-all">
        <label>
          <input class="chooseAll" type="checkbox" @click="checkAllEvent" ref="checkAll">
          <span>全选</span>
        </label>
      </div>
      <div class="option">
        <a @click="deleteSelectedGoods">删除选中的商品</a>
        <Teleport to="body">
          <div class="mask" v-show="isDeleteSelectedGoodsTipShow">
            <div class="dialog">
              <h3>确定要删除所选商品吗？</h3>
              <div class="btns">
                <button @click="deleteGoods">确定</button>
                <button @click="cancelDeleteGoods">取消</button>
              </div>
            </div>
          </div>
        </Teleport>
        <a href="#none">移到我的关注</a>
        <a href="#none">清除下柜商品</a>
      </div>
      <div class="money-box">
        <div class="chosed">已选择
          <span>{{ checkedGoodsNum }}</span>件商品</div>
        <div class="sumprice">
          <em>总价（不含运费） ：</em>
          <i class="summoney">{{ checkedGoodsTotalPrice }}</i>
        </div>
        <div class="sumbtn">
          <a class="sum-btn" @click="goToTrade">结算</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts" name="ShoppingCart">
  import { ref,reactive,onMounted,computed,toRaw } from 'vue'
  import { storeToRefs } from 'pinia'
  import { useRoute,useRouter } from 'vue-router'

  import { getShoppingCart,changeShoppingCart,deleteShoppingCart } from '@/api'
  import { useUserStore } from '@/stores/user'
  import { useTradeStore } from '@/stores/trade'


  // 购物车列表
  let shoppingCartInfo: any = reactive([]);
  // 是否勾选
  let isChecked: any = reactive([]);
  let { userName } = storeToRefs(useUserStore()); 
  // 挂载时获取初始购物车数据
  onMounted(async()=>{
    Object.assign(shoppingCartInfo, await getShoppingCart({'userName': userName.value}));  
    Object.assign(isChecked, new Array(shoppingCartInfo.length).fill(false));
  })
  // 有更新时重新获取购物车数据
  // onUpdated(async()=>{
  //   Object.assign(shoppingCartInfo, await getShoppingCart());
  //   Object.assign(isChecked, new Array(shoppingCartInfo.length).fill(false));
  // })
  

  // 更新本地商品数量和总价，并发送请求
  async function watchShoppingCartInfo(index: number){
    shoppingCartInfo[index].submitInfo.totalMoney = shoppingCartInfo[index].submitInfo.buyNum * shoppingCartInfo[index].submitInfo.price;
    // 给后端发送请求更新购物车
    return await changeShoppingCart(index, shoppingCartInfo[index], userName.value);
  }
  // 减一个商品的数量
  async function reduceOneGoods(index: number){
    if (shoppingCartInfo[index].submitInfo.buyNum <= 1) return
    shoppingCartInfo[index].submitInfo.buyNum--;
    await watchShoppingCartInfo(index);
  }
  // 输入一个商品的数量
  async function inputOneGoods(index: number){
    // 如果输入非0-9的数字，则替换完之后直接返回，不发送请求
    if (shoppingCartInfo[index].submitInfo.buyNum.match(/[^0-9]/)){
      shoppingCartInfo[index].submitInfo.buyNum = shoppingCartInfo[index].submitInfo.buyNum.replace(/[^0-9]/,''); // 过滤
      return
    }
    // 如果都删了，则显示为0
    if (shoppingCartInfo[index].submitInfo.buyNum === '') {
      shoppingCartInfo[index].submitInfo.buyNum = 0;
    }
    // 判断是否是都是0且至少出现两次的字符串
    shoppingCartInfo[index].submitInfo.buyNum = /^0{2,}$/.test(shoppingCartInfo[index].submitInfo.buyNum)? 0 : shoppingCartInfo[index].submitInfo.buyNum;
    // 判断是否以一个0开头，后面是其他数字
    if (/^0\d+/.test(shoppingCartInfo[index].submitInfo.buyNum)){
      shoppingCartInfo[index].submitInfo.buyNum = shoppingCartInfo[index].submitInfo.buyNum.replace(/^0/, '');
    }
    // 限制最大为100件
    shoppingCartInfo[index].submitInfo.buyNum = shoppingCartInfo[index].submitInfo.buyNum >= 100? 100 : shoppingCartInfo[index].submitInfo.buyNum;
    await watchShoppingCartInfo(index);
  }
  // 加一个商品的数量
  async function addOneGoods(index: number){
    if (shoppingCartInfo[index].submitInfo.buyNum >= 100) return
    shoppingCartInfo[index].submitInfo.buyNum++;
    await watchShoppingCartInfo(index);
  }
  
  // 全选框
  let checkAll = ref();
  // 单个勾选事件
  function checkedEvent(index:number){
    // 原来的勾选个数
    let originalCheckNum = ref(isChecked.filter((item:boolean)=>item).length);
    isChecked[index] = !isChecked[index];
    // 现在的勾选个数
    let nowCheckNum = ref(isChecked.filter((item:boolean)=>item).length);
    // 判断是否由未全选变为全选
    if (originalCheckNum.value < shoppingCartInfo.length && nowCheckNum.value === shoppingCartInfo.length){
      checkAll.value.checked = true;
    }
    // 判断是否由全选变为未全选
    if (originalCheckNum.value === shoppingCartInfo.length && nowCheckNum.value < shoppingCartInfo.length){
      checkAll.value.checked = false;
    }
    // 更新勾选状态数组
    updateShoppingCartSelected();
  }
  // 全选事件
  function checkAllEvent(){
    // 如果有未勾选的，就是未全选状态
    if (isChecked.filter((item:boolean)=>!item).length > 0){
      Object.assign(isChecked, new Array(shoppingCartInfo.length).fill(true));
    } else {
      // 否则是全选
      Object.assign(isChecked, new Array(shoppingCartInfo.length).fill(false));
    }
    // 更新勾选状态数组
    updateShoppingCartSelected();
  }

  // 勾选数量
  let checkedGoodsNum = computed(()=>{
    let tn = 0;
    isChecked.forEach((item:boolean,index:number)=>{
      tn += item ? shoppingCartInfo[index].submitInfo.buyNum : 0;
    })
    return tn
  })
  // 总价
  let checkedGoodsTotalPrice = computed(()=>{
    let tp = 0;
    isChecked.forEach((item:boolean,index:number)=>{
      tp += item ? shoppingCartInfo[index].submitInfo.price * shoppingCartInfo[index].submitInfo.buyNum : 0;
    })
    return tp
  })


  // 点删除一个商品
  async function deleteOneGoods(index:number){
    if (confirm('确认删除？')){
      shoppingCartInfo.splice(index,1);
      isChecked.splice(index,1);
      // 包装成数组
      await deleteShoppingCart([index], userName.value);
    } 
  }
  // 是否显示弹窗
  let isDeleteSelectedGoodsTipShow = ref(false);
  // 本地的选中的商品列表的索引
  let shoppingCartSelectedIndex: any = reactive([]);
  // 更新本地选中商品列表的索引
  function updateShoppingCartSelected(){
    // 先清空
    shoppingCartSelectedIndex.splice(0, shoppingCartSelectedIndex.length);
    isChecked.forEach((item: boolean,index: number)=>{
      if (item) { shoppingCartSelectedIndex.push(index) }
    })
  }
  // 点删除所选
  function deleteSelectedGoods(){
    // 先更新选中商品索引列表
    updateShoppingCartSelected();
    // 如果选了商品，显示弹窗
    if (shoppingCartSelectedIndex.length){
      isDeleteSelectedGoodsTipShow.value = true;
    }
  }
  // 弹窗中点确定，删除待删除商品列表中的商品
  async function deleteGoods(){
    // 先反转，从大到小删除，避免删掉小的导致大的索引找不到了
    shoppingCartSelectedIndex = shoppingCartSelectedIndex.reverse();
    shoppingCartSelectedIndex.forEach((index:number)=>{
        shoppingCartInfo.splice(index,1);
        isChecked.splice(index,1);
    })
    // 去掉弹窗
    isDeleteSelectedGoodsTipShow.value = false;
    await deleteShoppingCart(shoppingCartSelectedIndex, userName.value);
    // 更新待删除商品列表
    updateShoppingCartSelected();
    }

    
  // 取消，不删了
  function cancelDeleteGoods(){
    isDeleteSelectedGoodsTipShow.value = false;
  }

  // 结算前提取选中的商品数组
  let route = useRoute();
  let router = useRouter();
  // store中更新交易store中的选中商品列表
  let { changeShoppingCartSelected,changeShoppingCartSelectedIndex } = useTradeStore();
  function goToTrade(){
    if (isChecked.filter((item: boolean) => item).length === 0) { return }
    let tmp: any = [];
    toRaw(shoppingCartSelectedIndex).forEach((item: number) => { tmp.push(toRaw(shoppingCartInfo[item])) });
    changeShoppingCartSelected(tmp); // 修改store中选中商品数组
    changeShoppingCartSelectedIndex(shoppingCartSelectedIndex); // 修改store中选中商品索引数组
    route.meta.anyGoodsSelected = true;
    router.replace({path: '/trade'});
  }

</script>

<style lang="less" scoped>
  .cart {
    width: 70vw;
    min-width: 550px;
    margin: 0 auto;
    user-select: none;
    position: relative;
    margin-bottom: 130px;

    h4 {
      margin: 9px 0;
      font-size: 14px;
      line-height: 21px;
    }

    .cart-main {
      .cart-th {
        background: #f5f5f5;
        border: 1px solid #ddd;
        padding: 10px;
        overflow: hidden;

        &>div {
          float: left;
        }

        .cart-th1 {
          width: 15%;

          input {
            vertical-align: middle;
          }

          span {
            vertical-align: middle;
          }
        }

        .cart-th2 {
          width: 15%;
        }

        .cart-th3,
        .cart-th4,
        .cart-th5,
        .cart-th6 {
          width: 15%;

        }
      }
      .shoppingCartEmpty {
        width: 100%;
        height: 100%;
        font-size: 30px;
        text-align: center;
        margin: 200px auto;
      }

      .cart-body {
        margin-top: 15px;
        margin-bottom: 200px;
        border: 1px solid #ddd;
        max-height: 600px;
        overflow: auto;

        .cart-list {
          padding: 10px;
          border-bottom: 1px solid #ddd;
          overflow: hidden;
          display: flex;
          

          &>li {
            float: left;
          }

          .cart-list-con1 {
            width: 12%;
          }

          .cart-list-con2 {
            width: 10%;

            img {
              width: 82px;
              height: 82px;
              float: left;
            }

            .item-msg {
              float: left;
              width: 150px;
              margin: 0 10px;
              line-height: 18px;
            }
          }

          .cart-list-con3 {
            width: 20%;
            height: 82px;
            line-height: 20px;
            

            .item-txt {
              text-align: center;
              
            }
          }

          .cart-list-con4 {
            width: 13%;
            height: 82px;
            line-height: 82px;
            text-align: center;

          }

          .cart-list-con5 {
            width: 15%;
            transform: translateY(22px);
            display: flex;
            justify-content: center;
            height: 100%;

            .minus {
              border: 1px solid #ddd;
              border-right: 0;
              float: left;
              color: #666;
              width: 6px;
              text-align: center;
              padding: 8px;
            }

            input {
              border: 1px solid #ddd;
              width: 40px;
              height: 33px;
              float: left;
              text-align: center;
              font-size: 14px;
              
            }

            .plus {
              border: 1px solid #ddd;
              border-left: 0;
              float: left;
              color: #666;
              width: 6px;
              text-align: center;
              padding: 8px;
            }
          }

          .cart-list-con6 {
            width: 20%;
            height: 82px;
            line-height: 82px;
            text-align: center;

            .sum {
              font-size: 16px;
            }
          }

          .cart-list-con7 {
            width: 10%;
            height: 82px;
            line-height: 41px;

            a {
              color: #666;
              &:hover {
                color: red;
              }
            }
          }
        }
      }
    }

    .cart-tool {
      width: 100%;
      overflow: hidden;
      border-top: 1px solid #ccc;
      position: absolute;
      top: 100%;
      background-color: white;
      height: auto;
      padding: 30px;
      margin-bottom: 100px;
      box-shadow: 0 0 10px deepskyblue;
      box-sizing: border-box;
      

      .select-all {
        padding: 10px;
        overflow: hidden;
        float: left;

        span {
          vertical-align: middle;
        }

        input {
          vertical-align: middle;
        }
      }

      .option {
        padding: 10px;
        overflow: hidden;
        float: left;

        a {
          float: left;
          padding: 0 10px;
          color: #666;
          &:hover {
            color: red;
          }
        }
       
      }

      .money-box {
        float: right;

        .chosed {
          line-height: 26px;
          float: left;
          padding: 0 10px;
        }

        .sumprice {
          width: 200px;
          line-height: 22px;
          float: left;
          padding: 0 10px;

          .summoney {
            color: #c81623;
            font-size: 16px;
          }
        }

        .sumbtn {
          float: right;

          a {
            display: block;
            position: relative;
            width: 96px;
            height: 52px;
            line-height: 52px;
            color: #fff;
            text-align: center;
            font-size: 18px;
            font-family: "Microsoft YaHei";
            background: #e1251b;
            overflow: hidden;
          }
        }
      }
    }
  }
  .mask {
    background-color: rgba(0,0,0,0.5);
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    .dialog {
      width: 500px;
      height: 300px;
      text-align: center;
      background-color: #ccc;
      line-height: 130px;
      user-select: none;
      border-radius: 10px;
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translateX(-50%) translateY(-50%);

      h3 {
        font-size: 40px;
      }
      .btns {
        width: 500px;
        height: 80px;
        display: flex;
        justify-content: space-evenly;

        button {
          width: 100px;
          font-size: 40px;
          border-radius: 10px;
          border: none;
          cursor: pointer;
          &:hover {
            color: white;
            background-color: deepskyblue;
          }
        }
      }
    }
  }
</style>@/stores/user