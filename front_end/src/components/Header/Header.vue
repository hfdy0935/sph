<template>
    <header class="header">
        <!-- 头部的第一行 -->
        <div class="top">
            <div class="container">
                <div class="loginList">
                    <p>尚品汇欢迎您！</p>
                    <p>
                        <template v-if="!loginState">
                            <span>请</span>
                            <RouterLink to="/login" class="login">登录</RouterLink>
                            <RouterLink to="/register" class="register">免费注册</RouterLink>
                        </template>
                        <template v-if="loginState">
                            <RouterLink to="/shoppingCart" class="login">{{ userName }}</RouterLink>
                            <a @click="logout" class="register">退出登录</a>
                        </template>
                    </p>
                </div>
                <div class="typeList">
                    <RouterLink to="/center">我的订单</RouterLink>
                    <RouterLink to="/shoppingCart">我的购物车</RouterLink>
                    <a href="###">我的尚品汇</a>
                    <a href="###">尚品汇会员</a>
                    <a href="###">企业采购</a>
                    <a href="###">关注尚品汇</a>
                    <a href="###">合作招商</a>
                    <a href="###">商家后台</a>
                </div>
            </div>
        </div>
        <!--头部第二行 搜索区域-->
        <div class="bottom">
            <h1 class="logoArea">
                <RouterLink class="logo" title="尚品汇" to="/home">
                    <img src="./images/logo.png" alt="尚品汇">
                </RouterLink>
            </h1>
            <div class="searchArea">
                <form action="###" class="searchForm">
                    <input 
                        type="text" 
                        id="autocomplete" 
                        class="input-error input-xxlarge" 
                        v-model="keyword"
                        placeholder="请输入搜索内容"
                        ref="input"
                        @input="inputEvent"
                        @focus="focusEvent"
                        @blur="blurEvent"
                        @keydown.enter.prevent="goSearch"
                    />
                    <span class="clearInput" ref="clearInputIcon" @click="clearInputEvent">×</span>
                    <button class="sui-btn btn-xlarge btn-danger" type="button" @click="goSearch">搜索</button>
                    <div ref="inputListenerTip" class="inputListenerTip">商品名称长度应小于15</div>
                </form>
            </div>
        </div>
    </header>
</template>

<script setup lang="ts" name="Header">
    import { ref,onMounted,onBeforeUnmount } from 'vue'
    import { RouterLink,useRouter } from 'vue-router'
    import { storeToRefs } from 'pinia'
    import emitter from '@/utils/emitter'
    import { useSearchStore } from '@/stores/search'
    import { useUserStore } from '@/stores/user'
    
    let keyword = ref('');
    let { queryOfSearchComponent } = storeToRefs(useSearchStore());
    let { changeParamsOfSearchComponent,clearParamsOfSearchComponent } = useSearchStore();

    let router = useRouter(); // 路由器
    let inputListenerTip = ref(); // 输入长度监听提示
    let input = ref(); // 输入框
    let clearInputIcon = ref(); // 清除搜索框的×
    let { loginState,userName } = storeToRefs(useUserStore());
    let { setLoginState,setUserName } = useUserStore();

    // 输入事件
    function inputEvent(){
        clearInputIcon.value.style.display='block';
        inputListenerTip.value.style.display = keyword.value.length > 15 ? 'block' : 'none';
    }
    // 获取焦点事件
    function focusEvent(){
        clearInputIcon.value.style.display = keyword.value.length === 0 ? 'none' : 'block';
    }
    // 失去焦点事件
    function blurEvent(){
        setTimeout(()=>{
            clearInputIcon.value.style.display='none';
        },100)
    }
    
    // 清除输入内容事件
    function clearInputEvent(){
        // 输入框重新获取焦点，因为点了×之后会失焦
        input.value.focus();
        keyword.value = '';
        inputListenerTip.value.style.display = 'none';
    }
    
    // 搜索事件
    function goSearch(){
        if (!keyword.value.trim()) clearParamsOfSearchComponent();
        if (keyword.value.trim().length > 15) return;
        let searchInfo = keyword.value.trim();
        let params = { keyword: searchInfo };
        // 判断是否之前有query参数，如果有则保留
        let config:any = {
            name: 'search',
            params,
            query: queryOfSearchComponent.value || undefined
        };
        router.replace(config);
        // 把搜索页面的params输入参数存入store
        changeParamsOfSearchComponent(params);
    }

    // 绑定清除输入框事件
    onMounted(() => {
        emitter.on('clearSearchInput', () => {
            keyword.value = '';
        });
    })
    onBeforeUnmount(() => {
        emitter.off('clearSearchInput');
    })

    // 退出登录事件
    function logout(){
        setLoginState(false);
        setUserName('');
        localStorage.removeItem('userName');
        localStorage.removeItem('loginState');
        router.replace({
            path: '/home'
        })
    }
    // 前往购物车
    function goToShoppingCart(){
        if (loginState.value){
            router.replace({path: '/shoppingCart'})
            return
        }
        router.push({path: '/login'})
    }

    

</script>

<style scoped lang="less">
    .header {
        &>.top {
            background-color: #eaeaea;
            height: 30px;
            line-height: 30px;

            .container {
                width: 1200px;
                margin: 0 auto;
                overflow: hidden;

                .loginList {
                    float: left;

                    p {
                        float: left;
                        margin-right: 10px;

                        .register {
                            border-left: 1px solid #b3aeae;
                            padding: 0 5px;
                            margin-left: 5px;
                        }
                    }
                }
                
                .typeList {
                    float: right;

                    a {
                        padding: 0 10px;
                        cursor: pointer;

                        &+a {
                            border-left: 1px solid #b3aeae;
                        }
                    }

                }

            }
        }

        &>.bottom {
            width: 1200px;
            margin: 0 auto;
            overflow: hidden;

            .logoArea {
                float: left;
                cursor: pointer;

                .logo {
                    img {
                        width: 175px;
                        margin: 25px 45px;
                    }
                }
            }

            .searchArea {
                float: right;
                margin-top: 35px;

                .searchForm {
                    overflow: hidden;
                    position: relative;

                    input {
                        box-sizing: border-box;
                        width: 490px;
                        height: 32px;
                        padding: 0px 4px;
                        border: 2px solid #ea4a36;
                        float: left;

                        &:focus {
                            outline: none;
                        }
                    }

                    .clearInput {
                        width: 32px;
                        height: 32px;
                        font-size: 32px;
                        line-height: 32px;
                        position: absolute;
                        vertical-align: center;
                        top: -2px;
                        right: 70px;
                        display: none;
                        cursor: pointer;

                        &:hover {
                            color: deepskyblue;
                        }
                    }
                    button {
                        height: 32px;
                        width: 68px;
                        background-color: #ea4a36;
                        border: none;
                        color: #fff;
                        float: left;
                        cursor: pointer;

                        &:focus {
                            outline: none;
                        }
                    }
                    .inputListenerTip {
                        display: none;
                        background-color: white;
                        color: red;
                        width: 490px;
                        height: 60px;
                        text-align: center;
                        line-height: 30px;
                        font-size: 15px;
                        font-weight: bold;
                        user-select: none;
                    }
                }
            }
        }
    }
    a:hover {
        color: red;
    }
    a:active {
        color:red
    }
    input {
        background-color: rgb(240, 240, 240);
    }
    input:focus {
        background-color: white;
    }
    input::placeholder {
        opacity: 0.7;
    }
</style>@/stores/search@/stores/user