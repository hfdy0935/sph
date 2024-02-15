<template>
  <div class="trade-container">
    <h3 class="title">填写并核对订单信息</h3>
    <div class="content">
      <h5 class="receive">收件人信息</h5>
      <div class="address clearFix" v-for="(person, index) of persons" :key="index">
        <span class="username" :class="{selected: currentPerson.name===person.name}" @click="currentPerson.name=person.name">{{ person.name }}</span>
        <p>
          <span class="s1"  @click="currentPerson.name=person.name">{{ person.address }}</span>
          <span class="s2">{{ person.tel }}</span>
          <span class="s3">默认地址</span>
        </p>
      </div>

      <div class="line"></div>
      <h5 class="pay">支付方式</h5>
      <div class="address clearFix">
        <span class="username" :class="{selected: payWay === '在线支付'}" @click="payWay='在线支付'">在线支付</span>
        <span class="username" :class="{selected: payWay === '货到付款'}" style="margin-left:5px;" @click="payWay='货到付款'">货到付款</span>

      </div>
      <div class="line"></div>
      <h5 class="pay">送货清单</h5>
      <div class="way">
        <h5>配送方式</h5>
        <div class="info clearFix">
          <select class="s1" v-model="postWay">
            <option disabled selected value="">请选择配送方式</option>
            <option value="极兔">极兔</option>
            <option value="顺丰">顺丰</option>
            <option value="邮政">邮政</option>
          </select>
          <p>配送时间：预计{{ postTime.month }}月{{ postTime.day }}日（周{{ postTime.week }}）{{ postTime.hours - 1 }}:{{ postTime.minutes }}-{{ postTime.hours + 1 }}:{{ postTime.minutes }}送达</p>
        </div>
      </div>
      <div class="detail">
        <h5>商品清单</h5>
        <ul class="list clearFix" v-for="(goods, index) of shoppingCartSelected" :key="index">
          <li>
            <img :src="goods.goodsInfo.defaultImg">
          </li>
          <li>
            <p>
              {{ goods.goodsInfo.category1Name }} - {{ goods.goodsInfo.title }}
            </p>
            <p>
              {{ goods.goodsInfo.color }} - {{ goods.goodsInfo.memory }} - {{ goods.goodsInfo.version }} - {{ goods.goodsInfo.way }}
            </p>
            <h4>7天无理由退货</h4>
          </li>
          <li>
            <h3>{{ goods.submitInfo.totalMoney }}</h3>
          </li>
          <li><span>X{{ goods.submitInfo.buyNum }}</span></li>
          <li><span>有货</span></li>
        </ul>

      </div>
      <div class="bbs">
        <h5>买家留言：</h5>
        <textarea placeholder="建议留言前先与商家沟通确认" class="remarks-cont" v-model="customTip"></textarea>
      </div>
      <div class="line"></div>
      <div class="bill">
        <h5>发票信息：</h5>
        <div>普通发票（电子） 个人 明细</div>
        <h5>使用优惠/抵用</h5>
      </div>
    </div>
    <div class="money clearFix">
      <ul>
        <li>
          <b><i>{{ totalTradeNum }}</i>件商品，总商品金额</b>
          <span>¥{{ totalTradeMoney }}</span>
        </li>
        <li>
          <b>返现：</b>
          <span>￥{{ returnMoney.toFixed(2) }}</span>
        </li>
        <li>
          <b>运费：</b>
          <span>￥{{ postMoney.toFixed(2) }}</span>
        </li>
      </ul>
    </div>
    <div class="trade">
      <div class="price">应付金额:　<span>¥{{ finalPay }}</span></div>
      <div class="receiveInfo">
        寄送至:
        <span>{{ currentPerson.address }}</span>
        收货人：<span>{{ currentPerson.name }}</span>
        <span>{{ currentPerson.tel }}</span>
      </div>
    </div>
    <div class="sub clearFix">
      <a class="subBtn" @click="submitTrade">提交订单</a>
    </div>
  </div>
</template>

