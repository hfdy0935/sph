<template>
  <div class="pay-main">
    <div class="pay-container">
      <div class="checkout-tit">
        <h4 class="tit-txt">
          <span class="success-icon"></span>
          <span class="success-info">订单提交成功，请您及时付款，以便尽快为您发货~~</span>
        </h4>
        <div class="paymark">
          <span class="fl">请您在提交订单<em class="orange time">4小时</em>之内完成支付，超时订单会自动取消。订单号：<em>{{ route.params.orderNum }}</em></span>
          <span class="fr"><em class="lead">应付金额：</em><em class="orange money">￥{{ orderInfo.finalPay }}</em></span>
        </div>
      </div>
      <div class="checkout-info">
        <h4>重要说明：</h4>
        <ol>
          <li>尚品汇商城支付平台目前支持<span class="zfb">支付宝</span>支付方式。</li>
          <li>其它支付渠道正在调试中，敬请期待。</li>
          <li>为了保证您的购物支付流程顺利完成，请保存以下支付宝信息。</li>
        </ol>
        <h4>支付宝账户信息：（很重要，<span class="save">请保存！！！</span>）</h4>
        <ul>
          <li>支付帐号：11111111</li>
          <li>密码：111111</li>
          <li>支付密码：111111</li>
        </ul>
      </div>
      <div class="checkout-steps">
        <div class="step-tit">
          <h5>支付平台</h5>
        </div>
        <div class="step-cont">
          <ul class="payType">
            <li @click="payPlatform='支付宝'" :class="{selected:payPlatform==='支付宝'}"><img src="./images/pay2.jpg"></li>
            <li @click="payPlatform='微信'" :class="{selected:payPlatform==='微信'}"><img src="./images/pay3.jpg"></li>
          </ul>

        </div>
        <div class="hr"></div>

        <div class="payshipInfo">
          <div class="step-tit">
            <h5>支付网银</h5>
          </div>
          <div class="step-cont">
            <ul class="payType">
              <li v-for="k in 12" :key="k" @click="payPlatform=bankPayList[k-1]" :class="{selected:payPlatform===bankPayList[k-1]}">
                <img :src="`./images/pay${k + 9}.jpg`">
              </li>
            </ul>
          </div>

        </div>
        <div class="hr"></div>

        <div class="submit">
          <!-- <router-link class="btn" to="/paysuccess">立即支付</router-link> -->
          <a class="btn" @click="payNow">立即支付</a>
        </div>
        <el-dialog v-model="dialogVisible" width="500" title="提示">
          <span>确认要支付吗？</span>
          <template #footer>
            <div class="dialog-footer">
              <el-button @click="dialogVisible = false">取消</el-button>
              <el-button type="primary" @click="confirmPay">
                确认
              </el-button>
            </div>
          </template>
        </el-dialog>
        <div class="otherpay">
          <div class="step-tit">
            <h5>其他支付方式</h5>
          </div>
          <div class="step-cont">
            <span><a href="weixinpay.html" target="_blank">微信支付</a></span>
            <span>中国银联</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts" name="Pay">
  import { ref,toRaw } from 'vue'
  import { useRoute,useRouter } from 'vue-router'
  import { storeToRefs } from 'pinia'
  import { useTradeStore } from '@/stores/trade'
  import { reqPay } from '@/api'
  import { ElMessage } from 'element-plus'

  let bankPayList = ['招商银行','邮储银行','交通银行','农业银行','广发银行','兴业银行','光大银行','中信银行','浦发银行','平安银行','民生银行','北京银行'];
  let payPlatform = ref('');
  let route = useRoute();
  let router = useRouter();

  // 获取store中储存的本次订单信息
  let { orderInfo }:any = storeToRefs(useTradeStore());
  // 确认购买对话框是否显示
  let dialogVisible = ref(false);
  function payNow(){
    if (payPlatform.value === '') {
      alert('请选择支付方式');
      return
    }
    // 显示对话框
    dialogVisible.value = true;
  }
  async function confirmPay(){
    dialogVisible.value = false;
    let userName = orderInfo.value.shoppingCartSelected[0].userName;
    const result:any = await reqPay({
      userName,
      'orderNum': route.params.orderNum,
      'hasPaid': true, 
      'payPlatform': payPlatform.value
    });
    if (result.message === 'OK'){
      router.replace({
        name: 'paySuccess',
        params: { 'orderNum': result.orderNum }
      })
      ElMessage({
        message: '支付成功',
        type: 'success'
      })
    }
  }

</script>

<style lang="less" scoped>
  .pay-main {
    margin-bottom: 20px;

    .pay-container {
      margin: 0 auto;
      width: 1200px;

      a:hover {
        color: #4cb9fc;
      }

      .orange {
        color: #e1251b;
      }

      .money {
        font-size: 18px;
      }

      .zfb {
        color: #e1251b;
        font-weight: 700;
      }

      .checkout-tit {
        padding: 10px;

        .tit-txt {
          font-size: 14px;
          line-height: 21px;

          .success-icon {
            width: 30px;
            height: 30px;
            display: inline-block;
            background: url(./images/icon.png) no-repeat 0 0;
          }

          .success-info {
            padding: 0 8px;
            line-height: 30px;
            vertical-align: top;
          }
        }

        .paymark {
          overflow: hidden;
          line-height: 26px;
          text-indent: 38px;

          .fl {
            float: left;
          }

          .fr {
            float: right;

            .lead {
              margin-bottom: 18px;
              font-size: 15px;
              font-weight: 400;
              line-height: 22.5px;
            }
          }
        }
      }

      .checkout-info {
        padding-left: 25px;
        padding-bottom: 15px;
        margin-bottom: 10px;
        border: 2px solid #e1251b;

        h4 {
          margin: 9px 0;
          font-size: 14px;
          line-height: 21px;
          color: #e1251b;
        }

        ol {
          padding-left: 25px;
          list-style-type: decimal;
          line-height: 24px;
          font-size: 14px;
        }

        ul {
          padding-left: 25px;
          list-style-type: disc;
          line-height: 24px;
          font-size: 14px;
        }
      }

      .checkout-steps {
        border: 1px solid #ddd;
        padding: 25px;

        .hr {
          height: 1px;
          background-color: #ddd;
        }

        .step-tit {
          line-height: 36px;
          margin: 15px 0;
        }

        .step-cont {
          margin: 0 10px 12px 20px;

          ul {
            font-size: 0;

            li {
              margin: 2px;
              display: inline-block;
              padding: 5px 20px;
              border: 1px solid #ddd;
              cursor: pointer;
              line-height: 18px;
              &.selected {
                border: 2px solid red;
                border-radius: 10px;
              }
            }
          }
        }
      }

      .submit {
        text-align: center;

        .btn {
          display: inline-block;
          padding: 15px 45px;
          margin: 15px 0 10px;
          font: 18px "微软雅黑";
          font-weight: 700;
          border-radius: 0;
          background-color: #e1251b;
          border: 1px solid #e1251b;
          color: #fff;
          text-align: center;
          vertical-align: middle;
          cursor: pointer;
          user-select: none;
          text-decoration: none;
        }
      }
    }
  }
</style>