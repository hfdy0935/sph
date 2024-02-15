# cSpell:ignore fastapi, pydantic
from fastapi import APIRouter, Body
from pydantic import BaseModel
import os, json, random

trade = APIRouter(
    prefix = '/api/trade',
    tags = ['订单和结算']
)
base_path = os.path.dirname(__file__) + '\\data\\'
    
# 读取json订单信息
def get_original_order(path: str):
    data = []
    with open(path, 'r', encoding = 'utf-8') as f:
        try:
            data = json.load(f)
        except: pass
    return data

# 写入json订单信息
def write_order_info(path: str, value: list) -> None:
    with open(path, 'w', encoding = 'utf-8') as f:
        json.dump(value, f, ensure_ascii = False, indent = 2)

@trade.post('/order/{time}')
def submitTrade(item = Body(...)):
    tel = item['shoppingCartSelected'][0]['userName']
    record_path = base_path + tel + '.json'
    orderNum = str([random.randint(0,10) for i in range(10)]).replace('[','').replace(']','').replace(',','').replace(' ','')
    item['orderNum'] = orderNum
    # 首次创建订单记录文件
    if not os.path.exists(record_path):
        with open(record_path, 'w', encoding = 'utf-8') as f:
            pass
    original_data = get_original_order(record_path)
    write_order_info(record_path, original_data + [item])
    return {'message': 'OK', 'orderNum': orderNum}
    

@trade.post('/pay/{time}')
def payTrade(item = Body(...)):
    print(item)
    tel = item['userName']
    record_path = base_path + tel + '.json'
    # 原来的订单记录
    original_data = get_original_order(record_path)
    # 查找和支付订单的订单号相同的订单并修改信息
    for index,data in enumerate(original_data):
        if data['orderNum'] == item['orderNum']:
            original_data[index]['hasPaid'] = item['hasPaid']
            original_data[index]['payPlatform'] = item['payPlatform']
            break
    write_order_info(record_path, original_data)
    return {'message': 'OK'}

class DeleteOneTrade(BaseModel):
    userName: str
    orderNum: str

@trade.post('/delete/{time}')
def deleteTrade(item: DeleteOneTrade):
    record_path = base_path + item.userName + '.json'
    try:
        original_data = get_original_order(record_path)
        print(len(original_data))
        # 找到要删的订单
        target = [i['orderNum'] == item.orderNum for i in original_data]
        original_data.pop(target.index(True))
        # 重新写入
        write_order_info(record_path, original_data)
        return {'message': 'OK'}
    except:
        return {'message': 'Error'}
    