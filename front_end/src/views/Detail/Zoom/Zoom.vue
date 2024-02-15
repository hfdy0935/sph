<template>
  <div class="spec-preview">
    <img :src="currentGoods.defaultImg"/>
    <div class="event" @mousemove="mouseMoveListen($event)"></div>
    <div class="big">
      <img :src="currentGoods.defaultImg" ref="bigImg"/>
    </div>

    <div class="mask" ref="mask"></div>
  </div>
</template>



<script setup lang="ts" name="Zoom">
  import { ref,onMounted,reactive,onUnmounted } from 'vue'
  import { storeToRefs } from 'pinia'

  import emitter from '@/utils/emitter'
  import { useGoodsListStore } from '@/stores/goodsList'


  let { currentGoods } = storeToRefs(useGoodsListStore());

  onMounted(()=>{
    emitter.on('sendImageUrlFromCarouselCardToZoom',url=>{
      currentGoods.value.defaultImg = url;
    })
  })
  onUnmounted(()=>{
    emitter.off('sendImageUrlFromCarouselCardToZoom')
  })

  // 掩膜div
  let mask = ref();
  // 大图
  let bigImg = ref();
  // 鼠标在商品图上移动时的事件
  function mouseMoveListen(e: any){
    let left = e.offsetX - 100;
    left = left <= 0? 0 : left <= 200? left : 200;
    let top = e.offsetY - 100;
    top = top <= 0? 0 : top <= 200? top : 200;
    mask.value.style.left = left + 'px';
    mask.value.style.top = top + 'px';
    // 更新大图
    bigImg.value.style.top = -top*2 + 'px';
    bigImg.value.style.left = -left*2 + 'px';
  }
  
</script>




<style lang="less">
  .spec-preview {
    position: relative;
    width: 400px;
    height: 400px;
    border: 1px solid #ccc;

    img {
      width: 100%;
      height: 100%;
    }

    .event {
      width: 100%;
      height: 100%;
      position: absolute;
      top: 0;
      left: 0;
      z-index: 998;
    }

    .mask {
      width: 50%;
      height: 50%;
      background-color: rgba(0, 255, 0, 0.3);
      position: absolute;
      left: 0;
      top: 0;
      display: none;
    }

    .big {
      width: 100%;
      height: 100%;
      position: absolute;
      top: -1px;
      left: 100%;
      border: 1px solid #aaa;
      overflow: hidden;
      z-index: 998;
      display: none;
      background: white;

      img {
        width: 200%;
        max-width: 200%;
        height: 200%;
        position: absolute;
        left: 0;
        top: 0;
      }
    }

    .event:hover~.mask,
    .event:hover~.big {
      display: block;
    }
  }
</style>@/stores/goodsList