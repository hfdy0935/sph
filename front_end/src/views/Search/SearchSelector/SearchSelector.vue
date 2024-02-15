<template>
  <div class="clearfix selector">
    <div class="type-wrap logo">
      <div class="fl key brand" ref="brandRegion">品牌</div>
      <div class="value logos">
        <ul class="logo-list">
          <li v-for="item of tradeMarkList" :key="item.tmId">
            <img v-if="item.isImage" :src="item.tmUrl" @click="clickBrand(item.tmId,item.tmName)" :class="isBrandActive[item.tmId-1]"/>
            <li v-else @click="clickBrand(item.tmId,item.tmName)" :class="isBrandActive[item.tmId-1]">{{ item.tmName }}</li>
          </li>
        </ul>
      </div>
      <div class="ext" ref="ext">
        <a href="javascript:void(0);" class="sui-btn">多选</a>
        <a href="javascript:void(0);">更多</a>
      </div>
    </div>
    <div class="type-wrap" v-for="item of attrsList" :key="item.attrId">
      <div class="fl key">{{ item.attrName }}</div>
      <div class="fl value">
        <ul class="type-list">
          <li 
          v-for="(attrValue,index) of item.attrValueList" 
          :key="index" :title="`${item.attrName} : ${attrValue}`" 
          @click="clickProps(item.attrId,item.attrName,attrValue,index)"
          :class="isAttrsActive[item.attrId-1]? isAttrsActive[item.attrId-1][index]: ''"
          >
            <a>{{ attrValue }}</a>
          </li>
        </ul>
      </div>
      <div class="fl ext"></div>
    </div>

  </div>
</template>
  
<script lang="ts" setup name="SearchSelector">
  import { ref,reactive,onMounted,onBeforeMount,toRaw } from 'vue'

  import emitter from '@/utils/emitter'

  
  let attrsList:any = reactive({});
  let tradeMarkList:any = reactive({});

  let brandRegion = ref();
  let ext = ref();


  onMounted(() => {
    emitter.on('requestBodyOK',(data:any) => {
      Object.assign(attrsList, data.attrsList);
      Object.assign(tradeMarkList, data.tradeMarkList);
      // 初始化储存每个属性激活状态的数组
      if (isAttrsActiveCount++ < 1){
        // 挂载后只初始化一次
        initIsAttrsActive(); 
      }
      brandRegion.value.textContent = '品牌';
      brandRegion.value.style.height = 'auto';
      ext.value.style.display = 'block';
    })
    emitter.on('clearTradeMarkAndProps',()=>{
      Object.keys(attrsList).forEach(i=>{
        delete attrsList[i];
      });
      Object.keys(tradeMarkList).forEach(i=>{
        delete tradeMarkList[i];
      });
      brandRegion.value.textContent = '';
      brandRegion.value.style.height = '220px';
      ext.value.style.display = 'none';
    })
    // 所有品牌都失焦
    emitter.on('blurBrand',()=>{
      Object.assign(isBrandActive, new Array(Object.keys(tradeMarkList).length).fill(''));
    })
    // 对应行的属性失焦
    emitter.on('blurProps',(rowIndex:any)=>{
      initIsAttrsActive(rowIndex);
    })
  })
  onBeforeMount(() => {
    emitter.off('requestBodyOK');
    emitter.off('clearTradeMarkAndProps');
    emitter.off('blurBrand');
    emitter.off('blurProps');
  })


  // 品牌是否激活
  let isBrandActive:any = reactive([]);
  // 点击品牌事件
  function clickBrand(tmId:number,tmName:string){
    // 触发新增品牌事件
    emit('addTradeMarkToNav',tmName);
    // 给点的这个品牌新增类：激活
    Object.assign(isBrandActive, new Array(Object.keys(tradeMarkList).length).fill(''));
    isBrandActive[tmId-1] = 'active';
  }



  // 保存每种属性是否激活的数组
  let isAttrsActive:any = reactive([]);
  let isAttrsActiveCount = 0;
  // 清空所有或某行激活状态
  function initIsAttrsActive(rowIndex:number = -1){
    let arr = [];
    // 清空所有
    if (rowIndex === -1){
      for(let item of Object.keys(attrsList)){
        let tmp = new Array(attrsList[item].attrValueList.length).fill('');
        // id从1开始，数组下标从0开始
        arr[attrsList[item].attrId-1] = tmp;
      }
      Object.assign(isAttrsActive,arr);
    } else {
      // 清空某行
      let tmp = new Array(attrsList[rowIndex].attrValueList.length).fill('');
      Object.assign(isAttrsActive[rowIndex],tmp);
    }
  }
  // 点击属性事件
  function clickProps(attrId:number,attrName:string,attrValue:string,index:number){
    emit('addPropsToNav',attrId,attrName,attrValue);
    // 重置所在那行属性的激活状态
    initIsAttrsActive(attrId-1);
    isAttrsActive[attrId-1][index] = 'active';
  }


  let emit = defineEmits(['addTradeMarkToNav','addPropsToNav']);

</script>

<style lang="less" scoped>
  .selector {
    border: 1px solid #ddd;
    margin-bottom: 5px;
    overflow: hidden;

    .logo {
      border-top: 0;
      margin: 0;
      position: relative;
      overflow: hidden;

      .key {
        line-height: 226px !important;
        // padding-bottom: 87px !important;
      }
    }

    .type-wrap {
      margin: 0;
      position: relative;
      border-top: 1px solid #ddd;
      overflow: hidden;

      .key {
        width: 100px;
        height: 36px;
        background: #f1f1f1;
        line-height: 26px;
        text-align: right;
        padding: 10px 10px 0 15px;
        float: left;
      }

      .value {
        height: 100%;
        overflow: hidden;
        padding: 10px 0 0 15px;
        color: #333;
        margin-left: 120px;
        padding-right: 90px;

        .logo-list {
          li {
            float: left;
            border: 1px solid #e4e4e4;
            margin: -1px -1px 0 0;
            width: 105px;
            height: 52px;
            text-align: center;
            line-height: 52px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            font-weight: 700;
            color: #333;
            font-style: italic;
            font-size: 14px;

            img {
              max-width: 100%;
              vertical-align: middle;
            }
          }
        }

        .type-list {
          li {
            float: left;
            display: block;
            margin-right: 30px;
            line-height: 26px;
            height: 36px;

            a {
              text-decoration: none;
              color: #666;
              padding-left: 10px;
              padding-right: 10px;
              height: 36px;
              line-height: 36px;
              margin-top: 10px;
            }
          }
        }
      }

      .ext {
        position: absolute;
        top: 10px;
        right: 10px;

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
          padding: 0 10px;
          background: #fff;
          border: 1px solid #d5d5d5;
        }

        a {
          color: #666;
        }
      }
    }
  }
  li {
    user-select: none;
    cursor: pointer;
  }
  .active {
    color: white !important;
    background-color: #e1251b;
  }
  .active a {
    color: white !important;
  }
</style>