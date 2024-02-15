<template>
    <TypeNav></TypeNav>
    <ListContainer></ListContainer>
    <Recommend></Recommend>
    <Rank></Rank>
    <Like></Like>
    <Floor v-for="data of floorList" :key="data.id" :data="data"></Floor>
    <Brand></Brand>
</template>

<script setup lang="ts" name="Home">
    import { reactive,onMounted } from 'vue'
    import { useHomeStore } from '@/stores/home'
    import TypeNav from '@/components/TypeNav/TypeNav.vue'
    import ListContainer from '@/views/Home/ListContainer/ListContainer.vue'
    import Recommend from '@/views/Home/Recommend/Recommend.vue'
    import Rank from '@/views/Home/Rank/Rank.vue'
    import Like from '@/views/Home/Like/Like.vue'
    import Floor from '@/views/Home/Floor/Floor.vue'
    import Brand from '@/views/Home/Brand/Brand.vue'

    let floorList:any = reactive({});
    onMounted(async() => {
        let { getFloorList } = useHomeStore();
        Object.assign(floorList, await getFloorList());
    })
</script>

@/stores/home