<template>
  <el-carousel :interval="2000" type="card" trigger="click">
    <el-carousel-item v-for="image of list" :key="image.id" @click="sendImageUrlFromCarouselCardToZoom(image.imgUrl)">
        <img :src="image.imgUrl">
    </el-carousel-item>
  </el-carousel>
</template>


<script setup lang="ts" name="Carousel">
  import { onMounted,reactive } from 'vue'
  import { storeToRefs } from 'pinia'

  import emitter from '@/utils/emitter'


  import { useGoodsListStore } from '@/stores/goodsList'

  let { goodsList,currentGoods } = storeToRefs(useGoodsListStore());
  
  // 轮播图列表
  let list:any = reactive([]);

  function sendImageUrlFromCarouselCardToZoom(url:string){
    emitter.emit('sendImageUrlFromCarouselCardToZoom',url)
  }

  onMounted(()=>{
    
    list[0] = {id: currentGoods.value.id, imgUrl: currentGoods.value.defaultImg}
    for(let k=1; k<=4; k++){
      let num = Math.floor(Math.random()*(Object.keys(goodsList.value).length));
      list[k] = {
        id: num,
        imgUrl: goodsList.value[num].defaultImg
      }
    }
  })
    


</script>


<style scoped>
.el-carousel {
  width: 400px;
  margin-top: 10px;
  margin-bottom: 10px;
  vertical-align: center;
  background-color: rgba(0,0,0,0.3);
  border: 1px solid rgba(0,0,0,0.1);
  border-radius: 10px;
  box-shadow: 0 0 10px;
  text-align: center;
  height: 180px;
}
.el-carousel__item {
  border-radius: 5px;
  height: 160px;
}
img {
  height: 140px;
  margin-top: 10px;
  border: 1px solid black;
  border-radius: 10px;
}
</style>@/stores/goodsList