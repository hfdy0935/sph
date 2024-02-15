import { reactive } from 'vue'
import { defineStore } from 'pinia'
import { reqSearchList } from '@/api'

export const useSearchStore = defineStore('searchStore',() => {
    // 防止页面一刷新数据就没了，保存到localStorage
    // 搜索页面输入框params参数
    let paramsOfSearchComponentFromLocalStorage = localStorage.getItem('paramsOfSearchComponent')? JSON.parse(localStorage.getItem('paramsOfSearchComponent') as string) : {};
    let paramsOfSearchComponent = reactive(paramsOfSearchComponentFromLocalStorage);
    // 修改
    function changeParamsOfSearchComponent(params: object){
        Object.assign(paramsOfSearchComponent, params);
        localStorage.setItem('paramsOfSearchComponent',JSON.stringify(paramsOfSearchComponent));
    }
    // 清空，删除params搜索导航时执行
    function clearParamsOfSearchComponent(){
        Object.keys(paramsOfSearchComponent).forEach((item)=>{
            delete paramsOfSearchComponent[item];
        })
        localStorage.removeItem('paramsOfSearchComponent');
    }


    // 搜索页面选择分类query参数
    let queryOfSearchComponentFromLocalStorage = localStorage.getItem('queryOfSearchComponent')? JSON.parse(localStorage.getItem('queryOfSearchComponent') as string) : {};
    let queryOfSearchComponent = reactive(queryOfSearchComponentFromLocalStorage);
    // 修改
    function changeQueryOfSearchComponent(query: object){
        Object.assign(queryOfSearchComponent, query);
        localStorage.setItem('queryOfSearchComponent',JSON.stringify(queryOfSearchComponent));
    }
    // 清空，删除query分类导航时执行
    function clearQueryOfSearchComponent(){
        Object.keys(queryOfSearchComponent).forEach((item)=>{
            delete queryOfSearchComponent[item];
        })
        localStorage.removeItem('queryOfSearchComponent');
    }



    
    let requestBody = reactive({});
    initRequestBody();
      
    // 初始化requestBody
    function initRequestBody(){
        Object.assign(requestBody,{
            category1Id: "", //一级分类的id
            category2Id: "", //二级分类的id
            category3Id: "", //三级分类的id
            category1Name: "", //一级分类的名字
            category2Name: "", //二级分类的名字
            category3Name: "", //三级分类的名字
            keyword: "", //用户搜索的关键字
            props: [], //商品属性的搜索条件
            tradeMark: "", //品牌的搜索条件
            // order: "1:desc", //排序的参数 【默认初始值:1:desc】
            pageNo: 1, //当前分页器的页码  【默认初始值:1】
            pageSize: 20, //代表当前一页显示几条数据 【默认初始值:10】
          });
    }
    // 修改requestBody
    // p是所有参数合并的对象
    function changeRequestBody(p: object){
        Object.assign(requestBody, p);
    }
    
    // 发送请求
    async function getSearchList(){
        let res = await reqSearchList(requestBody);
        return await res
    }
    return {
        paramsOfSearchComponent,
        changeParamsOfSearchComponent,
        clearParamsOfSearchComponent,
        queryOfSearchComponent,
        changeQueryOfSearchComponent,
        clearQueryOfSearchComponent,
        requestBody,
        initRequestBody,
        changeRequestBody,
        getSearchList
    }
})
