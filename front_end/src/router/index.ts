import { toRaw } from 'vue'
import { useSearchStore } from '@/stores/search'
import { createRouter, createWebHashHistory } from 'vue-router'
import { useRouterGuardStore } from '@/stores/routerGuard'
import emitter from '@/utils/emitter'



const router = createRouter({
    history:createWebHashHistory(),
    routes:[
        {
            path: '/',
            redirect: '/home'  
        },
        {
            name: 'home',
            path: '/home',
            component: ()=>import('@/views/Home/Home.vue'),
            meta: {isFooterShow:true},
            // 进入之前清空store中之前保存的params和query，以及输入框
            beforeEnter(to,from,next){
                const { clearParamsOfSearchComponent,clearQueryOfSearchComponent } = useSearchStore();
                clearParamsOfSearchComponent();
                clearQueryOfSearchComponent();
                emitter.emit('clearSearchInput');
                next();
            }
        },
        {
            name: 'login',
            path: '/login',
            component: ()=>import('@/views/Login/Login.vue'),
            meta: {isFooterShow:false}
        },
        {
            name: 'register',
            path:'/register',
            component: ()=>import('@/views/Register/Register.vue'),
            meta: {isFooterShow:false}
        },
        {
            name: 'search',
            path: '/search/:keyword?', // params参数可有可无
            component: ()=>import('@/views/Search/Search.vue'),
            meta: {isFooterShow:true},
            props(route){
                return route.query
            }
        },
        {
            name: 'detail',
            path: '/detail/:currentPage/:id',
            component: ()=>import('@/views/Detail/Detail.vue'),
        },
        {
            name: 'addCartSuccess',
            path: '/addCartSuccess',
            component: ()=>import('@/views/AddCartSuccess/AddCartSuccess.vue'),
            meta: {isFooterShow:true}
        },
        {
            name: 'shoppingCart',
            path: '/shoppingCart',
            component: ()=>import('@/views/ShoppingCart/ShoppingCart.vue'),
            meta: {isFooterShow: true}
        },
        {
            name: 'trade',
            path: '/trade',
            component: ()=>import('@/views/Trade/Trade.vue'),
            meta: {isFooterShow: true}
        },
        {
            name: 'pay',
            path: '/pay/:orderNum',
            component: ()=>import('@/views/Pay/Pay.vue'),
            meta: {isFooterShow: true}
        },
        {
            name: 'paySuccess',
            path: '/paySuccess/:orderNum',
            component: ()=>import('@/views/PaySuccess/PaySuccess.vue'),
            meta: {isFooterShow: true}
        },
        {
            name: 'center',
            path: '/center',
            component: ()=>import('@/views/Center/Center.vue'),
            meta: {isFooterShow: true}
        }
    ],
    // 每次切换路由后滚动到页面顶部
    scrollBehavior(to,from,savedPosition){
        return { top: 0 }
    }
})

// 全局前置路由守卫
// 每次去登录前判断是否已登录

let sign = true;
router.beforeEach((to, from ,next) => {
    // 登录、未登录都可以进
    // 1.主页
    if (to.name === 'home' || to.name === '/') { next();return }
    // 2.搜索结果页面，且无query或params参数
    if (to.name === 'search' && (to.query || to.params)) { next();return }
    // 3.商品详情页面，且有页数和商品序号
    if (to.name === 'detail' && (/.*?currentPage.*?\d+.*?id.*?\d+/.test(JSON.stringify(to.params)))) { next();return } 


    let { preRouterObj, changePreRouterObj, clearPreRouterObj } = useRouterGuardStore();
    // 已登录
    if (eval(localStorage.getItem('loginState') as string)) {
        // 如果来自登录、注册页面，则返回之前保存的页面
        if ((from.path === '/login' || from.path === '/register') && sign === true) { 
            sign = false;
            // 这时已经登录了，跳转到储存前一个路由的列表中最后一个非登录注册的路由，保底home
            let lastPage = toRaw(preRouterObj.findLast((item: any) => item.name !== 'login' && item.name !== 'register'))? toRaw(preRouterObj.findLast((item: any) => item.name !== 'login' && item.name !== 'register')) : '/home';
            next(lastPage);
            clearPreRouterObj();
            return
         }  
        
        // 加入购物车成功页面
        if (to.path === '/addCartSuccess' && from.name === 'detail') { next();return }
        // 购物车页面
        if (to.path === '/shoppingCart') { next();return }
        // 结算页面
        // 拦截 1.不是从trade进入的结算页面，2.从搜索页面进的但是没选商品（直接输入地址）
        if (to.path === '/trade' && (from.path == '/shoppingCart' || from.meta.anyGoodsSelected)) { next();return }
        // 支付页面
        if (to.name === 'pay' && (from.name === 'trade' || from.name === 'center')) { next();return }
        // 支付成功页面
        if (to.name === 'paySuccess' && from.name === 'pay') { next();return }
        // 我的订单
        if (to.path === '/center') { next();return }
        next(false); 
    } else {
        sign = true;
        // 保存登录注册之前的路由
        changePreRouterObj({'name': from.name, 'query': from.query, 'params': from.params});
        // 未登录
        // 去登录、注册
        if (to.path === '/login' || to.path === '/register') { next();return }
        // 去不了加入购物车成功、购物车
        if (to.path === '/addCartSuccess' || to.path === '/shoppingCart') { next('/login');return }
        // 个人中心
        if (to.path === '/center' || to.path === '/shoppingCart') { next('/login');return }
        next(false);
    }
})

export default router