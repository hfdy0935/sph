<template>
    <div>
      <TypeNav />
      <div class="main">
        <div class="py-container">
          <!--bread-->
          <div class="bread">
            <ul class="fl sui-breadcrumb" ref="tipRegionOfUl">
              <li>
                <a href="#" ref="tipRegion" class="tipRegion">全部结果</a>
              </li>
            </ul>
            <ul class="fl sui-tag">
              <li class="with-x" v-if="queryOfSearchComponent.category1Name">{{ queryOfSearchComponent.category1Name }}
                <i @click="removeCategoryName">×</i>
              </li>
              <li class="with-x" v-if="paramsOfSearchComponent.keyword">{{ paramsOfSearchComponent.keyword }}
                <i @click="removeSearchParams">×</i>
              </li>
              <li class="with-x" v-if="tradeMark">{{ tradeMark }}
                <i @click="removeTradeMark">×</i>
              </li>
              <template v-for="item of props">
                <li class="with-x">{{ item.attrName }}: {{ item.attrValue }}
                  <i @click="removeProp(item.attrId)">×</i>
                </li>
              </template>
            </ul>
          </div>
  
          <!--selector-->
          <SearchSelector @addTradeMarkToNav="getTradeMark" @addPropsToNav="getProps" ></SearchSelector>
  
          <!--details-->
          <div class="details clearfix" ref="rankRegion">
            <div class="sui-navbar">
              <div class="navbar-inner filter">
                <ul class="sui-nav">
                  <li>
                    <a @click.prevent style="color:black;cursor:auto">排序</a>
                  </li>
                  <li :class="isOrderActive[0]" @click="recoverDefaultOrder">
                    <a>默认</a>
                  </li>
                  <li :class="isOrderActive[1]" @click="changeTotalOrder">
                    <a>综合{{ totalOrder }}<div title="计算方式：价格*0.003 + 销量*0.007">?</div></a>
                  </li>
                  <li :class="isOrderActive[2]" @click="changePriceOrder">
                    <a>价格{{ priceOrder }}</a>
                  </li>
                  <li :class="isOrderActive[3]" @click="changeSalesOrder">
                    <a>销量{{ salesOrder }}</a>
                  </li>
                </ul>
              </div>
            </div>
            <div class="goods-list">
              <ul class="yui3-g">
                <li class="yui3-u-1-5" v-for="(item,index) of goodsList" :key="index">
                  <div class="list-wrap">
                    <!-- 跳往详情页 -->
                    <div class="p-img">
                      <a @click="goToGoodsDetail(item.id)">
                        <img :src="item.defaultImg" />
                      </a>
                    </div>
                    <div class="priceOrder">
                      <strong>
                        <em>¥</em>&nbsp;
                        <i>{{ item.price }}</i>
                      </strong>
                    </div>
                    <div class="attr">
                      <a target="_blank" href="#" :title="item.title">{{ item.title }}</a>
                      <br>
                      <a>综合得分：{{ (item.price*0.003+item.sales*0.007).toFixed(2) }}</a>
                    </div>
                    <div class="commit">
                      <i class="command">已售
                        <span :style="goodsStyle(item)">{{ item.sales }}</span>&nbsp;台
                        <div v-if="item.sales > 10000" class="highSalesNum">超高人气！</div>
                        <div v-else-if="item.sales > 5000" class="newSalesNum">后起之秀~</div>
                      </i>
                    </div>
                    <div class="operate">
                      <a href="success-cart.html" target="_blank" class="sui-btn btn-bordered btn-danger">加入购物车</a>
                      <a href="javascript:void(0);" class="sui-btn btn-bordered">收藏</a>
                    </div>
                  </div>
                </li>
              </ul>
            </div>
            <!-- 分页器 -->
            <Pagination
            v-show="isPaginationShow" 
            :totalGoodsNum="responseData.totalGoodsNum" 
            :totalPagesNum="responseData.totalPagesNum"
            :currentPage="responseData.currentPage"
            ></Pagination>
          </div>
        </div>
      </div>
    </div>
  </template>
  
