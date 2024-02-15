<template>
  <div class="cart-complete-wrap">
    <div class="cart-complete">
      <h3><i class="sui-icon icon-pc-right"></i>商品已成功加入购物车！</h3>
      <div class="goods">
        <div class="left-good">
          <div class="left-pic">
            <img :src="currentGoods.defaultImg">
          </div>
          <div class="right-info">
            <p class="title">{{ currentGoods.title }}</p>
          </div>
          <div class="right-info" style="margin-left: 30px;">
            <p class="attr">颜色：<span>{{ currentGoods.submitInfo.goodsInfo.color }}</span></p>
            <p class="attr">内存：<span>{{ currentGoods.submitInfo.goodsInfo.memory }}</span></p>
          </div>
          <div class="right-info">
            <p class="attr">版本：<span>{{ currentGoods.submitInfo.goodsInfo.version }}</span></p>
            <p class="attr">购买方式：<span>{{ currentGoods.submitInfo.goodsInfo.way }}</span></p>
          </div>
          <div class="right-info num">
            数量：<span>{{ currentGoods.submitInfo.submitInfo.buyNum }}</span>
          </div>
          <div class="right-info totalMoney">
            总金额：<span>{{ currentGoods.submitInfo.submitInfo.totalMoney }}</span>
          </div>
        </div>
        <div class="right-gocart">
          <a @click="goToCurrentGoodsDetail" class="sui-btn btn-xlarge">返回商品详情</a>
          <RouterLink  to="/shoppingCart" replace>去购物车结算</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts" name="AddCartSuccess">
  import { useRouter } from 'vue-router'
  import { storeToRefs } from 'pinia'

  import { useGoodsListStore } from '@/stores/goodsList'

  let { currentGoods }:any = storeToRefs(useGoodsListStore());
  

  // 返回商品详情页面
  let router = useRouter();
  function goToCurrentGoodsDetail(){
    router.replace({
      name: 'detail',
      params: {
        currentPage: currentGoods.value.defaultImg.match(/\/(\d+)\/(\d+)$/)[1],
        id: currentGoods.value.defaultImg.match(/\/(\d+)\/(\d+)$/)[2]
      }
    })
  }


</script>

<style lang="less" scoped>
  .cart-complete-wrap {
    background-color: #f4f4f4;
    user-select: none;
    height: 446px;

    .cart-complete {
      width: 1200px;
      margin: 0 auto;

      h3 {
        font-weight: 400;
        font-size: 16px;
        color: #6aaf04;
        padding-top: 15px;
        padding-bottom: 15px;
        margin: 0;

        .icon-pc-right {
          background-color: #fff;
          border: 2px solid #6aaf04;
          padding: 3px;
          margin-right: 8px;
          border-radius: 15px;
        }
      }

      .goods {
        overflow: hidden;
        padding: 10px 0;

        .left-good {
          float: left;

          .left-pic {
            border: 1px solid #dfdfdf;
            width: 60px;
            float: left;
            img {
              width: 60px;
              height: 60px;
            }
          }

          .right-info {
            color: #444;
            float: left;
            margin-left: 20px;

            .title {
              width: 100%;
              height: 60px;
              line-height: 60px;
              overflow: hidden;
              text-overflow: ellipsis;
              white-space: nowrap;
              font-size: 20px;
            }

            .attr {
              color: #aaa;
              height: 60px;
              span {
                color: deepskyblue;
              }
            }
          }
          .num,.totalMoney {
            font-size: 20px;
            color: #444;
            height: 60px;
            line-height: 60px;
            margin-right: 30px;
            span {
              color: red;
            }
          }
        }

        .right-gocart {
          float: right;

          a {
            padding: 7px 36px;
            font-size: 15px;
            line-height: 22px;
            color: #333;
            background-color: #eee;
            text-decoration: none;
            box-sizing: border-box;
            border: 1px solid #e1e1e1;
          }

          a:hover {
            background-color: #f7f7f7;
            border: 1px solid #eaeaea;
          }

          a:active {
            background-color: #e1e1e1;
            border: 1px solid #d5d5d5;
          }

          .btn-danger {
            background-color: #e1251b;
            color: #fff;
          }

          .btn-danger:hover {
            background-color: #e1251b;
          }
        }

      }
    }
  }
</style>@/stores/goodsList