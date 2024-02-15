<template>
    <div class="type-nav">
        <div class="container">
            <h2 class="all" @mouseenter="enterSortShow" @mouseleave="leaveSortShow">全部商品分类</h2>
            <nav class="nav">
                <a href="###">服装城</a>
                <a href="###">美妆馆</a>
                <a href="###">尚品汇超市</a>
                <a href="###">全球购</a>
                <a href="###">闪购</a>
                <a href="###">团购</a>
                <a href="###">有趣</a>
                <a href="###">秒杀</a>
            </nav>
            <div class="sort" v-show="isSortShow" @mouseenter="enterSortShow" @mouseleave="leaveSortShow">
                <div class="all-sort-list2">
                    <div 
                        class="item" 
                        v-for="c1 of data" 
                        :key ="c1.categoryId" 
                        :class="{cur:currentIndex == c1.categoryId}" 
                        @mouseenter="mouseEnter(c1.categoryId)" 
                        @mouseleave="mouseLeave"
                    >
                        <h3 @click.stop="goSearch(c1.categoryId,c1.categoryName)">
                            <a>{{c1.categoryName}}</a>
                        </h3>
                        <div class="item-list clearfix" :style="{display:currentIndex === c1.categoryId? 'block':'none'}">
                            <div class="subitem" v-for="c2 of c1.categoryChild" :key="c2.categoryId">
                                <dl class="fore">
                                    <dt @click.stop="goSearch(c1.categoryId,c1.categoryName,c2.categoryId,c2.categoryName)">
                                        <a>{{ c2.categoryName }}</a>
                                    </dt>
                                    <dd>
                                        <em 
                                        v-for="c3 of c2.categoryChild" 
                                        :key="c3.categoryId" 
                                        @click.stop="goSearch(c1.categoryId,c1.categoryName,c2.categoryId,c2.categoryName,c3.categoryId,c3.categoryName)"
                                        >
                                            <a>{{ c3.categoryName }}</a>
                                        </em>
                                    </dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts" name="TypeNav">
    import { ref,reactive,computed,watchEffect,onMounted,inject } from 'vue'
    import { useRoute,useRouter } from'vue-router'
    import { storeToRefs } from 'pinia'

    import { useHomeStore } from '@/stores/home'
    import { useSearchStore } from '@/stores/search'


    // 挂载后发送请求获取列表数据
    let data:any = reactive({});
    onMounted(async() => {
        let { getCategoryList } = useHomeStore();
        Object.assign(data, await getCategoryList());
    });
    
    // 鼠标进入移出时时样式改变
    // 用CSS设置更简单
    let currentIndex = ref(-1);
    function mouseEnter(index:number){
        currentIndex.value = index;
    }
    function mouseLeave(){
        currentIndex.value = -1;
    }

    let router = useRouter();

    let { paramsOfSearchComponent } = storeToRefs(useSearchStore());
    let { changeRequestBody,initRequestBody,changeQueryOfSearchComponent } = useSearchStore();
    function goSearch(p1:string, n1:string, p2 = false,n2 = false, p3 = false, n3 = false){
        initRequestBody();
        // Id用请求体传不直接写在query参数中
        changeRequestBody({
            category1Id: p1,
            category2Id: p2 || '',
            category3Id: p3 || ''
        })
        // 判断之前是否有params，如果有则带上
        // 这里需要排除detail路由中的currentPage和id参数，因为是全局路由的params
        // 从detail组件切回来时，获取之前储存的搜索关键词
        let query = {
            category1Name: n1,
            category2Name: n2 || undefined,
            category3Name: n3 || undefined,
        };
        let config:any = {
            name: 'search',
            query,
            params: paramsOfSearchComponent.value || undefined
        };
        router.push(config);
        // 把搜索页面的query分类参数存入store
        changeQueryOfSearchComponent(query);
    }
    

    // 左侧导航栏是否显示
    let isSortShow = ref(true);
    let route = useRoute();
    watchEffect(() => {
        isSortShow.value = route.path === '/home'? true:false;
    })
    function enterSortShow(){
        isSortShow.value = route.path === '/home'? isSortShow.value:true;
    }
    function leaveSortShow(){
        isSortShow.value = route.path === '/home'? isSortShow.value:false;
    }
    
</script>


<style scoped lang="less">
    .type-nav {
        border-bottom: 2px solid #e1251b;

        .container {
            width: 1200px;
            margin: 0 auto;
            display: flex;
            position: relative;

            .all {
                width: 210px;
                height: 45px;
                background-color: #e1251b;
                line-height: 45px;
                text-align: center;
                color: #fff;
                font-size: 14px;
                font-weight: bold;
            }

            .nav {
                a {
                    height: 45px;
                    margin: 0 22px;
                    line-height: 45px;
                    font-size: 16px;
                    color: #333;
                }
            }

            .sort {
                position: absolute;
                left: 0;
                top: 45px;
                width: 210px;
                height: 461px;
                position: absolute;
                background: #fafafa;
                z-index: 999;

                .all-sort-list2 {
                    .item {
                        h3 {
                            line-height: 30px;
                            font-size: 14px;
                            font-weight: 400;
                            overflow: hidden;
                            padding: 0 20px;
                            margin: 0;

                            a {
                                color: #333;
                            }
                        }

                        .item-list {
                            display: none;
                            position: absolute;
                            width: 734px;
                            min-height: 460px;
                            background: #f7f7f7;
                            left: 210px;
                            border: 1px solid #ddd;
                            top: 0;
                            z-index: 9999 !important;

                            .subitem {
                                float: left;
                                width: 650px;
                                padding: 0 4px 0 8px;

                                dl {
                                    border-top: 1px solid #eee;
                                    padding: 6px 0;
                                    overflow: hidden;
                                    zoom: 1;

                                    &.fore {
                                        border-top: 0;
                                    }

                                    dt {
                                        float: left;
                                        width: 54px;
                                        line-height: 22px;
                                        text-align: right;
                                        padding: 3px 6px 0 0;
                                        font-weight: 700;
                                    }

                                    dd {
                                        float: left;
                                        width: 415px;
                                        padding: 3px 0 0;
                                        overflow: hidden;

                                        em {
                                            float: left;
                                            height: 14px;
                                            line-height: 14px;
                                            padding: 0 8px;
                                            margin-top: 5px;
                                            border-left: 1px solid #ccc;
                                        }
                                    }
                                }
                            }
                        }

                        // &:hover {
                        //     .item-list {
                        //         display: block;
                        //     }
                        // }
                    }
                }
            }
        }
    }
    a:hover {
        color: red;
    }
    a {
        cursor: pointer;
    }
    .cur {
        background-color: deepskyblue;
        h3>a {
            color: white !important;
        }
    }

</style>@/stores/home@/stores/search