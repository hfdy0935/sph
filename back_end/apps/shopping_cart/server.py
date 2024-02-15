# cSpell:ignore fastapi, pydantic

from fastapi import APIRouter, Request, Body
from pydantic import BaseModel
from typing import Annotated
import os
import json



shopping_cart = APIRouter(
    prefix = '/api/shoppingCart', 
    tags = ['购物车相关路由']
)


class goodsInfo(BaseModel):
    attrs: str | None = None
    category1Id: str | None = None
    category1Name: str | None = None
    category2Id: str | None = None
    category2Name: str | None = None
    category3Id: str | None = None
    category3Name: str | None = None
    color: str
    defaultImg: str
    hotScore: float
    id: int
    memory: str
    price: int
    sales: int
    title: str
    tmId: str | None = None
    tmName: str | None = None
    version: str
    way: str

class submitInfo(BaseModel):
    buyNum: int
    price: int
    submitTime: list
    totalMoney: int


class Item(BaseModel):
    goodsInfo: goodsInfo
    submitInfo: submitInfo
    userName: str


base_path = os.path.dirname(__file__) + '\\record\\'
user_path =  os.path.dirname(__file__).split('\\')
user_path = '\\'.join(user_path[:len(user_path) - 1]) + '\\users\\data\\users.json'
# 用户是否注册
def is_registered(username: str):
    users = []
    with open(user_path, 'r', encoding = 'utf-8') as f:
        try:
            users = json.load(f)
        except:
           pass
        print(any(username == user['tel'] for user in users))
        return any(username == user['tel'] for user in users)

# 提交购物车
@shopping_cart.post('/set/{time}')
def shopping_cart_function(
    request: Request,
    item: Annotated[Item, Body(..., description = '请求商品信息')]
):
    if not is_registered(item.userName):
        return {'message': 'Error', 'detail': '用户还未登录'}
    record_path = base_path + item.userName + '.json'
    if not os.path.exists(record_path):
        with open(record_path, 'w', encoding = 'utf-8') as f:
            pass

    origin_data = []
    with open(record_path, 'r', encoding = 'utf-8') as f:
        try:
            origin_data = json.load(f)
        except:
            pass

    with open(record_path, 'w', encoding = 'utf-8') as f:
        # 首次添加
        if not origin_data:
            json.dump([item.dict()], f, ensure_ascii = False, indent = 2)
            return {'message': 'OK', 'log': '首次添加'}
        else:
            # 只有一条数据时类型是字典，这里要转成列表
            origin_data = origin_data if isinstance(origin_data, list) else [origin_data]
            # 相同商品
            for k in origin_data:
                if k['goodsInfo'] == item.goodsInfo.dict():
                    k['submitInfo']['buyNum'] += item.submitInfo.buyNum
                    k['submitInfo']['totalMoney'] += item.goodsInfo.price
                    k['submitInfo']['submitTime'] += item.submitInfo.submitTime
                    json.dump(origin_data, f, ensure_ascii = False, indent = 2)
                    return {'message':'OK', 'log': '相同商品'}
            # 不同商品、同一商品不同售卖属性
            json.dump(origin_data + [item.dict()], f, ensure_ascii = False, indent = 2)
            return {'message':'OK', 'log': '不同商品、同一商品不同售卖属性'}


# 获取购物车
@shopping_cart.post('/get/{time}')
def get_shopping_cart(
    request: Request, 
    item = Body(description = '获取购物车数据')
):
    record_path = base_path + item['userName'] + '.json'
    if not os.path.exists(record_path):
        with open(record_path, 'w', encoding = 'utf-8') as f:
            pass
    with open(record_path, 'r', encoding = 'utf-8') as f:
        try:
            return json.load(f)
        except:
            return []
    

# 修改购物车请求体模型
class changeItemModel(BaseModel):
    index: int
    data: Item
    userName: str


# 修改购物车
@shopping_cart.post('/change/{time}')
def change_shopping_cart(
    item: Annotated[changeItemModel, Body(description = '请求商品信息')], 
    request: Request
):
    origin_data = ''
    record_path = base_path + item.userName + '.json'
    # 读取原购物车数据
    with open(record_path, 'r', encoding = 'utf-8') as f:
        origin_data = json.load(f)
        # 修改
        origin_data[item.index] = item.data.dict()
    # 重新写入
    with open(record_path, 'w', encoding = 'utf-8') as f:
        json.dump(origin_data, f, ensure_ascii = False, indent = 2)
    return {'message': 'OK'}


class DeleteShoppingCartModel(BaseModel):
    index: list[int]
    userName: str

# 删除购物车
@shopping_cart.post('/delete/{time}')
def delete_shopping_cart(request: Request, item: DeleteShoppingCartModel):
    origin_data = ''
    record_path = base_path + item.userName + '.json'
    with open(record_path, 'r', encoding = 'utf-8') as f:
        origin_data = json.load(f)
    # 从后往前删
    for i in sorted(item.index, reverse = True):
        origin_data.pop(i)
    # 重新写入
    with open(record_path, 'w', encoding = 'utf-8') as f:
        json.dump(origin_data, f, ensure_ascii = False, indent = 2)
    return {'message': 'OK'}