<script lang="ts" setup name="Search">
    import { ref,reactive,onMounted,onBeforeUnmount,markRaw } from 'vue'
    import { useRouter } from 'vue-router'
    import { storeToRefs } from 'pinia'

    
    import emitter from '@/utils/emitter'
    import { useSearchStore } from '@/stores/search'
    import { useGoodsListStore } from '@/stores/goodsList'

    import TypeNav from '@/components/TypeNav/TypeNav.vue'
    import SearchSelector from '@/views/Search/SearchSelector/SearchSelector.vue'
    import Pagination from '@/components/Pagination/Pagination.vue'


    let { queryOfSearchComponent, paramsOfSearchComponent } = storeToRefs(useSearchStore());
    let { initRequestBody,changeRequestBody,getSearchList,clearParamsOfSearchComponent,clearQueryOfSearchComponent } = useSearchStore();
    // 路由器
    let router = useRouter();

    let isPaginationShow = ref(true); // 分页器是否显示
    let rankRegion = ref(); // 排序区域
    let tipRegion = ref(); // 提示
    let tipRegionOfUl = ref(); // 提示所在的ul
    // 动态决定每个商品的样式
    let goodsStyle = function(item:any){
      return {
        color: item.salesOrder>10000? 'red' : item.salesOrder>5000? 'deepskyblue' : '#646fb0',
        fontSize: item.salesOrder>10000? '20px' : item.salesOrder>5000? '16px' : '12px',
      }
    }
    
    // 响应数据中的data部分
    let responseData:any = reactive([]);
    // 接收的产品列表
    let goodsList:any = reactive({});
    // 储存商品列表
    let { changeGoodsList } = useGoodsListStore();
    // tradeMark添加或移除面包屑导航以及分页器时重新发请求
    // 这里路由没变，App监听不到，需要手动发请求并触发
    async function tradeMarkOrPropsOrPageChange(){
      let data = await getSearchList();
      emitter.emit('requestBodyOK',data.data);
    }
    // 绑定事件，APP处理完请求体之后触发
    onMounted(() => {
      emitter.on('requestBodyOK',(data:any) => {
        // 需要清空原商品列表再赋值，不然最后一页不足20的部分会被倒数第二页的内容填充
        Object.keys(goodsList).forEach((key:string) => {
          delete goodsList[key]
        })
        Object.assign(goodsList, data.goodsList);
        Object.assign(responseData, data);
        // 备份默认顺序商品列表，再切换到之前的排序
        defaultOrder = markRaw(data.goodsList);
        continuePreviousOrder(isOrderActive.indexOf('active'));
        // 分页器显示
        emitter.emit('searchPagePaginationDisplay', 'block');
        isPaginationShow.value = true;

        tipRegion.value.innerHTML = '全部结果';
        tipRegionOfUl.value.style.width = '60px';
        // 把本页商品列表数据存入store，后面Detail组件用
        changeGoodsList(goodsList);
      })
      // query、params为空时，触发清除商品列表对象和导航区数组的函数
      emitter.on('clearGoodsListAndNav',() => {
        Object.keys(goodsList).forEach(i => delete goodsList[i]);
        tradeMark.value = '';
        props.splice(0);
        // 分页器隐藏
        isPaginationShow.value = false;
        rankRegion.value.style.display = 'none';
        tipRegion.value.innerHTML = '<span style="color:deepskyblue">清选择商品分类或搜索商品关键词</span>';
        tipRegionOfUl.value.style.width = '200px';
      });
      // 点击分页器页数变化
      emitter.on('goToPage',async (page: any)=>{
        changeRequestBody({'pageNo': page});
        await tradeMarkOrPropsOrPageChange();
      });
    });
    onBeforeUnmount(() => {
      emitter.off('requestBodyOK');
      emitter.off('clearGoodsListAndNav');
      emitter.off('goToPage');
    })

    // 点×删除分类
    function removeCategoryName(){
      // 清除请求体
      initRequestBody();
      // 判断是否有params参数，如果有则保留
      let config = {
        name: 'search',
        params: paramsOfSearchComponent.value || undefined
      };
      router.replace(config);
      // 删除store中的paramsOfSearchComponent
      clearQueryOfSearchComponent();
    }
    
    // 点×删除params
    function removeSearchParams(){
      // 判断是否有query参数，如果有则保留保留
      let config = {
        name: 'search',
        query: queryOfSearchComponent.value || undefined
      };
      // 路由变化，监听到自动发送请求
      router.replace(config);
      // 触发清除输入框事件
      emitter.emit('clearSearchInput');
      changeRequestBody({keyword:''});
      // 删除store中的paramsOfSearchComponent
      clearParamsOfSearchComponent();
    }
    

    let tradeMark = ref('');
    // SearchSelector组件通过自定义事件传来的品牌名，加到面包屑导航中
    async function getTradeMark(name: string){
      // 重复点击相同的品牌，不发送请求
      if (tradeMark.value === name) { return }
      tradeMark.value = name;
      // 请求体添加tradeMark品牌属性，并发送请求，路由没变不用改query和params
      changeRequestBody({tradeMark: name});
      await tradeMarkOrPropsOrPageChange();
    }
    // 面包屑导航中移除品牌名
    async function removeTradeMark(){
      tradeMark.value = '';
      // 让SearchSelector中的品牌名转为未激活
      emitter.emit('blurBrand');
      // 请求体移除tradeMark品牌属性，并发送请求
      changeRequestBody({tradeMark: ''});
      await tradeMarkOrPropsOrPageChange();
    }

    let props: any = reactive([]);
    // 把其他属性添加到筛选结果中
    async function getProps(attrId: number, attrName: string, attrValue: string){
      let obj = {attrId, attrName, attrValue};
      // 添加第一个情况
      if (props.length === 0) {
        props.push(obj);
        // 发送请求
        changeRequestBody({props});
        await tradeMarkOrPropsOrPageChange();
        return
      }
      for (let item of props){
        if (item.attrName === attrName && item.attrValue === attrValue){ // 一模一样
          return
        } else if (item.attrName === attrName && item.attrValue !== attrValue) { // 名一样值不同
          item.attrValue = attrValue; 
          // 发送请求
          changeRequestBody({props});
          await tradeMarkOrPropsOrPageChange();
          return
        } 
      }
      props.push(obj); // 名、值都不同
      // 发送请求
      changeRequestBody({props});
      await tradeMarkOrPropsOrPageChange();
    }


    // 面包屑导航中移除某个prop
    async function removeProp(attrId: number){
      // 改变SearchSelector中属性名的激活状态
      emitter.emit('blurProps',attrId-1); // 转为索引
      let index = props.findIndex((e:any) => e.attrId === attrId);
      if (index !== -1) { props.splice(index,1)}
      // 发送请求
      changeRequestBody({props});
      await tradeMarkOrPropsOrPageChange();
    }



    // 排序部分
    let totalOrder = ref('↓');
    let priceOrder = ref('↓');
    let salesOrder = ref('↓');
    let isOrderActive = reactive(['active','','','']);

    // 默认顺序
    let defaultOrder:Array<object>;
    function recoverDefaultOrder(){
      if (isOrderActive[0] === 'active') return;
      Object.assign(isOrderActive,['active','','','']);
      Object.assign(goodsList,defaultOrder);
    }
    // 获取原来商品列表的一个复制数组
    function getGoodsListAsArray(){
        let tmp:Array<object> = [];
        Object.keys(goodsList).forEach((key:any)=>{
          tmp[key] = goodsList[key]
        })
        return tmp
    }
    function changeTotalOrder(){
      let tmp = getGoodsListAsArray();
      // 如果已经被激活，只需要转换排序
      if (isOrderActive[1] === 'active'){
        // 原来是降序，这里按照升序排
        if(totalOrder.value === '↓') {
          tmp.sort((a:any,b:any)=>a.price*0.003+a.sales*0.007 - b.price*0.003-b.sales*0.007);
          totalOrder.value = '↑';
        } else {
          tmp.sort((a:any,b:any)=>b.price*0.003+b.sales*0.007 - a.price*0.003-a.sales*0.007);
          totalOrder.value = '↓';
        }
      } else {
        // 未激活，需要先激活再按默认顺序排序
        Object.assign(isOrderActive,['','active','','']);
        if(totalOrder.value === '↓') {
          tmp.sort((a:any,b:any)=>b.price*0.003+b.sales*0.007 - a.price*0.003-a.sales*0.007);
        } else {
          tmp.sort((a:any,b:any)=>a.price*0.003+a.sales*0.007 - b.price*0.003-b.sales*0.007);
        }
      }
      Object.assign(goodsList,tmp);
    }
    // 价格排序
    function changePriceOrder(){
      let tmp = getGoodsListAsArray();
      if (isOrderActive[2] === 'active'){
        // 原来是降序，这里按照升序排
        if(priceOrder.value === '↓') {
          tmp.sort((a:any,b:any)=>a.price - b.price);
          priceOrder.value = '↑';
        } else {
          tmp.sort((a:any,b:any)=>b.price - a.price);
          priceOrder.value = '↓';
        }
      } else {
        Object.assign(isOrderActive,['','','active','']);
        if(priceOrder.value === '↓') {
          tmp.sort((a:any,b:any)=>b.price - a.price);
        } else {
          tmp.sort((a:any,b:any)=>a.price - b.price);
        }
      }
      Object.assign(goodsList,tmp);
    }
    // 销量排序
    function changeSalesOrder(){
      let tmp = getGoodsListAsArray();
      if (isOrderActive[3] === 'active'){
        if(salesOrder.value === '↓') {
          tmp.sort((a:any,b:any)=>a.sales - b.sales);
          salesOrder.value = '↑';
        } else {
          tmp.sort((a:any,b:any)=>b.sales - a.sales);
          salesOrder.value = '↓';
        }
      } else {
        Object.assign(isOrderActive,['','','','active']);
        if(salesOrder.value === '↓') {
          tmp.sort((a:any,b:any)=>b.sales - a.sales);
        } else {
          tmp.sort((a:any,b:any)=>a.sales - b.sales);
        }
      }
      Object.assign(goodsList,tmp);
    }

    // 继续上一次的分类，用于发送请求接收时
    // 先清空对应激活状态，再切换，这样顺序不变
    // 也可以不清空，直接执行两次切换
    function continuePreviousOrder(flag:number){
      switch(flag){
        case 0: break;
        case 1: isOrderActive[1] = '';changeTotalOrder();break;
        case 2: isOrderActive[2] = '';changePriceOrder();break;
        case 3: isOrderActive[3] = '';changeSalesOrder();break;
      }  
    }


    // 点击跳转到详情页
    let { changeCurrentGoods } = useGoodsListStore();
    function goToGoodsDetail(id:number){
      // 改变储存的当前商品的id，修改当前商品
      changeCurrentGoods(id);
      router.push({
        name: 'detail',
        params: {
          currentPage: responseData.currentPage,
          id
        }
      })
    }

    

