<template>
  <el-carousel :interval="2000" trigger="click" :height="height" auto-play="true">
    <el-carousel-item v-for="image of list" :key="image.id">
        <img :src="image.imgUrl" alt="">
    </el-carousel-item>
  </el-carousel>
</template>


<script setup lang="ts" name="Carousel">
  defineProps(['list','height']);
</script>


<style scoped>
  .el-carousel__item {
    width: 730px;
    height: 454px;
  }
</style>