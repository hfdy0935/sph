import requests from './requests'

// 三级联动接口
//    /api/product/getBaseCategoryList  get  无参数
export const reqCategoryList = () => requests.get('/home/getBaseCategoryList')
export const reqBannerList = () => requests.get('/home/getBannerList')
export const reqFloorList = () => requests.get('/home/getFloorList')

// 搜索页面
export const reqSearchList = (data:object) => requests({
    url: `/search/goods/${Date.now()}`,
    method: 'POST',
    data: data
})
// 提交购物车
export const submitShoppingCart = (data:object) => requests({
    url: `/shoppingCart/set/${Date.now()}`,
    method: 'POST',
    data: Object.assign(data)
})
// 获取购物车数据
export const getShoppingCart = (userName: object) => requests({
    url: `shoppingCart/get/${Date.now()}`,
    method: 'POST',
    data: userName
})
// 修改购物车数量
export const changeShoppingCart = (index: number, data: object, userName: string)=> requests({
    url: `shoppingCart/change/${Date.now()}`,
    method: 'POST',
    data: {index, data, userName}
})

// 删除购物车的商品
export const deleteShoppingCart = (index: Array<number>, userName: string)=> requests({
    url: `shoppingCart/delete/${Date.now()}`,
    method: 'POST',
    data: {'index': index, userName}
})

// 获取验证码
export const reqIdCode = (data: object)=> requests({
    url: `user/register/reqIdCode/${Date.now()}`,
    method: 'POST',
    data
})
// 注册
export const reqRegister = (data: object) => requests({
    url: `user/register/%{Date.now()}`,
    method: 'POST',
    data
})
// 登录
export const reqLogin = (data: object) => requests({
    url: `user/login/${Date.now()}`,
    method: 'POST',
    data
})
// 提交订单
export const reqTrade = (data: object) => requests({
    url: `/trade/order/${Date.now()}`,
    method: 'POST',
    data
})
// 支付
export const reqPay = (data: object) => requests({
    url: `/trade/pay/${Date.now()}`,
    method: 'POST',
    data
})
// 个人中心
export const reqCenter = (userName: string) => requests({
    url: `/center/${Date.now()}`,
    method: 'POST',
    data: { userName }
})
// 删除某个订单
export const reqDeleteOneOrder = (userName: string, orderNum: string) => requests({
    url: `/trade/delete/${Date.now()}`,
    method: 'POST',
    data: { userName, orderNum }
})