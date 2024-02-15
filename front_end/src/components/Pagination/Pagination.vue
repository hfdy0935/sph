<template>
  <div class="pagination">
    <button :disabled="currentPage === 1" @click="toPage(currentPage - 1)">上一页</button>
    <button v-if="currentPage >= 4 && totalPagesNum > 5" @click="toPage(1)">1</button>
    <button v-if="currentPage >= 5 && totalPagesNum > 5">···</button>


      <button 
        v-for="page in continuePagesNum" 
        :key="page" 
        :class="{active: start + page - 1 === currentPage}" 
        @click="toPage(start + page - 1)"
      >
        {{ start + page - 1}}
    </button>

        
    <button v-if="currentPage <= totalPagesNum - 4 && totalPagesNum > 5">···</button>
    <button v-if="currentPage <= totalPagesNum - 3 && totalPagesNum > 5" @click="toPage(totalPagesNum)">{{ totalPagesNum }}</button>
    <button :disabled="currentPage === totalPagesNum" @click="toPage(currentPage + 1)">下一页</button>
        
    <button style="margin-left: 30px" class="static">共 {{ totalGoodsNum }} 条</button>
    <button class="static">去第</button>
    <input type="text" v-model="goToPageNum" @keyup.enter="goToPageNumCheck" @input="goToPageNum=goToPageNum.replace(/[^0-9]/g,'')">
    <button class="static">页</button>
    <button @click="goToPageNumCheck">跳转</button>
  </div>
</template>
  

<script setup lang="ts" name="Pagination">
  import { ref,watchEffect } from 'vue'
  import emitter from '@/utils/emitter'


  let pageDetails = defineProps(['totalGoodsNum','totalPagesNum','currentPage']);
  let start = ref(0), end = ref(0), continuePagesNum = ref(5);
  
  watchEffect(()=>{
    const { totalPagesNum, currentPage } = pageDetails;
    // 总页数小于5
    if (totalPagesNum < 5) {
      start.value = 1;
      end.value = totalPagesNum;
      continuePagesNum.value = totalPagesNum;
    } else {
      // 总页数大于5
      start.value = currentPage -2;
      end.value = currentPage + 2;
      if (start.value < 1) {
        start.value = 1;
        end.value = 5;
      }
      if (end.value > totalPagesNum) {
        end.value = totalPagesNum;
        start.value = totalPagesNum - 4;
      }

    }
  })

  // 输入页数跳转
  let goToPageNum = ref('');
  function goToPageNumCheck(){
    let num = parseInt(goToPageNum.value);
    if (num && num <= pageDetails.totalPagesNum){
      toPage(parseInt(goToPageNum.value));
    } else if (num > pageDetails.totalPagesNum){
      toPage(pageDetails.totalPagesNum);
    }
    goToPageNum.value = '';
  }

  // 跳转页面事件
  function toPage(page: any){
    if (page === pageDetails.currentPage) return
    emitter.emit('goToPage',page);
  }

</script>

<style lang="less" scoped>
  .pagination {
    text-align: center;
    button {
      margin: 0 5px;
      background-color: #f4f4f5;
      color: #606266;
      outline: none;
      border-radius: 2px;
      padding: 0 4px;
      vertical-align: top;
      display: inline-block;
      font-size: 13px;
      min-width: 35.5px;
      height: 28px;
      line-height: 28px;
      cursor: pointer;
      box-sizing: border-box;
      text-align: center;
      border: 0;

      &[disabled] {
        color: #c0c4cc;
        cursor: not-allowed;
      }

      &.active {
        background-color: #409eff;
        color: #fff;
      }
      &:hover:not(.active) {
        color: deepskyblue
      }
      &:hover.static{
        color: #606266;
        cursor:auto
      }
    }
    input {
      width: 50px;
      transform: translateY(5px);
    }
  }
</style>