<script setup lang="ts" name="Trade">
  import { ref,toRaw,computed,reactive } from 'vue'
  import { useRouter } from 'vue-router'
  import { storeToRefs } from 'pinia'

  import { useTradeStore } from '@/stores/trade'
  import { reqTrade,deleteShoppingCart } from '@/api'


  // 收件人
  let persons = [
    {name: '张三', address: '北京市昌平区宏福科技园综合楼6层', tel: '15010658793'},
    {name: '李四', address: '广东省广州市天河区xx路xx号', tel: '13590909098'},
    {name: '王五', address: '陕西省西安市xx区xx路xx号', tel: '18012340987'}
  ];
  // 默认收件人、地址、电话
  let currentPerson = reactive({
    name: '张三',
    address: '北京市昌平区宏福科技园综合楼6层',
    tel: '15010658793'
  });
  // 支付方式
  let payWay = ref('在线支付');
  // 配送方式
  let postWay = ref('');
  // 收货时间
  let postTime = computed(()=>{
    // 如果为null,则格式化当前时间为时间戳
    let dateTime: any = new Date();
    let dayNum: number = 3;
    // 如果dateTime长度为10或者13，则为秒和毫秒的时间戳，如果超过13位，则为其他的时间格式
    if (dateTime.toString().length == 10) dateTime *= 1000;
    const timestamp = +new Date(Number(dateTime));

    const one_day = 86400000; // 24 * 60 * 60 * 1000;
    const addVal = dayNum * one_day + timestamp;
    //x天后的日期
    const date = new Date(addVal);

    //格式化日期
    const filters = (n: any) => {
      return n < 10 ? (n = '0' + n) : n;
    };
    const month = filters(date.getMonth() + 1);
    const day = filters(date.getDate());
    const hours = filters(date.getHours());
    const minutes = filters(date.getMinutes());
    const seconds = filters(date.getSeconds());

    let weekDic: any = {
      0: '日',
      1: '一',
      2: '二',
      3: '三',
      4: '四',
      5: '五',
      6: '六'
    }
    return {
      year: date.getFullYear(),
      month,
      day,
      week: weekDic[date.getDay()],
      hours,
      minutes,
      seconds
    }
  })


  // 获取store中已选中商品列表
  let { shoppingCartSelected,shoppingCartSelectedIndex } = storeToRefs(useTradeStore());
  // 修改订单信息的函数
  let { changeOrderInfo } = useTradeStore();
  // 商品总数量和总价格
  let totalTradeNum = ref(0), totalTradeMoney = ref(0);
  shoppingCartSelected.value.forEach((goods: any) => {
    totalTradeNum.value += goods.submitInfo.buyNum;
    totalTradeMoney.value += goods.submitInfo.totalMoney;
  })
  // 买家留言
  let customTip = ref('');
  // 返现和运费
  let returnMoney = ref(Math.floor(Math.random()*20));
  let postMoney = ref(Math.floor(Math.random()*30 + 20));
  let finalPay = ref(totalTradeMoney.value - returnMoney.value + postMoney.value);
  
  // 提交订单
  let router = useRouter();
  async function submitTrade(){
    if (postWay.value === ''){
      alert('请选择配送方式');
      return
    }
    let currentTime = new Date();
    let orderInfo = {
      'currentPerson': toRaw(currentPerson),
      'payWay': payWay.value,
      'postWay': postWay.value,
      'createTime': `${currentTime.getFullYear()}-${currentTime.getMonth() + 1}-${currentTime.getDate()}`,
      'postTime':  `${postTime.value.year}-${postTime.value.month}-${postTime.value.day}-星期${postTime.value.week}-${postTime.value.hours - 1}:${postTime.value.minutes}~${postTime.value.hours + 1}:${postTime.value.minutes}`,
      'shoppingCartSelected': toRaw(shoppingCartSelected.value),
      'shoppingCartSelectedIndex': toRaw(shoppingCartSelectedIndex.value),
      'totalTradeNum': totalTradeNum.value,
      'totalTradeMoney': totalTradeMoney.value,
      'customTip': customTip.value,
      'returnMoney': returnMoney.value,
      'postMoney': postMoney.value,
      'finalPay': finalPay.value,
      'hasPaid': false
    }
    const result: any = await reqTrade(orderInfo);
    if (result.message === 'OK'){
      // 跳转到支付页面
      router.replace({
        name: 'pay',
        params: { 'orderNum': result.orderNum }
      });
      // 删除购物车中对应的商品
      let userName = orderInfo.shoppingCartSelected[0].userName;
      deleteShoppingCart(toRaw(orderInfo.shoppingCartSelectedIndex), userName);
      // 修改store中订单信息
    changeOrderInfo(orderInfo);
    }
  }