</script>
  
<style lang="less" scoped>
  .main {
      margin: 10px 0;

      .py-container {
      width: 1200px;
      margin: 0 auto;

      .bread {
          margin-bottom: 5px;
          overflow: hidden;
          height: 60px;
          display: flex;

          .sui-breadcrumb {
            width: 60px;
            padding: 3px 15px;
            margin: 0;
            font-weight: 400;
            border-radius: 3px;
            float: left;

            li {
                display: inline-block;
                line-height: 18px;

                a {
                color: #666;
                text-decoration: none;

                &:hover {
                    color: #4cb9fc;
                }
                }
            }
          }

          .sui-tag {
            margin-top: -5px;
            list-style: none;
            font-size: 0;
            line-height: 0;
            padding: 5px 0 0;
            margin-bottom: 18px;
            float: left;

            .with-x {
                font-size: 12px;
                margin: 0 5px 5px 0;
                display: inline-block;
                overflow: hidden;
                color: #000;
                background: #f7f7f7;
                padding: 0 7px;
                height: 20px;
                line-height: 20px;
                border: 1px solid #dedede;
                white-space: nowrap;
                transition: color 400ms;
                cursor: pointer;

                i {
                margin-left: 10px;
                cursor: pointer;
                font: 400 14px tahoma;
                display: inline-block;
                height: 100%;
                vertical-align: middle;
                }

                &:hover {
                color: #28a3ef;
                }
            }
          }
      }

      .details {
          margin-bottom: 5px;

          .sui-navbar {
            overflow: visible;
            margin-bottom: 0;

            .filter {
              min-height: 40px;
              padding-right: 20px;
              background: #fbfbfb;
              border: 1px solid #e2e2e2;
              padding-left: 0;
              border-radius: 0;
              box-shadow: 0 1px 4px rgba(0, 0, 0, 0.065);

              .sui-nav {
              position: relative;
              left: 0;
              display: block;
              float: left;
              margin: 0 10px 0 0;

              li {
                float: left;
                line-height: 18px;

                a {
                display: block;
                cursor: pointer;
                padding: 11px 15px;
                color: #777;
                text-decoration: none;
                user-select: none;
                position: relative;
                div {
                  width: 12px;
                  height: 12px;
                  line-height: 12px;
                  background-color: #777;
                  display: inline-block;
                  text-align: center;
                  font-weight: bold;
                  border-radius: 8px;
                  color: white;
                  position: absolute;
                  top: 6px;
                }
              }

                &.active {
                  a {
                    background: #e1251b;
                    color: #fff;
                  }
                }
              }
            }
          }
        }

          .goods-list {
          margin: 20px 0;

          ul {
              display: flex;
              flex-wrap: wrap;

              li {
              height: 100%;
              width: 20%;
              margin-top: 10px;
              line-height: 28px;

              .list-wrap {
                  .p-img {
                    padding-left: 15px;
                    width: 215px;
                    height: 255px;

                    a {
                      color: #666;

                      img {
                      max-width: 100%;
                      height: auto;
                      vertical-align: middle;
                      }
                    }
                  }

                  .priceOrder {
                    padding-left: 15px;
                    font-size: 18px;
                    color: #c81623;

                    strong {
                      font-weight: 700;
                      i {
                        margin-left: -5px;
                      }
                    }
                }

                  .attr {
                    padding-left: 15px;
                    width: 85%;
                    overflow: hidden;
                    margin-bottom: 8px;
                    min-height: 38px;
                    cursor: pointer;
                    line-height: 1.8;
                    display: -webkit-box;
                    -webkit-box-orient: vertical;
                    -webkit-line-clamp: 2;

                    a {
                        color: #333;
                        text-decoration: none;
                    }
                  }

                  .commit {
                    padding-left: 15px;
                    height: 22px;
                    font-size: 13px;
                    color: #a7a7a7;
                    span {
                      font-weight: 700;
                      color: #646fb0;
                    }
                    .highSalesNum,.newSalesNum {
                      color:red;
                      font-size: 18px;
                      transform: rotateZ(30deg) translateX(90px) translateY(-60px);
                      font-weight: bolder;
                      user-select: none;
                      transition: all 0.1s linear;
                      &:hover {
                        font-size: 22px;
                      }
                    }
                    .newSalesNum {
                      color: deepskyblue;
                    }
                  }

                  .operate {
                    padding: 12px 15px;

                  .sui-btn {
                    display: inline-block;
                    padding: 2px 14px;
                    box-sizing: border-box;
                    margin-bottom: 0;
                    font-size: 12px;
                    line-height: 18px;
                    text-align: center;
                    vertical-align: middle;
                    cursor: pointer;
                    border-radius: 0;
                    background-color: transparent;
                    margin-right: 15px;
                  }

                  .btn-bordered {
                    min-width: 85px;
                    background-color: transparent;
                    border: 1px solid #8c8c8c;
                    color: #8c8c8c;

                    &:hover {
                      border: 1px solid #666;
                      color: #fff !important;
                      background-color: #666;
                      text-decoration: none;
                      }
                  }

                  .btn-danger {
                    border: 1px solid #e1251b;
                    color: #e1251b;

                    &:hover {
                    border: 1px solid #e1251b;
                    background-color: #e1251b;
                    color: white !important;
                    text-decoration: none;
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  
  

  img {
    transition: all 0.2s linear;
    &:hover {
      transform: scale(1.1);
    }
  }


</style
