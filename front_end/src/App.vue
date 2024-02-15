<template>
  <Header></Header>
  <!-- <router-view></router-view> -->
  <!-- 可以保留从search组件调到detail组件再跳回来时，原来选择匹配等信息 -->
  <!-- query和params需要用pinia保存 -->
  
  <!-- <RouterView v-slot="{ Component }">
    <KeepAlive>
      <component :is="Component" />
    </KeepAlive>
  </RouterView> -->
  <RouterView></RouterView>
  <Footer v-show="isFooterShow"></Footer>
</template>

<script setup lang="ts">
  import { computed,watch,toRefs } from 'vue'
  import { useRoute } from 'vue-router'
  import { storeToRefs } from 'pinia'

  import emitter from '@/utils/emitter'
  import { useSearchStore } from '@/stores/search'

  import Header from '@/components/Header/Header.vue'
  import Footer from '@/components/Footer/Footer.vue'

  let route = useRoute();
  // 主页、搜索页面才显示Footer组件
  let isFooterShow = computed(()=>{
    // let { path } = route;
    // return ['/','/home','/search'].indexOf(path) === -1? false : true
    // 或者
    return route.meta.isFooterShow
  });

  let { requestBody } = storeToRefs(useSearchStore());
  let { changeRequestBody,getSearchList } = useSearchStore();
  // 发送请求
  async function request(){
    // params也算在路径中
    if (!route.path.includes('search')) {return}
    // 重置请求体之前获取请求体中的品牌和props
    let { tradeMark,props } = requestBody.value as {tradeMark: string, props: string};
    // 切换路由后的参数
    let { query,params } = toRefs(route);
    // 如果query、params都没有，则不发送请求，并触发清空商品列表和导航的操作、清除品牌和属性的操作，因为没商品了只有属性
    if (!(query.value.category1Name || params.value.keyword)) {
      emitter.emit('clearGoodsListAndNav');
      emitter.emit('clearTradeMarkAndProps');
      return
    }
    // 否则发送请求
    changeRequestBody({
      ...query.value,
      ...params.value,
      ...{tradeMark},
      ...{props}
    }); 
    // 发送请求
    let data = await getSearchList();
    // 触发事件，把请求结果给Search和SearchSelector
    emitter.emit('requestBodyOK',data.data);
  }

  // 需要在App组件中监听路由变化，每当Search路由变化，获取参数，更改请求体
  watch(route,async()=>{
    await request();
  });

  
</script>

<style scoped>

</style>@/stores/search