</script>

<style lang="less" scoped>
  .trade-container {
    .title {
      width: 1200px;
      margin: 0 auto;
      font-size: 14px;
      line-height: 21px;
    }

    .content {
      width: 1200px;
      margin: 10px auto 0;
      border: 1px solid rgb(221, 221, 221);
      padding: 25px;
      box-sizing: border-box;

      .receive,
      .pay {
        line-height: 36px;
        margin: 18px 0;
      }

      .address {
        padding-left: 20px;
        margin-bottom: 15px;

        .username {
          float: left;
          width: 100px;
          height: 30px;
          line-height: 30px;
          text-align: center;
          border: 1px solid #ddd;
          position: relative;
          cursor: pointer;
        }

        .username::after {
          content: "";
          display: none;
          width: 13px;
          height: 13px;
          position: absolute;
          right: 0;
          bottom: 0;
          background: url(./images/choosed.png) no-repeat;
        }

        .username.selected {
          border-color: #e1251b;
        }

        .username.selected::after {
          display: block;
        }

        p {
          width: 610px;
          float: left;
          line-height: 30px;
          margin-left: 10px;
          padding-left: 5px;
          cursor: pointer;

          .s1 {
            float: left;

          }

          .s2 {
            float: left;
            margin: 0 5px;
          }

          .s3 {
            float: left;
            width: 56px;
            height: 24px;
            line-height: 24px;
            margin-left: 10px;
            background-color: #878787;
            color: #fff;
            margin-top: 3px;
            text-align: center;
          }
        }

        p:hover {
          background-color: #ddd;
        }
      }

      .line {
        height: 1px;
        background-color: #ddd;
      }

      .way {
        width: 1080px;
        height: 110px;
        background: #f4f4f4;
        padding: 15px;
        margin: 0 auto;

        h5 {
          line-height: 50px;
        }

        .info {
          margin-top: 20px;

          .s1 {
            float: left;
            border: 1px solid #ddd;
            width: 120px;
            height: 30px;
            line-height: 30px;
            text-align: center;
            margin-right: 10px;
          }

          p {
            line-height: 30px;
          }
        }
      }

      .detail {
        width: 1080px;

        background: #feedef;
        padding: 15px;
        margin: 2px auto 0;

        h5 {
          line-height: 50px;
        }

        .list {
          display: flex;
          justify-content: space-between;
          border-bottom: 1px solid rgba(0,0,0,0.1);
          border-top: 1px solid rgba(0,0,0,0.1);
          li {
            margin-bottom: 10px;
            margin-top: 10px;
            img {
              height: 100px;
            }

            p {
              margin-bottom: 15px;
              width: 300px;
              line-height: 30px;
            }

            h4 {
              color: #c81623;
              font-weight: 400;
            }

            h3 {
              color: #e12228;
              width: 60px;
              line-height: 100px;
            }
            span {
              line-height: 100px;
            }
          }
        }
      }

      .bbs {
        margin-bottom: 15px;

        h5 {
          line-height: 50px;
        }

        textarea {
          width: 100%;
          border-color: #e4e2e2;
          line-height: 1.8;
          outline: none;
          resize: none;
        }
      }

      .bill {
        h5 {
          line-height: 50px;
        }

        div {
          padding-left: 15px;
        }
      }
    }

    .money {
      width: 1200px;
      margin: 20px auto;

      ul {
        width: 220px;
        float: right;

        li {
          line-height: 30px;
          display: flex;
          justify-content: space-between;

          i {
            color: red;
          }
        }
      }
    }

    .trade {
      box-sizing: border-box;
      width: 1200px;
      padding: 10px;
      margin: 10px auto;
      text-align: right;
      background-color: #f4f4f4;
      border: 1px solid #ddd;

      div {
        line-height: 30px;
      }

      .price span {
        color: #e12228;
        font-weight: 700;
        font-size: 14px;
      }

      .receiveInfo {
        color: #999;
      }
    }

    .sub {
      width: 1200px;
      margin: 0 auto 10px;

      .subBtn {
        float: right;
        width: 164px;
        height: 56px;
        font: 700 18px "微软雅黑";
        line-height: 56px;
        text-align: center;
        color: #fff;
        background-color: #e1251b;
        cursor: pointer;
        user-select: none;
      }
    }

  }
</style>